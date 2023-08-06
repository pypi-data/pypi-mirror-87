#!/usr/bin/env python3

import os
import sys
import subprocess
import traceback
from certora_cli.certoraUtils import read_from_conf, get_certora_root_directory  # type: ignore
from certora_cli.certoraUtils import OPTION_CACHE, DEFAULT_CONF
from certora_cli.certoraUtils import nestedOptionHack, debug_print_
from certora_cli.certoraUtils import sanitize_path, prepare_call_args
from certora_cli.certoraUtils import legal_run_args, check_legal_args, CloudVerification, checkResultsFromFile
from certora_cli.certoraUtils import CERTORA_BUILD, CERTORA_VERIFY
from certora_cli.certoraUtils import which

from typing import Dict, List, Optional, Tuple, Any

# a list of valid environments to be used when running remotly
VALID_ENVS = ["--staging", "--cloud"]
JAR_PATH_KEY = "jar_path"
JAVA_ARGS_KEY = "java_args"
BUILD_SCRIPT_PATH_KEY = "build_script_path"
TOOL_OUTPUT_LOCAL = "toolOutput"

RUN_IS_LIBRARY = False
def exit_if_not_library(code: int) -> None:
    if RUN_IS_LIBRARY:
        return
    else:
        sys.exit(code)

DEBUG = False
def debug_print(s: str) -> None:
    debug_print_(s, DEBUG)

def print_usage() -> None:
    print("""Usage:
       [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac
       [--link [contractName:slot=contractName ...]]
       [--verify [contractName:specName ...] (space separated)]
       [--solc SOLC_EXEC (default: solc)] or [--solc_map [name=solc,..]]
       [--settings [flag1,...,k1=v1,...]]
       For example,
       ContractA.sol ContractB.sol --link ContractA:b=ContractB --verify ContractA:verifyingRules.spec --solc solc5
       [--help]
       [--help-advanced]""",
          flush=True)

def print_advanced_usage() -> None:
    print("""Usage:
       If no arguments, read from default.conf
       Otherwise:
       [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac
       [--settings [flag1,...,k1=v1,...]]
       [--cache NAME]
       [--output OUTPUT_FILE_NAME (default: .certora_build)]
       [--output_folder OUTPUT_FOLDER_NAME (default: .certora_config)]
       [--link [contractName:slot=contractName ...]]
       [--address [contractName:address ...] (default: auto-assigned)]
       [--path ALLOWED_PATH (default: $PWD/contracts/)]
       [--packages_path PATH (default: $NODE_PATH)] or [--packages [name=path,...]]
       [--solc SOLC_EXEC (default: solc)] or [--solc_map [name=solc,..]]
       [--solc_args 'SOLC_ARGS' (default: none. wrap in quotes, may need to escape)]
       [--verify [contractName:specName ...] (space separated)]
       [--assert [contractName, ...]]
       [--dont_fetch_sources]
       [--iscygwin]
       [--varmap]
       [--build PATH_TO_BUILD_SCRIPT (default: $CERTORA/certoraBuild.py)]
       [--jar JAR_FULL_PATH (full path to jar including name)]
       [--javaArgs 'JAVA_ARGS']
       [--toolOutput PATH (only in local mode)]
       [--disableLocalTypeChecking]
       [--debug]
       [--help]
       [--staging/cloud [environment] (run on the amazon server, default environment is production)]""",
          flush=True)

def run_cmd(cmd: str, overrideExitcode: bool) -> None:
    try:
        args = prepare_call_args(cmd)
        exitcode = subprocess.call(args, shell=False)
        if exitcode:
            debug_print(str(args))
            print("Failed to run %s, exitcode %d" % (' '.join(args), exitcode), flush=True)
            debug_print("Path is %s" % (os.getenv("PATH"),))
            if not overrideExitcode:
                exit_if_not_library(1)
        else:
            debug_print("Exitcode %d" % (exitcode,))
    except Exception:
        debug_print(str(args))
        #  debug_print(traceback.format_exc())
        print("Failed to run %s" % (cmd,), flush=True)
        debug_print(str(sys.exc_info()))
        exit_if_not_library(1)

