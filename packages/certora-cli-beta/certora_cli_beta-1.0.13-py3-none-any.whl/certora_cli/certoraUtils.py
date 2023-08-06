import json
import os
import requests
# import secrets
import sys
import subprocess
import platform
import shlex
import time
import zipfile
import shutil
from datetime import datetime
import re
from tqdm import tqdm  # type: ignore
from typing import Any, Dict, List, Optional, cast
from certora_cli.certoraTester import compareResultsWithExpected, get_errors, has_violations, get_violations  # type: ignore

MAX_FILE_SIZE = 10 * 1024 * 1024
NO_OUTPUT_LIMIT_MINUTES = 15
MAX_POLLING_TIME_MINUTES = 120
LOG_READ_FREQUENCY = 10
MAX_ATTEMPTS_TO_FETCH_OUTPUT = 3
DELAY_FETCH_OUTPUT_SECONDS = 10
config_path = "%s/%s" % (os.getcwd().replace("\\", "/"), ".certora_config")
CompressingProgress = "  - compressing  ({}/{})\r"
Response = requests.models.Response

# bash colors
bashGreenColor = "\033[32m"
bashRedColor = "\033[31m"
bashColorEnd = "\033[0m"

# error messages
TimeoutMsgPrefix = bashRedColor + "Request timed out." + bashColorEnd
ErrorMsgPrefix = bashRedColor + "An error occurred:" + bashColorEnd
ErrorStatusPrefix = bashRedColor + "Error Status:" + bashColorEnd
ConnectionErrorPrefix = bashRedColor + "Connection error:" + bashColorEnd
VaasErrorPrefix = bashRedColor + "Server reported an error:" + bashColorEnd
ServerErrorPrefix = bashRedColor + "Server Error" + bashColorEnd
verificationErrorMsgPrefix = bashRedColor + "Prover found violations:" + bashColorEnd

# option names

DEFAULT_CONF = "default.conf"
MANDATORY_CONTRACTS = "contracts"
OPTION_OUTPUT = "output"
OPTION_OUTPUT_FOLDER = "output_folder"
OPTION_OUTPUT_VERIFY = "output_verify"
OPTION_PATH = "path"
OPTION_PACKAGES_PATH = "packages_path"
OPTION_PACKAGES = "packages"
OPTION_SOLC_MAP = "solc_map"
OPTION_SOLC = "solc"
OPTION_LINK = "link"
OPTION_STRUCT_LINK = "structLink"
OPTION_ADDRESS = "address"
OPTION_VERIFY = "verify"
OPTION_ASSERT = "assert"
OPTION_CACHE = "cache"
OPTION_LINK_CANDIDATES = "linkCandidates"
OPTION_SOLC_ARGS = "solc_args"
ENVVAR_CERTORA = "CERTORA"
JAVA_ARGS_KEY = "java_args"

# completion messages
completeCompress = bashGreenColor + "Finished compressing" + bashColorEnd
completeSubmit = bashGreenColor + "Job submitted to server" + bashColorEnd
noVerificationErrors = bashGreenColor + "No errors found by Prover!" + bashColorEnd

common_solidity_options = ["--optimize", "--optimize-runs"]
legal_run_args = ["--settings", "--cache", "--output", "--output_folder",
                  "--link",
                  "--" + OPTION_STRUCT_LINK,
                  "--address", "--path", "--packages_path", "--packages", "--solc",
                  "--solc_args", "--verify", "--assert", "--dont_fetch_sources", "--toolOutput",
                  "--iscygwin", "--varmap", "--build", "--jar", "--debug", "--help",
                  "--cloud", "--staging", "--local", "--key", "--javaArgs", "--solc_map",
                  "--msg", "--queue_wait_minutes", "--max_poll_time", "--log_query_frequency_seconds",
                  "--disableLocalTypeChecking"]
legal_run_args += common_solidity_options
legal_build_args = ["--cache", "--output", "--output_folder", "--link",
                    "--" + OPTION_STRUCT_LINK,
                    "--address", "--path", "--packages_path", "--packages", "--solc",
                    "--solc_args", "--verify", "--assert", "--dont_fetch_sources",
                    "--solc_map", "--iscygwin", "--varmap", "--debug", "--help"]
legal_build_args += common_solidity_options

CERTORA_CONFIG = ".certora_config"  # folder
CERTORA_BUILD = ".certora_build.json"
CERTORA_VERIFY = ".certora_verify.json"

class TimeError(Exception):
    """A custom exception used to report on time elapsed errors"""