"""
    This code parses a settings arg string.
    Commas ',' separate different settings.
    Since commas can appear inside values (like for method choice, '-m'),
    we need to ignore commas that appear within parenthesis.
    It's not a regular property, so we just parse this string.
    This is done by iterating over the characters and maintaining whether we're
    reading the key (assumed that it can't have commas) (IS_KEY),
            the value (which may have commas only within parenthesis) (not IS_KEY),
            in-between (comma for key only, or '=' for key-value properties),
            where we are in the portion (key/value) (idxPortion),
            the current key (KEY) or value (VALUE),
            where we are in the string (idxString),
            how many parenthesis we didn't close yet (COUNT_PAREN)
"""
def parse_settings_arg(settingsArg: str) -> List[str]:
    debug_print("Parsing {}".format(settingsArg))
    COUNT_PAREN = 0
    IS_KEY = True
    idxString = 0
    idxPortion = 0
    KEY = ""
    VALUE = ""
    args_list = []
    while idxString < len(settingsArg):
        ch = settingsArg[idxString]
        # debug_print("handling char {}".format(ch))
        if IS_KEY:
            if ch == '(' or ch == ')':
                print("""Error: Cannot contain parenthesis in key,
                got {} in index {} of {}""".format(ch, idxString, settingsArg))
                exit_if_not_library(1)

            if idxPortion == 0:
                if ch != '-':
                    print("Error: parsing settings {}, expected '-', got {}".format(settingsArg, ch))
                    exit_if_not_library(1)
                KEY = "-"
                idxPortion += 1
                idxString += 1
                continue

            if idxPortion > 0:
                if ch == '=':
                    debug_print("Got key {}".format(KEY))
                    IS_KEY = False
                    idxPortion = 0
                    idxString += 1
                elif ch == ',':
                    KEY += " "
                    # Still key, but no value
                    debug_print("Adding {}".format(KEY))
                    args_list.append(KEY)
                    KEY = ""
                    idxPortion = 0
                    idxString += 1
                else:
                    KEY += ch
                    if idxString + 1 == len(settingsArg):  # finishing
                        debug_print("Adding {}".format(KEY))
                        args_list.append(KEY)
                    idxPortion += 1
                    idxString += 1
            continue

        # Here: is handling VALUE
        if not IS_KEY:
            if ch == '(':
                COUNT_PAREN += 1
            if ch == ')':
                COUNT_PAREN -= 1

            if COUNT_PAREN < 0:
                print("Error: Unbalanced parenthesis in {}".format(settingsArg))
                exit_if_not_library(1)

            if (ch == "," and COUNT_PAREN == 0) or idxString + 1 == len(settingsArg):
                # done with this pair
                if ch != ",":
                    VALUE += ch  # close parenthesis probably

                if COUNT_PAREN > 0:
                    print("Error: Cannot close value {} if parenthesis are unbalanced".format(VALUE))
                    exit_if_not_library(1)

                debug_print("Adding {} {}".format(KEY, VALUE))
                args_list.append("{} {}".format(KEY, VALUE))
                IS_KEY = True
                KEY = ""
                VALUE = ""
                idxPortion = 0
                idxString += 1
            else:
                VALUE += ch
                idxString += 1
                idxPortion += 1

    return args_list