class CloudVerification:
    """Represents an AWS Cloud verification"""

    def __init__(self, timers: Dict[str, int] = {}) -> None:
        self.queue_wait_minutes = timers["--queue_wait_minutes"] if \
            "--queue_wait_minutes" in timers else NO_OUTPUT_LIMIT_MINUTES
        self.max_poll_minutes = timers["--max_poll_minutes"] if \
            "--max_poll_minutes" in timers else MAX_POLLING_TIME_MINUTES
        self.log_read_frequency = timers["--log_query_frequency_seconds"] if \
            "--log_query_frequency_seconds" in timers else LOG_READ_FREQUENCY
        self.max_attempts_to_fetch_output = timers["--max_attempts_to_fetch_output"] if \
            "--max_attempts_to_fetch_output" in timers else MAX_ATTEMPTS_TO_FETCH_OUTPUT
        self.delay_fetch_output_seconds = timers["--delay_fetch_output_seconds"] if \
            "--delay_fetch_output_seconds" in timers else DELAY_FETCH_OUTPUT_SECONDS
        self.runName = os.urandom(10).hex()
        self.ZipFileName = self.runName + ".zip"
        self.env = ""
        self.url = ""
        self.jsonOutputUrl = ""
        self.outputUrl = ""
        self.statusUrl = ""
        self.reportUrl = ""
        self.zipOutputUrl = ""

    # jar output (logs) url
    def setOutputUrl(self, userId: int, anonymousKey: str) -> None:
        if self.url == "":
            debug_print_("setOutputUrl(): url is not defined.")
        elif self.runName == "":
            debug_print_("setOutputUrl(): runName is not defined.")
        else:
            self.outputUrl = "{url}/job/{userId}/{runName}?" \
                             "anonymousKey={anonymousKey}".format(url=self.url,
                                                                  userId=userId,
                                                                  runName=self.runName,
                                                                  anonymousKey=anonymousKey)

    # index report url
    def setReportUrl(self, userId: int, anonymousKey: str) -> None:
        if self.url == "":
            debug_print_("setReportUrl(): url is not defined.")
        elif self.runName == "":
            debug_print_("setReportUrl(): runName is not defined.")
        else:
            self.reportUrl = "{url}/output/{userId}/{runName}/?" \
                             "anonymousKey={anonymousKey}".format(url=self.url,
                                                                  userId=userId,
                                                                  runName=self.runName,
                                                                  anonymousKey=anonymousKey)

    # status page url
    def setStatusUrl(self, userId: int, anonymousKey: str) -> None:
        if self.url == "":
            debug_print_("setStatusUrl(): url is not defined.")
        elif self.runName == "":
            debug_print_("setStatusUrl(): runName is not defined.")
        else:
            self.statusUrl = "{url}/jobStatus/{userId}/{runName}?" \
                             "anonymousKey={anonymousKey}".format(url=self.url,
                                                                  userId=userId,
                                                                  runName=self.runName,
                                                                  anonymousKey=anonymousKey)

    # compressed output folder url
    def setZipOutputUrl(self, userId: int, anonymousKey: str) -> None:
        if self.url == "":
            debug_print_("setZipOutputUrl(): url is not defined.")
        elif self.runName == "":
            debug_print_("setZipOutputUrl(): runName is not defined.")
        else:
            self.zipOutputUrl = "{url}/zipOutput/{userId}/{runName}?" \
                                "anonymousKey={anonymousKey}".format(url=self.url,
                                                                     userId=userId,
                                                                     runName=self.runName,
                                                                     anonymousKey=anonymousKey)

    # json output url
    def setJsonOutputUrl(self, userId: int, anonymousKey: str) -> None:
        if self.url == "":
            debug_print_("setJsonOutputUrl(): url is not defined.")
        elif self.runName == "":
            debug_print_("setJsonOutputUrl(): runName is not defined.")
        else:
            self.jsonOutputUrl = "{url}/jsonOutput/{userId}/{runName}?" \
                                 "anonymousKey={anonymousKey}".format(url=self.url,
                                                                      userId=userId,
                                                                      runName=self.runName,
                                                                      anonymousKey=anonymousKey)

    def prepare_auth_data(self, args: Dict[str, str]) -> Optional[Dict[str, Any]]:
        certoraKey = getKey(args)
        if not certoraKey:
            print("Please provide certoraKey")
            return None

        process_name = getProcessName(args)
        authData = {
            "certoraKey": certoraKey,
            "runName": self.runName
        }  # type: Dict[str, Any]

        if process_name:
            authData["process"] = process_name

        if self.env == "staging":
            authData["branch"] = getBranch(args)

        if "settings" in args:
            # authData["settings"] = args["settings"]
            authData["jarSettings"] = []
            for key_val in args["settings"]:
                authData["jarSettings"].extend(key_val.strip().split(" "))

        if JAVA_ARGS_KEY in args:
            authData["javaArgs"] = args[JAVA_ARGS_KEY]
        if "buildArgs" in args:
            authData["buildArgs"] = args["buildArgs"]
        if OPTION_CACHE in args:
            authData["toolSceneCacheKey"] = args[OPTION_CACHE]
        if "msg" in args:  # used for notification
            authData["msg"] = args["msg"]
        return authData

    def cliVerify(self, args: Dict[str, str], compareToExpected: bool = True) -> bool:
        """Sends a verification request to HTTP Handler, uploads a zip file and outputs the results

        Parameters
        ----------
        args :  Dict[str, str]
            prover arguments and additional configurations
        compareToExpected : bool
            if true, compares the expected output with the actual results

        Returns
        ------
        bool
            if compareToExpected is True, returns True when the expected output equals the actual results.
            otherwise returns False if there was at least one violated rule
        """

        self.env = args["env"] if "env" in args else ""
        self.url = getUrl(self.env)

        authData = self.prepare_auth_data(args)
        if authData is None:
            return False
        resp = self.verificationRequest(authData)  # send post request to /cli/vertify

        if resp is None:  # on error
            return False

        if resp.status_code != requests.codes.ok:
            respStatus = resp.status_code
            if respStatus == 403:
                print("You have no permission. Please, make sure you entered a valid key.")
                return False
            if respStatus == 502:
                debug_print_("502 Bad Gateway")
                print("Oops, an error occurred when sending your request. Please try again later")
                return False

            outputErrorResponse(resp)
            return False

        jsonResponse = parseJson(resp)
        if not jsonResponse:
            return False

        try:
            if not jsonResponse["success"]:  # on exception
                errString = jsonResponse[
                    "errorString"] if "errorString" in jsonResponse else "No error string in json response {}".format(
                    jsonResponse)
                print(ErrorMsgPrefix, errString, flush=True)
                return False

            anonymousKey = jsonResponse["anonymousKey"]
            presigned_url = jsonResponse["presigned_url"]
            userId = jsonResponse["userId"]
        except Exception as e:  # (Json) ValueError
            debug_print_(str(e))
            print(ErrorMsgPrefix, "Unexpected response")
            return False

        print("Compressing the files...", flush=True)
        print()
        # remove previous zip file
        if os.path.exists(self.ZipFileName):
            os.remove(self.ZipFileName)

        # create new zip file
        if not compressFiles(self.ZipFileName, CERTORA_BUILD, CERTORA_VERIFY, CERTORA_CONFIG):
            return False

        if os.path.getsize(self.ZipFileName) > MAX_FILE_SIZE:
            print(ErrorMsgPrefix, "Max 10MB file size exceeded.", flush=True)
            return False
        print(completeCompress, flush=True)
        print()
        print("Uploading files...", flush=True)
        if self.upload(presigned_url, self.ZipFileName):
            print(completeSubmit, flush=True)
            print()
        else:  # upload error
            return False
        os.remove(self.ZipFileName)  # remove zip file

        # set results url
        self.setOutputUrl(userId, anonymousKey)
        self.setStatusUrl(userId, anonymousKey)
        self.setReportUrl(userId, anonymousKey)
        self.setZipOutputUrl(userId, anonymousKey)
        self.setJsonOutputUrl(userId, anonymousKey)
        if self.outputUrl == "":  # on error
            return False
        print("You can follow up on the status:", self.statusUrl)
        print()
        print("Output:", flush=True)

        try:
            self.newPollOutput(self.outputUrl, self.statusUrl)
        except (requests.exceptions.ConnectionError, KeyboardInterrupt):
            print("You were disconnected from server, but your request is still being processed.")
            print("You can follow up on the status:", self.statusUrl)
            print("You will also receive an email notification when this process is completed")
            print("When the job is completed, use the following link for downloading compressed results folder: ",
                  self.zipOutputUrl)
            # print("When the job is completed without errors, the results will be presented in", indexPath)
            return False
        except requests.exceptions.RequestException:
            # other requests exceptions
            printConnError()
            return False
        except TimeError:
            return False
        except Exception as e:
            print("Encountered an error: " + str(e))
            return False

        print()
        print("Status page:", self.statusUrl)
        print("Verification report:", self.reportUrl)
        print("Finished verification request")

        if compareToExpected:
            return checkResultsFromWeb(self.jsonOutputUrl,
                                       self.max_attempts_to_fetch_output,
                                       self.delay_fetch_output_seconds)
        return True

    def verificationRequest(self, authData: Dict[str, Any]) -> Optional[Response]:
        verifyUrl = self.url + "/cli/verify"

        try:
            return requests.post(verifyUrl, data=authData, timeout=60)
        except requests.exceptions.Timeout:
            # set up for a retry?
            print(TimeoutMsgPrefix, "Please, contact Certora on https://www.certora.com", flush=True)
        except (requests.exceptions.RequestException, ConnectionError):
            printConnError()
        return None

    def newPollOutput(self, url: str, statusUrl: str, lim: int = 60) -> bool:
        has_output = True
        params = ""
        nextToken = ""
        result = False
        # progressBar(35)
        print()
        start_poll_t = time.perf_counter()

        while True:
            try:
                if nextToken:  # used for retrieving the logs in chunks
                    params = "&nextToken=" + nextToken

                r = requests.get(url + params, timeout=lim)
                if r.status_code != requests.codes.ok:
                    if r.status_code != 502:
                        outputErrorResponse(r)
                        raise requests.exceptions.RequestException
                        # raise Exception('No additional output is available')
                    else:
                        debug_print_("502 Bad Gateway")
                        allOutput = None
                        newToken = nextToken  # keep the same token
                        status = "PROCESSED"
                else:
                    jsonResponse = parseJson(r)
                    if not jsonResponse:  # Error parsing json
                        print(ErrorMsgPrefix, "Failed to parse response. For more information visit", statusUrl)
                        break
                    if not isSuccessResponse(jsonResponse, statusUrl):  # look for execution exceptions
                        break
                    try:
                        status = jsonResponse["status"]
                    except KeyError:
                        errorMsg = "No status"
                        printErrorMessage(errorMsg, statusUrl)
                        break
                    try:
                        newToken = jsonResponse["nextToken"]
                    except KeyError:
                        errorMsg = "No token"
                        printErrorMessage(errorMsg, statusUrl)
                        break

                    try:
                        allOutput = jsonResponse["logEventsList"]
                    except KeyError:
                        errorMsg = "No output is available."
                        printErrorMessage(errorMsg, statusUrl)
                        break

                if allOutput:
                    has_output = True
                    for outputLog in allOutput:
                        msg = outputLog["message"]
                        print(msg, flush=True)
                elif has_output:  # first missing output
                    has_output = False
                    first_miss_out = time.perf_counter()  # start a timer
                else:  # missing output
                    curr_miss_out = time.perf_counter()
                    if curr_miss_out - first_miss_out > self.queue_wait_minutes * 60:  # more than N min
                        errorMsg = "There was no output for {} minutes.".format(self.queue_wait_minutes)
                        printErrorMessage(errorMsg, statusUrl)
                        raise TimeError()
                if newToken == nextToken and nextToken != "":
                    if status == "SUCCEEDED" or status == "FAILED":
                        # When finished it returns the same token you passed in
                        break
                    else:  # the job is still being processed
                        print("Job status:", status, flush=True)
                        print("No logs available yet...", flush=True)
                        time.sleep(self.log_read_frequency)
                        print()
                nextToken = newToken
            except requests.exceptions.Timeout:  # catch timeout and resend request
                # print("processing user request...")
                pass
            curr_poll_t = time.perf_counter()
            if curr_poll_t - start_poll_t > self.max_poll_minutes * 60:  # polling for more than 30 min
                errorMsg = "The contract is being processed " \
                           "for more than {} minutes".format(self.max_poll_minutes)
                printErrorMessage(errorMsg, statusUrl)
                raise TimeError()
            time.sleep(0.5)
        return result

    @staticmethod
    def upload(presigned_url: str, file_to_upload: str) -> Optional[Response]:
        """Uploads user contract/s as a zip file to S3

        Parameters
        ----------
        presigned_url : str
            S3 presigned url
        file_to_upload : str
            zip file name

        Returns
        -------
        Response
            S3 response - can be handled as a json object
        """
        try:
            with open(file_to_upload, "rb") as my_file:
                http_response = requests.put(presigned_url, data=my_file, headers={"content-type": "application/zip"})
        except OSError as e:
            print(ErrorMsgPrefix, "OSError:", "couldn't upload file -", file_to_upload)
            debug_print_(str(e))
        except ConnectionError as e:
            print(ErrorMsgPrefix, "ConnectionError:", "couldn't upload file -", file_to_upload)
            debug_print_(str(e))
        except requests.exceptions.Timeout as e:
            print(ErrorMsgPrefix, "Timeout:", "couldn't upload file -", file_to_upload)
            debug_print_(str(e))
        except requests.exceptions.RequestException as e:
            print(ErrorMsgPrefix, "couldn't upload file -", file_to_upload)
            debug_print_(str(e))
            return None

        return http_response


def check_legal_args(args: List[str], legal_args: List[str]) -> None:
    for arg in args:
        if arg.startswith("--") and arg not in legal_args:
            print("Error: argument is illegal {}".format(arg))
            sys.exit(1)

def getUrl(env: str) -> str:
    if env == "staging":
        url = 'https://vaas-stg.certora.com'
    else:
        url = 'https://prover.certora.com'
    return url

def getKey(args: Dict[str, str]) -> str:
    if "key" in args:
        return args["key"]
    if "CERTORAKEY" in os.environ:
        return os.environ["CERTORAKEY"]
    return ""

def getProcessName(args: Dict[str, str]) -> str:
    if "process" in args:
        return args["process"]
    return ""

def getBranch(args: Dict[str, str]) -> str:
    branch = args["branch"] if "branch" in args else ""
    if branch == "" or branch is None:
        return "master"

    return branch

# TODO: update error message - email notification (?)
def printErrorMessage(errorMsg: str, statusUrl: str) -> None:
    print(ErrorMsgPrefix, errorMsg)
    print("For further details visit", statusUrl)
    print("Closing connection...", flush=True)

def outputErrorResponse(response: Response) -> None:
    print(ErrorStatusPrefix, response.status_code)
    if response.status_code == 500:
        print(ServerErrorPrefix)
        print("Please, contact Certora on https://www.certora.com")
        return
    try:
        errorResponse = response.json()
        # print(errorResponse)
        if "errorString" in errorResponse:
            print(VaasErrorPrefix, errorResponse["errorString"])
        elif "message" in errorResponse:
            print(VaasErrorPrefix, errorResponse["message"])
    except Exception as e:
        print(ErrorMsgPrefix)
        print("Encountered an error: " + str(e))
        print(response.text)