def parse_args(args: List[str]) -> Tuple[List[str], Dict[str, Any], List[str], Dict[str, Any], Dict[str, Any]]:
    run_args = []  # type: List[str]
    build_args = []  # type: List[str]
    script_args = {}  # type: Dict[str, Any]
    timers = {}  # type: Dict[str, Any]
    script_args[JAVA_ARGS_KEY] = ""
    custom_args = {}  # type: Dict[str, Any]

    i = 0

    while i < len(args):
        current_arg = args[i]
        current_potential_value = args[i + 1] if len(args) > i + 1 else None
        if current_arg in VALID_ENVS:  # when it's production --cloud or no flag
            script_args["env"] = current_arg[2:]
            # add branches to the PROD environment
            if (current_arg in ["--staging", "--cloud"] and current_potential_value is not None and not
                    current_potential_value.startswith("-")):
                i += 1
                script_args["branch"] = current_potential_value
        elif current_arg == "--settings":
            i += 1  # inc for the settings
            if current_potential_value is not None:
                settingsList = parse_settings_arg(current_potential_value)
                run_args.extend(settingsList)
                # script_args["settings"] = current_potential_value
                if "settings" in script_args:
                    script_args["settings"].extend(settingsList)
                else:
                    script_args["settings"] = settingsList
            else:
                print("--settings requires an argument", flush=True)
                exit_if_not_library(1)
        elif current_arg == "--jar":
            script_args[JAR_PATH_KEY] = ""
            if current_potential_value and not current_potential_value.startswith("-"):
                script_args[JAR_PATH_KEY] = current_potential_value
                i += 1
        elif current_arg == "--javaArgs":
            if current_potential_value and not current_potential_value.startswith("-"):
                normalized = ''.join(map(lambda x: x.replace("\"", ""), current_potential_value))
                old = script_args[JAVA_ARGS_KEY]
                if old != "":
                    script_args[JAVA_ARGS_KEY] = old + " " + normalized
                else:
                    script_args[JAVA_ARGS_KEY] = normalized
                i += 1
        elif current_arg == "--build":
            i += 1  # inc for the path
            script_args[BUILD_SCRIPT_PATH_KEY] = current_potential_value
        elif current_arg == "--key":
            i += 1
            script_args["key"] = current_potential_value
        elif current_arg == "--toolOutput" and current_potential_value is not None:
            i += 1
            script_args[TOOL_OUTPUT_LOCAL] = current_potential_value
            run_args.extend(["-json", current_potential_value])
        elif current_arg == "--msg" and current_potential_value is not None:
            i += 1
            script_args["msg"] = current_potential_value
            if len(script_args["msg"]) > 100:
                print("Warning: notification message is too long. Only the first 100 characters will be used")
                script_args["msg"] = script_args["msg"][:100]
        elif current_arg in ["--queue_wait_minutes", "--max_poll_minutes", "--log_query_frequency_seconds",
                             "--max_attempts_to_fetch_output", "--delay_fetch_output_seconds"] and \
                current_potential_value is not None:
            i += 1
            try:
                timers[current_arg] = int(current_potential_value)
            except ValueError:
                print("Warning: wrong timer type. Removing {}".format(current_arg), flush=True)
        elif current_arg in ["--disableLocalTypeChecking"]:
            custom_args["disableLocalTypeChecking"] = True
        else:
            build_args.append(current_arg)

        i += 1

    if len(build_args) == 0 or (build_args[0].endswith(".conf") or build_args[0].startswith("--")):
        # No build args (default.conf) or first build arg ends with .conf or starts with -- (an option)
        files = []  # type: List[str]
        fileToContractName = {}  # type: Dict[str, str]
        parsed_options = {"solc": "solc"}

        if len(build_args) == 0:
            conf_file = DEFAULT_CONF
        else:
            conf_file = build_args[0]

        read_from_conf(conf_file, parsed_options, files, fileToContractName)

        if OPTION_CACHE in parsed_options:
            build_args.append("--cache")
            build_args.append(parsed_options[OPTION_CACHE])

    return build_args, script_args, run_args, timers, custom_args


def get_cache_key(args: List[str]) -> Optional[str]:
    if "--cache" in args:
        location_of_cache = args.index("--cache")
        if location_of_cache + 1 >= len(args):
            print("Did not provide cache key", flush=True)
            exit_if_not_library(1)
            return None
        else:
            return args[location_of_cache + 1]
    else:
        return None

def get_cache_param(cache_arg: Optional[str]) -> str:
    if cache_arg is not None:
        return " -cache %s" % cache_arg
    else:
        return ""

def is_tac_file(filename: str) -> bool:
    return filename.endswith(".tac")


def run_local_type_check(args: Dict[str, Any]) -> None:
    # Should even run local type checking? by default yes, but allow opt-out
    if "disableLocalTypeChecking" in args and args["disableLocalTypeChecking"]:
        return

    # Check if java exists on the machine
    java = which("java")
    if java is None:
        return  # if user doesn't have java installed, user will have to wait for remote type checking

    # Find path to typechecker jar
    local_certora_path = sanitize_path(
        os.path.join(os.path.split(__file__)[0], "certora_jars", "Typechecker.jar"))
    installed_certora_path = sanitize_path(
        os.path.join(os.path.split(__file__)[0], "..", "certora_jars", "Typechecker.jar"))
    path_to_typechecker = local_certora_path if os.path.isfile(local_certora_path) else installed_certora_path
    # if typechecker jar does not exist, we just skip this step
    if not os.path.isfile(path_to_typechecker):
        print("Error: Could not run type checker locally", flush=True)
        return

    # args to typechecker
    build_file = CERTORA_BUILD
    verify_file = CERTORA_VERIFY
    debug_print("Path to typechecker is {}".format(path_to_typechecker))
    typecheck_cmd = "java -jar {} {} {}".format(path_to_typechecker, build_file, verify_file)

    # run it - exit with code 1 if failed
    run_cmd(typecheck_cmd, False)