def isSuccessResponse(jsonResponse: Dict[str, Any], statusUrl: str) -> bool:
    # When there is an exception while running the job
    # return False
    if "execException" in jsonResponse:
        exceptionResponse = jsonResponse["execException"]
        if exceptionResponse is not None:
            try:
                errorMsg = exceptionResponse[
                    "message"] if "message" in exceptionResponse else "No message in exception response {}".format(
                    exceptionResponse)
                printErrorMessage(errorMsg, statusUrl)
            except KeyError:
                print(ErrorMsgPrefix, "Server returned an error with no message:")
                print(exceptionResponse)
                print("Please contact Certora on https://www.certora.com")
            return False
    return True

def parseJson(response: Response) -> Dict[str, Any]:
    try:
        jsonResponse = response.json()
    except ValueError:
        print(ErrorMsgPrefix, "Could not parse JSON response")
        print(response.text)  # Should we print the whole response here?
        return {}
    return jsonResponse


def progressBar(total: int = 70, describe: str = "Initializing verification") -> None:
    for _ in tqdm(range(total),
                  bar_format="{l_bar}{bar}| [remaining-{remaining}]",
                  ncols=70, desc=describe, ascii=".#"):
        time.sleep(1)

def lookForPath(path: str) -> Optional[str]:
    try:
        r = requests.get(path, timeout=10)
        if r.status_code == requests.codes.ok:
            # read
            return r.json()
        else:
            return None
    except (requests.exceptions.Timeout, requests.exceptions.RequestException, ConnectionError):
        printConnError()
        return None


def printConnError() -> None:
    print(
        ConnectionErrorPrefix,
        "Server is currently unavailable. Please try again later.")
    print("For further information, please contact Certora on https://www.certora.com",
          flush=True)

def getTotalFiles(directory: str) -> int:
    try:
        total_files = sum(len(files) for _, _, files in os.walk(directory))
        return total_files
    except OSError:
        print(ErrorMsgPrefix, "Could not traverse", directory)
        return -1


def compressFiles(ZipFileName: str, *fileNames: Any) -> bool:
    zipObj = zipfile.ZipFile(ZipFileName, 'w', zipfile.ZIP_DEFLATED)

    total_files = 0
    for fileName in fileNames:
        # print(fileName)
        if os.path.isdir(fileName):
            total_dir_files = getTotalFiles(fileName)
            if total_dir_files == 0:
                print(ErrorMsgPrefix, "Provided directory - '{}' is empty.".format(fileName))
                return False
            elif total_dir_files > 0:
                total_files += total_dir_files
        elif os.path.isfile(fileName):
            total_files += 1
        else:
            print(ErrorMsgPrefix, "Provided file - '{}' does not exist.".format(fileName))
            return False
    if total_files < 1:
        if len(fileNames) == 0:
            print(ErrorMsgPrefix, "No file was provided. Please, contact Certora on https://www.certora.com")
        else:
            print(ErrorMsgPrefix, "Provided file(s) - {} do(es) not exist.".format(", ".join(fileNames)))
        return False

    i = 0

    for fileName in fileNames:
        if os.path.isdir(fileName):
            try:
                # traverse a directory
                for root, _, files in os.walk(fileName):
                    for f in files:
                        f_name = sanitize_path(os.path.join(root, f))
                        zipObj.write(f_name)
                        i += 1
                        print(CompressingProgress.format(i, total_files), flush=True, end="")
                print("", flush=True)
            except OSError:
                print(ErrorMsgPrefix, "Could not compress a directory -", fileName)
                return False
        else:  # zip file
            try:
                zipObj.write(fileName)
                i += 1
                print(CompressingProgress.format(i, total_files), flush=True, end="")
            except OSError:
                print(ErrorMsgPrefix, "Could not compress", fileName)
                return False

    zipObj.close()
    return True