def main_with_args(args: List[str], isLibrary: bool = False, actualResultExpectedPath: str = None) -> None:
    global RUN_IS_LIBRARY
    RUN_IS_LIBRARY = isLibrary
    global DEBUG
    try:
        if len(args) == 0:
            print_usage()
            exit_if_not_library(1)

        if "--debug" in sys.argv:
            DEBUG = True

        nestedOptionHack(args)

        if "--help" in args:
            print_usage()
            exit_if_not_library(1)

        if "--help-advanced" in args:
            print_advanced_usage()
            exit_if_not_library(1)

        check_legal_args(args, legal_run_args)
        build_args, script_args, run_args, timers, custom_args = parse_args(args)

        is_only_tac = is_tac_file(build_args[0])

        cache_arg = get_cache_key(build_args)
        if cache_arg is not None:
            run_args.append(get_cache_param(cache_arg))
            script_args[OPTION_CACHE] = cache_arg

        if BUILD_SCRIPT_PATH_KEY in script_args:
            build_script_path = sanitize_path(script_args[BUILD_SCRIPT_PATH_KEY])
            print("Running with custom build script" + build_script_path)
        else:
            build_script_path = "certoraBuild.py"

        if len(build_args) > 0:
            build_cmd = "%s %s" % (build_script_path, ' '.join(build_args))
        else:
            build_cmd = build_script_path

        # When a TAC file is provided, no build arguments will be processed
        if not is_only_tac:
            print("Building: %s" % (build_cmd,), flush=True)
            if BUILD_SCRIPT_PATH_KEY in script_args:
                run_cmd(build_cmd, False)
            else:
                from certora_cli.certoraBuild import main_with_args  # type: ignore
                main_with_args(build_args, isLibrary)

        defaultPath = "%s/emv.jar" % (sanitize_path(get_certora_root_directory()),)
        if JAR_PATH_KEY in script_args or (os.path.exists(defaultPath) and "env" not in script_args):
            jar_path = (
                script_args[JAR_PATH_KEY] if JAR_PATH_KEY in script_args and script_args[JAR_PATH_KEY]
                else defaultPath)
            if is_only_tac:
                run_args.insert(0, build_args[0])
            if JAVA_ARGS_KEY in script_args:
                java_args = script_args[JAVA_ARGS_KEY]
                check_cmd = " ".join(["java", java_args, "-jar", jar_path] + run_args)
            else:
                check_cmd = " ".join(["java", "-jar", jar_path] + run_args)
            print("Running: %s" % (check_cmd,), flush=True)
            compareWithToolOutput = TOOL_OUTPUT_LOCAL in script_args
            run_cmd(check_cmd, compareWithToolOutput)
            debug_print("Running the verifier like this:\n %s" % (check_cmd,))
            if compareWithToolOutput:
                print("Comparing tool output to expected:")
                result = checkResultsFromFile(script_args[TOOL_OUTPUT_LOCAL])
                if result:
                    exit_if_not_library(0)
                else:
                    exit_if_not_library(1)
        else:
            # In cloud mode, we first run a local type checker
            run_local_type_check(custom_args)
            script_args["buildArgs"] = ' '.join(args)
            if len(timers) > 0:  # at least one timer is supplied
                cv = CloudVerification(timers)
            else:
                cv = CloudVerification()
            result = cv.cliVerify(script_args)
            if result:
                exit_if_not_library(0)
            else:
                exit_if_not_library(1)

    except Exception:
        print("Encountered an error running Certora Prover", flush=True)
        if DEBUG:
            print(traceback.format_exc(), flush=True)
        exit_if_not_library(1)
    except KeyboardInterrupt:
        print('Interrupted', flush=True)

def main() -> None:
    main_with_args(sys.argv[1:])

if __name__ == '__main__':
    main()