def checkResultsFromWeb(outputPathURL: str, max_attempts: int, delay_between_attempts_seconds: int) -> bool:
    attempts = 0
    actual = None
    while actual is None and attempts < max_attempts:
        attempts += 1
        actual = lookForPath(outputPathURL)
        if actual is None and attempts >= max_attempts:
            print("Could not find actual results file output.json")
            return False
        elif actual is None:
            time.sleep(delay_between_attempts_seconds)

    return checkResults(cast(dict, actual))

def checkResultsFromFile(outputPath: str) -> bool:
    with open(outputPath) as outputPathFile:
        actual = json.load(outputPathFile)
        return checkResults(actual)

def checkResults(actual: Dict[str, Any]) -> bool:
    actualResults = actual
    expectedFilename = "expected.json"
    basedOnExpected = os.path.exists(expectedFilename)
    if basedOnExpected:  # compare actual results with expected
        with open(expectedFilename) as expectedFile:
            expected = json.load(expectedFile)
            if "rules" in actualResults and "rules" in expected:
                is_equal = compareResultsWithExpected("test", actualResults["rules"], expected["rules"], {}, {})
            elif "rules" not in actualResults and "rules" not in expected:
                is_equal = True
            else:
                is_equal = False

        if is_equal:
            print(noVerificationErrors, "(based on expected.json)")
            return True
        # not is_equal:
        errorStr = get_errors()
        if errorStr:
            print(verificationErrorMsgPrefix, errorStr)
        if has_violations():
            print(verificationErrorMsgPrefix)
            get_violations()
        return False

    # if expected results are not defined
    # traverse results and look for violation
    errors = []
    result = True

    if "rules" not in actualResults:
        errors.append("No rules in results")
        result = False
    else:
        for rule in actualResults["rules"].keys():
            ruleResult = actualResults["rules"][rule]
            if isinstance(ruleResult, str) and ruleResult != 'SUCCESS':
                errors.append("[rule] " + rule)
                result = False
            elif isinstance(ruleResult, dict):
                # nested rule - ruleName: {result1: [funcionts list], result2: [funcionts list] }
                nesting = ruleResult
                violatingFunctions = ""
                for method in nesting.keys():
                    if method != 'SUCCESS' and len(nesting[method]) > 0:
                        violatingFunctions += '\n  [func] ' + '\n  [func] '.join(nesting[method])
                        result = False
                if violatingFunctions:
                    errors.append("[rule] " + rule + ":" + violatingFunctions)

    if not result:
        print(verificationErrorMsgPrefix)
        print('\n'.join(errors))
        return False
    # if result:
    print(noVerificationErrors)
    return True

def fatal_error(s: str, DEBUG: bool = False) -> None:
    print(s)
    if DEBUG:
        raise Exception(s)
    sys.exit(1)

def debug_print_(s: str, DEBUG: bool = False) -> None:
    if DEBUG:
        print(s)

def is_windows() -> bool:
    return platform.system() == 'Windows'

def get_file_name(file: str) -> str:
    return ''.join(file.split("/")[-1])

def get_file_basename(file: str) -> str:
    return ''.join(file.split("/")[-1].split(".")[0:-1])

def get_file_extension(file: str) -> str:
    return file.split("/")[-1].split(".")[-1]

def safe_create_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except OSError:
        debug_print_("Failed to create directory %s: %s" % (path, sys.exc_info()))
        pass

def as_posix(path: str) -> str:
    return path.replace("\\", "/")

def getcwd() -> str:
    return as_posix(os.getcwd().replace("\\", "/"))


def remove_and_recreate_dir(path: str) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)
    safe_create_dir(path)


def print_failed_to_run(cmd: str) -> None:
    print()
    print("Failed to run %s" % (cmd, ))
    if is_windows() and cmd.find('solc') != -1 and cmd.find('exe') == -1:
        print("did you forget the .exe extension for solcXX.exe??")
    print()


def run_cmd(cmd: str, name: str, config_path: str, input: bytes = None, shell: bool = False) -> None:
    debug_print_("Running cmd %s" % (cmd,))

    stdout_name = "%s/%s.stdout" % (config_path, name)
    stderr_name = "%s/%s.stderr" % (config_path, name)
    debug_print_("stdout, stderr = %s,%s" % (stdout_name, stderr_name))

    with open(stdout_name, 'w+') as stdout:
        with open(stderr_name, 'w+') as stderr:
            try:
                args = prepare_call_args(cmd)
                if shell:
                    shell_args = ' '.join(args)
                    exitcode = subprocess.run(shell_args, stdout=stdout, stderr=stderr,
                                              input=input, shell=shell).returncode
                else:
                    exitcode = subprocess.run(args, stdout=stdout, stderr=stderr, input=input, shell=shell).returncode
                if exitcode:
                    msg = "Failed to run %s, exit code %d" % (cmd, exitcode)
                    with open(stderr_name, 'r') as stderr_read:
                        for line in stderr_read:
                            print(line)
                    raise Exception(msg)
                else:
                    debug_print_("Exitcode %d" % (exitcode,))
            except Exception:
                print_failed_to_run(cmd)
                raise


def run_cmd_slim(cmd: str, name: str) -> None:
    try:
        exitcode = subprocess.call(shlex.split(cmd))
        if exitcode:
            print("Failed to run %s, got exitcode %d" % (cmd, exitcode))
            sys.exit(1)
        else:
            debug_print_("Exitcode %d" % (exitcode,))
    except Exception:
        print_failed_to_run(cmd)
        raise

def unfold_option(parsed_option: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates option (as string) into a dictionary
    Expected option format is {param1}:{param2}={param3}
    Returned dictionary is { 'param1': { 'param2': 'param3' } }
    """
    unfolded_option = {}  # type: Dict[str, Any]
    for link in parsed_option:
        k, f_v = link.split(":", 2)
        f, v = f_v.split("=", 2)

        if k in unfolded_option:
            unfolded_option[k][f] = v
        else:
            unfolded_option[k] = {f: v}
    return unfolded_option

def current_conf_to_file(parsed_options: Dict[str, Any], files: List[str], fileToContractName: Dict[str, str]) -> None:
    out = {}

    def simple_set(option: str) -> None:
        if option in parsed_options:
            out[option] = parsed_options[option]

    simple_set(OPTION_CACHE)
    simple_set(OPTION_OUTPUT)
    simple_set(OPTION_OUTPUT_FOLDER)
    simple_set(OPTION_OUTPUT_VERIFY)
    simple_set(OPTION_PACKAGES_PATH)
    simple_set(OPTION_SOLC)
    simple_set(OPTION_SOLC_MAP)
    simple_set(OPTION_PATH)
    simple_set(OPTION_SOLC_ARGS)

    if OPTION_LINK in parsed_options:
        out[OPTION_LINK] = unfold_option(parsed_options[OPTION_LINK])

    if OPTION_STRUCT_LINK in parsed_options:
        out[OPTION_STRUCT_LINK] = unfold_option(parsed_options[OPTION_STRUCT_LINK])

    if OPTION_PACKAGES in parsed_options:
        out[OPTION_PACKAGES] = {}
        for package_entry in parsed_options[OPTION_PACKAGES].split(" "):
            package, package_path = package_entry.split("=", 2)
            out[OPTION_PACKAGES][package] = package_path

    if OPTION_ADDRESS in parsed_options:
        out[OPTION_ADDRESS] = {}
        for manual_address_entry in parsed_options[OPTION_ADDRESS]:
            out[OPTION_ADDRESS][manual_address_entry] = parsed_options[OPTION_ADDRESS][manual_address_entry]

    if OPTION_VERIFY in parsed_options:
        out[OPTION_VERIFY] = {}
        for verquery_entry in parsed_options[OPTION_VERIFY]:
            contract, spec = verquery_entry.split(":", 2)
            if contract in out[OPTION_VERIFY]:
                out[OPTION_VERIFY][contract].append(spec)
            else:
                out[OPTION_VERIFY][contract] = [spec]

    if OPTION_ASSERT in parsed_options:
        out[OPTION_ASSERT] = parsed_options[OPTION_ASSERT]

    # TODO: Add OPTION_LINK_CANDIDATES handling from command line to conf

    # finally... files:
    out[MANDATORY_CONTRACTS] = []
    for file in files:
        out[MANDATORY_CONTRACTS].append("%s:%s" % (file, fileToContractName[file]))

    safe_create_dir(".last_confs")
    out_file_name = ".last_confs/last_conf_%s.conf" % (datetime.now().strftime("%d_%m_%Y__%H_%M_%S"))
    with open(out_file_name, 'w+') as out_file:
        json.dump(out, out_file, indent=4, sort_keys=True)

def handle_file_list(file_list: List[str], files: List[str], fileToContractName: Dict[str, str]) -> None:
    for arg in file_list:
        if arg.startswith("--"):
            break

        if is_windows():
            path_normalized_file = arg.replace("\\", "/")
        else:
            path_normalized_file = arg

        if ":" in path_normalized_file:
            contract_path = path_normalized_file.split(":")[0]
            contract_name = path_normalized_file.split(":")[1]
            files.append(contract_path)
            fileToContractName[contract_path] = contract_name
        else:
            files.append(path_normalized_file)
            fileToContractName[path_normalized_file] = get_file_basename(path_normalized_file)

def flatter_link(option_link: Dict[str, Any]) -> List[str]:
    flattened_links = []
    for linked in option_link:
        for field in option_link[linked]:
            flattened_links.append("%s:%s=%s" % (linked, field, option_link[linked][field]))
    return flattened_links

# features: read from conf. write last to last_conf and to conf_date..
def read_from_conf(conf_file_name: str, parsed_options: Dict[str, Any], files: List[str],
                   fileToContractName: Dict[str, str]) -> None:
    with open(conf_file_name, "r") as conf_file:
        json_obj = json.load(conf_file)
        if MANDATORY_CONTRACTS not in json_obj:
            raise Exception("Configuration file %s must specify contract files in \"contracts\"" % conf_file_name)

        handle_file_list(json_obj[MANDATORY_CONTRACTS], files, fileToContractName)

        if OPTION_SOLC in json_obj:
            parsed_options[OPTION_SOLC] = json_obj[OPTION_SOLC]

        if OPTION_SOLC_ARGS in json_obj:
            parsed_options[OPTION_SOLC_ARGS] = json_obj[OPTION_SOLC_ARGS]

        if OPTION_LINK in json_obj:
            parsed_options[OPTION_LINK] = flatter_link(json_obj[OPTION_LINK])

        if OPTION_STRUCT_LINK in json_obj:
            parsed_options[OPTION_STRUCT_LINK] = flatter_link(json_obj[OPTION_STRUCT_LINK])

        if OPTION_ADDRESS in json_obj:
            parsed_options[OPTION_ADDRESS] = {}
            for entry in json_obj[OPTION_ADDRESS]:
                parsed_options[OPTION_ADDRESS][entry] = json_obj[OPTION_ADDRESS][entry]

        if OPTION_PACKAGES in json_obj:
            flattened_packages = []
            for package in json_obj[OPTION_PACKAGES]:
                package_loc = json_obj[OPTION_PACKAGES][package]
                if package_loc.find("$PWD") != -1:
                    package_loc = package_loc.replace("$PWD", os.getcwd().replace("\\", "/"))
                flattened_packages.append("%s=%s" % (package, package_loc))
            parsed_options[OPTION_PACKAGES] = ' '.join(flattened_packages)

        if OPTION_VERIFY in json_obj:
            flattened_verification_queries = []
            for contract_verquery in json_obj[OPTION_VERIFY]:
                for specfile in json_obj[OPTION_VERIFY][contract_verquery]:
                    flattened_verification_queries.append("%s:%s" % (contract_verquery, specfile))
            parsed_options[OPTION_VERIFY] = flattened_verification_queries

        if OPTION_ASSERT in json_obj:
            parsed_options[OPTION_ASSERT] = json_obj[OPTION_ASSERT]

        if OPTION_LINK_CANDIDATES in json_obj:
            parsed_options[OPTION_LINK_CANDIDATES] = json_obj[OPTION_LINK_CANDIDATES]

        if OPTION_CACHE in json_obj:
            parsed_options[OPTION_CACHE] = json_obj[OPTION_CACHE]

        if OPTION_PATH in json_obj:
            parsed_options[OPTION_PATH] = json_obj[OPTION_PATH].replace("$PWD", sanitize_path(os.getcwd()))


"""
 Hack to avoid problems with the parameter of --solc_args (problem is that the
 parameter looks like an option).

 Changes its parameter object (a list) in place.

 What this actually does:
   look for the argument "--solc_args"
   prepend the argument that immediately follows "--solc_args" with a space, so
   it is not recognized as an option by the argument parsing logic.

 source of inspiration:
   https://stackoverflow.com/questions/16174992/cant-get-argparse-to-read-quoted-string-with-dashes-in-it
"""
def nestedOptionHack(args: List[str]) -> None:
    for i in range(len(args)):
        debug_print_(args[i])
        if args[i] == '--' + OPTION_SOLC_ARGS:
            try:
                # TODO: throw a warning if args[i+1] matches one of the options of this script
                args[i + 1] = ' ' + args[i + 1]
            except IndexError:
                print("Error: '-solc_args' needs a parameter, thus cannot be the last argument")
                sys.exit()

def sanitize_path(pathString: str) -> str:
    return pathString.replace("\\", "/")

def prepare_call_args(cmd: str) -> List[str]:
    split = shlex.split(cmd)
    if split[0].endswith('.py'):
        # sys.executable returns a full path to the current running python, so it's good for running our own scripts
        certora_root = get_certora_root_directory()
        args = [sys.executable] + [sanitize_path(os.path.join(certora_root, split[0]))] + split[1:]
    else:
        args = split
    return args

def get_certora_root_directory() -> str:
    return os.getenv(ENVVAR_CERTORA, os.getcwd())


def which(filename: str) -> Optional[str]:
    if is_windows() and not re.search(r"\.exe$", filename):
        filename += ".exe"

    # TODO: find a better way to iterate over all directories in path
    for dirname in os.environ['PATH'].split(os.pathsep) + [os.getcwd()]:
        candidate = os.path.join(dirname, filename)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return filename

    return None
