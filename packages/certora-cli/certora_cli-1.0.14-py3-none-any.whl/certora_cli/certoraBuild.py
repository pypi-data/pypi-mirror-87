#!/usr/bin/env python3

import json
import os
import sys
from Crypto.Hash import keccak
import shutil
import traceback
import re
from collections import OrderedDict
from certora_cli.certoraUtils import debug_print_  # type: ignore
from certora_cli.certoraUtils import safe_create_dir, run_cmd, get_file_basename, get_file_extension, \
    read_from_conf, handle_file_list, current_conf_to_file
from certora_cli.certoraUtils import OPTION_SOLC, OPTION_SOLC_ARGS, OPTION_SOLC_MAP, OPTION_PATH, OPTION_OUTPUT, \
    OPTION_OUTPUT_FOLDER, OPTION_OUTPUT_VERIFY, OPTION_VERIFY, OPTION_ASSERT, OPTION_LINK, OPTION_STRUCT_LINK, \
    OPTION_PACKAGES, \
    OPTION_PACKAGES_PATH, DEFAULT_CONF, OPTION_ADDRESS, OPTION_LINK_CANDIDATES, fatal_error, is_windows, \
    remove_and_recreate_dir, getcwd, as_posix
from certora_cli.certoraUtils import legal_build_args, check_legal_args, nestedOptionHack, sanitize_path

from typing import Any, Dict, List, Tuple, Union


def print_usage() -> None:  # TODO use the macros in print usage as well?
    print("""Usage:
       If no arguments, read from default.conf
       Otherwise:
       [file[:contractName] ...] or CONF_FILE.conf
       [--cache NAME]
       [--output OUTPUT_FILE_NAME (default: .certora_build)]
       [--output_folder OUTPUT_FOLDER_NAME (default: .certora_config)]
       [--link [contractName:slotNumOrFieldName=contractName ...]]
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
       [--debug]
       [--help]""")


BUILD_IS_LIBRARY = False


def is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def exit_if_not_library(code: int) -> None:
    if BUILD_IS_LIBRARY:
        return
    else:
        sys.exit(code)


def fatal_error_if_not_library(msg: str) -> None:
    if BUILD_IS_LIBRARY:
        print(msg)
        raise Exception(msg)
    else:
        fatal_error(msg)


DEBUG = False


def debug_print(s: str) -> None:
    debug_print_(s, DEBUG)


class InputConfig:
    def __init__(self, args: List[str]) -> None:
        self.args = args  # type: List[str]
        self.parsed_options = {"solc": "solc"}  # type: Dict[str, Any]
        self.solc_mappings = {}  # type: Dict[str, str]
        self.files = []  # type: List[str]
        self.fileToContractName = {}  # type: Dict[str, str]
        self.load_input(self.get_options_start_idx(self.get_options()))

    def get_options(self) -> List[Tuple[int, Any]]:
        enumerated_args = [(i, arg) for i, arg in enumerate(self.args)]
        debug_print("Enumerated args %s" % (enumerated_args))
        options = list(filter(lambda x: (x[1].startswith("--")), enumerated_args))
        debug_print("Options indices %s" % (options))
        return options

    @staticmethod
    def get_options_start_idx(options: List[Tuple[int, Any]]) -> int:
        # Figure out indices where there are options
        if len(options) > 0:
            first_option_idx = options[0][0]
        else:
            first_option_idx = -1
        debug_print("First option index is %s" % first_option_idx)
        return first_option_idx

    def load_input(self, first_option_idx: int) -> None:
        if first_option_idx == -1 and len(self.args) == 0:
            debug_print("Will read from default.conf")
            read_from_conf(DEFAULT_CONF, self.parsed_options, self.files, self.fileToContractName)
            print("Building verification environment for files: %s" % (self.files,))
        elif self.args[0].endswith(".conf"):
            if first_option_idx != -1 and len(self.args[:first_option_idx]) != 1:
                fatal_error_if_not_library(
                    "When passing a conf file, can only pass options, not additional files: %s" % (self.args[1:]))
            debug_print("Will read from conf file %s" % (self.args[0]))
            read_from_conf(self.args[0], self.parsed_options, self.files, self.fileToContractName)
            print("Building verification environment for files: %s" % (self.files,))
        else:
            file_list = self.args[0:first_option_idx]
            handle_file_list(file_list, self.files, self.fileToContractName)

            print("Building verification environment for files: %s" % (self.files,))
            # FROM THIS POINT ONWARD, files & fileToContractName DOES NOT CHANGE

        # Process options and override
        self.process_all_options(self.get_options())

        # HANDLE OPTION DEFAULTS
        self.process_defaults()

        # FROM THIS POINT ONWARD, parsed_options and solc_mappings are not changed!

    def update_config(self, name: str, value: Any) -> None:
        self.parsed_options[name] = value

    # Process options - may override those from conf file
    @staticmethod
    def process_option(option: Tuple[int, str], value: Any) -> Tuple[str, str]:
        debug_print("Processing option %s with value %s" % (option, value))
        option_name = option[1][2:]
        # normalize for non-list options
        if option_name in ["solc", "path", "packages_path", "output", "output_folder", "solc_map", "cache"]:
            if len(value) != 1:
                print("Error: option {} should not take more than 1 value, got {}".format(option_name, value))
                print_usage()
                exit_if_not_library(1)
            value = value[0]
        elif option_name in ["packages"]:
            value = ' '.join(value)
        elif option_name in ["address"]:
            def split_tuple(s: str) -> Tuple[str, str]:
                x, y = s.split(":", 2)
                return x, y

            value = dict(map(split_tuple, value))
        elif option_name in [OPTION_ASSERT]:
            if isinstance(value, bool) and value:
                fatal_error_if_not_library("Error: must specify which contract to check assertions for")

        return (option_name, value)

    def process_all_options(self, options: List[Tuple[int, Any]]) -> None:
        for optionIdx, option in enumerate(options):
            debug_print("Working on option %d %s out of %d" % (optionIdx + 1, option, len(options)))
            if optionIdx + 1 < len(options):
                nextOption = options[optionIdx + 1]
                if nextOption[0] == option[0] + 1:
                    self.update_config(*self.process_option(option, True))
                else:
                    optionParams = self.args[option[0] + 1:nextOption[0]]
                    self.update_config(*self.process_option(option, optionParams))
            else:
                if option[0] + 1 < len(self.args):
                    value = self.args[option[0] + 1:]
                    self.update_config(*self.process_option(option, value))
                else:
                    self.update_config(*self.process_option(option, [True]))

        debug_print("Options: %s" % (self.parsed_options))

    def process_defaults(self) -> None:
        # Add default for "output"
        if OPTION_OUTPUT not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT] = ".certora_build"

        # Add default for "output_folder"
        if OPTION_OUTPUT_FOLDER not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT_FOLDER] = ".certora_config"

        if OPTION_OUTPUT_VERIFY not in self.parsed_options:
            self.parsed_options[OPTION_OUTPUT_VERIFY] = ".certora_verify"

        # Add default for "path"
        if OPTION_PATH not in self.parsed_options:
            self.parsed_options[OPTION_PATH] = "%s/contracts/,%s" % (getcwd(), getcwd())
        self.parsed_options[OPTION_PATH] = ','.join(
            [sanitize_path(os.path.abspath(p)) for p in self.parsed_options[OPTION_PATH].split(",")])

        # Add default packages path
        if OPTION_PACKAGES_PATH not in self.parsed_options:
            self.parsed_options[OPTION_PACKAGES_PATH] = \
                os.getenv("NODE_PATH", "%s/node_modules" % (getcwd()))

        # If packages were not specified, try to find them from package.json, if it exists
        if OPTION_PACKAGES not in self.parsed_options:
            try:
                with open("package.json", "r") as package_json_file:
                    package_json = json.load(package_json_file)
                    deps = set(list(package_json["dependencies"].keys()) if "dependencies" in package_json else
                               list(package_json["devDependencies"].keys()) if "devDependencies" in package_json
                               else list())  # May need both
                    # Don't know which ones we need, so we take them all
                    # solidity_deps = [k for k in deps.keys() if k.find("solidity") != -1]
                    # debug_print("Solidity dependencies: %s" % (solidity_deps))

                    packages_path = self.parsed_options[OPTION_PACKAGES_PATH]
                    packages_to_pass_list = ["%s=%s/%s" % (package, packages_path, package) for package in deps]
                    packages_to_pass = ' '.join(packages_to_pass_list)
                    debug_print("Packages to pass: %s" % (packages_to_pass))
                    self.parsed_options[OPTION_PACKAGES] = packages_to_pass
            except EnvironmentError:
                ex_type, ex_value, _ = sys.exc_info()
                debug_print("Failed in processing package.json: %s,%s" % (ex_type, ex_value))

        # Add default for addresses - empty
        if OPTION_ADDRESS not in self.parsed_options:
            self.parsed_options[OPTION_ADDRESS] = {}

        if OPTION_SOLC_MAP in self.parsed_options:
            solcmaps = self.parsed_options[OPTION_SOLC_MAP]
            split = solcmaps.split(",")
            for solcmap in split:
                contract = solcmap.rsplit("=")[0]
                solcver = solcmap.rsplit("=")[1]
                debug_print("Adding solc mapping from %s to %s" % (contract, solcver))
                self.solc_mappings[contract] = solcver

        if OPTION_SOLC_ARGS in self.parsed_options:
            solcargs = self.parsed_options[OPTION_SOLC_ARGS]
            normalized = ' '.join(map(lambda x: x.replace("'", ""), solcargs))
            self.parsed_options[OPTION_SOLC_ARGS] = normalized

    # Utils
    def get_certora_config_dir(self) -> str:
        return self.parsed_options[OPTION_OUTPUT_FOLDER]


class SolidityType:
    def __init__(self,
                 type: str,
                 components: List[Any],  # List[SolidityType]
                 array_dims: List[int],
                 # If this is an array, the i-th element is its i-th dimension size; -1 denotes a dynamic array
                 is_storage: bool,  # Whether it's a storage pointer (only applicable to library functions)
                 is_tuple: bool  # Whether it's a tuple or a struct
                 ):
        self.type = type
        self.components = components
        self.array_dims = array_dims
        self.is_storage = is_storage
        self.is_tuple = is_tuple

    def asdict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "components": [x.asdict() for x in self.components],
            "arrayDims": self.array_dims,
            "isStorage": self.is_storage,
            "isTuple": self.is_tuple
        }

    def __repr__(self) -> str:
        return repr(self.asdict())

    def array_dims_signature(self) -> str:
        return "".join([(lambda x: "[]" if (x == -1) else "[%d]" % x)(dim_size) for dim_size in self.array_dims[::-1]])

    def signature(self) -> str:
        signature_prefix = ("(" + ",".join([x.signature() for x in self.components]) + ")" +
                            self.array_dims_signature()) if self.is_tuple else self.type
        return signature_prefix + (" storage" if self.is_storage else "")


class Func:
    def __init__(self,
                 name: str,
                 args: List[str],
                 fullArgs: List[SolidityType],
                 returns: List[str],
                 sighash: str,
                 notpayable: bool,
                 isABI: bool,
                 stateMutability: Dict[str, str]
                 ):
        self.name = name
        self.args = args
        self.fullArgs = fullArgs
        self.returns = returns
        self.sighash = sighash
        self.notpayable = notpayable
        self.isABI = isABI
        self.stateMutability = stateMutability

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "args": self.args,
            "fullArgs": list(map(lambda x: x.asdict(), self.fullArgs)),
            "returns": self.returns,
            "sighash": self.sighash,
            "notpayable": self.notpayable,
            "isABI": self.isABI,
            "stateMutability": self.stateMutability
        }

    def __repr__(self) -> str:
        return repr(self.asdict())

    def signature(self) -> str:
        return Func.compute_signature(self.name, self.fullArgs)

    @staticmethod
    def compute_signature(
            name: str,
            args: List[SolidityType]
    ) -> str:
        return name + "(" + ",".join([x.signature() for x in args]) + ")"


class ImmutableReference:
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str
                 ):
        self.offset = offset
        self.length = length
        self.varname = varname

    def asdict(self) -> Dict[str, Any]:
        return {
            "offset": self.offset,
            "length": self.length,
            "varname": self.varname
        }

    def __repr__(self) -> str:
        return repr(self.asdict())


class PresetImmutableReference(ImmutableReference):
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str,
                 value: str
                 ):
        ImmutableReference.__init__(self, offset, length, varname)
        self.value = value

    def asdict(self) -> Dict[str, Any]:
        dict = ImmutableReference.asdict(self)
        dict["value"] = self.value
        return dict

    def __repr__(self) -> str:
        return repr(self.asdict())


# Python3.5 to which we maintain backward-compatibility due to CI's docker image, does not support @dataclass
class ContractInSDC:
    def __init__(self,
                 name: str,
                 original_file: str,
                 file: str,
                 address: str,
                 methods: List[Any],
                 bytecode: str,
                 srcmap: str,
                 varmap: Any,
                 linkCandidates: Any,
                 storageLayout: Any,
                 immutables: List[ImmutableReference]
                 ):
        self.name = name
        self.original_file = original_file
        self.file = file
        self.address = address
        self.methods = methods
        self.bytecode = bytecode
        self.srcmap = srcmap
        self.varmap = varmap
        self.linkCandidates = linkCandidates
        self.storageLayout = storageLayout
        self.immutables = immutables

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "original_file": self.original_file,
            "file": self.file,
            "address": self.address,
            "methods": list(map(lambda x: x.asdict(), self.methods)),
            "bytecode": self.bytecode,
            "srcmap": self.srcmap,
            "varmap": self.varmap,
            "linkCandidates": self.linkCandidates,
            "storageLayout": self.storageLayout,
            "immutables": list(map(lambda x: x.asdict(), self.immutables)),
        }

    def __repr__(self) -> str:
        return repr(self.asdict())


class SDC:
    def __init__(self,
                 primary_contract: str,
                 primary_contract_address: str,
                 sdc_origin_file: str,
                 original_srclist: Dict[Any, Any],
                 srclist: Dict[Any, Any],
                 sdc_name: str,
                 contracts: List[ContractInSDC],
                 library_addresses: List[str],
                 generated_with: str,
                 state: Dict[str, str],
                 structLinkingInfo: Dict[str, str]
                 ):
        self.primary_contract = primary_contract
        self.primary_contract_address = primary_contract_address
        self.sdc_origin_file = sdc_origin_file
        self.original_srclist = original_srclist
        self.srclist = srclist
        self.sdc_name = sdc_name
        self.contracts = contracts
        self.library_addresses = library_addresses
        self.generated_with = generated_with
        self.state = state
        self.structLinkingInfo = structLinkingInfo

    def asdict(self) -> Dict[str, Any]:
        return {
            "primary_contract": self.primary_contract,
            "primary_contract_address": self.primary_contract_address,
            "sdc_origin_file": self.sdc_origin_file,
            "original_srclist": self.original_srclist,
            "srclist": self.srclist,
            "sdc_name": self.sdc_name,
            "contracts": list(map(lambda x: x.asdict(), self.contracts)),
            "library_addresses": self.library_addresses,
            "generated_with": self.generated_with,
            "state": self.state,
            "structLinkingInfo": self.structLinkingInfo,
        }


class CertoraBuildGenerator:
    def __init__(self, input_config: InputConfig) -> None:
        self.input_config = input_config
        # SDCs describes the set of all 'Single Deployed Contracts' the solidity file whose contracts comprise a single
        # bytecode of interest. Which one it is - we don't know yet, but we make a guess based on the base filename.
        # An SDC corresponds to a single solidity file.
        self.SDCs = {}  # type: Dict[str, SDC]

        # Note that the the last '/' in config_path is important for solc to succeed, so it should be added
        self.config_path = "%s/%s" % (getcwd(), input_config.get_certora_config_dir())
        self.library_addresses = []  # type: List[str]

        # ASTs will be lazily loaded
        self.asts = {}  # type: Dict[str, Dict[str, Dict[int, Any]]]

        remove_and_recreate_dir(self.config_path)

        self.address_generator_idx = 0

    def collect_array_dims_rec(self, type_str: str, dims: List[int]) -> None:
        outer_dim = re.findall(r"\[\d*\]$", type_str)
        if outer_dim:
            type_rstrip_dim = re.sub(r"\[\d*\]$", '', type_str)
            if len(outer_dim[0]) == 2:
                dims.append(-1)  # dynamic array
            else:
                assert len(outer_dim[0]) > 2, "Expected to find a fixed-size array, but found %s" % type_str
                dims.append(int(re.findall(r"\d+", outer_dim[0])[0]))
            self.collect_array_dims_rec(type_rstrip_dim, dims)

    def collect_array_dims(self, type_str: str) -> List[int]:
        dims = []  # type: List[int]
        self.collect_array_dims_rec(type_str, dims)
        return dims

    # Collects the type of a function parameter from the ABI
    def collect_type(self, typeEntry: Dict[str, Any]) -> Dict[str, Any]:
        if typeEntry["type"].startswith("tuple"):
            is_tuple = True
            assert "components" in typeEntry, "Expected a non-empty tuple, but found %s" % typeEntry["type"]
            components = [self.collect_type(x) for x in typeEntry["components"]]
            assert len(components) >= 1, "Expected a non-empty tuple, but found %s" % typeEntry["type"]
        else:
            is_tuple = False
            components = []
        return {"type": typeEntry["type"], "components": components,
                "arrayDims": self.collect_array_dims(typeEntry["type"]),
                "isStorage": False, "isTuple": is_tuple}

    # Gets the type of a function parameter from the ABI
    def get_solidity_type(self, typeEntry: Dict[str, Any]) -> SolidityType:
        if "components" in typeEntry:
            components = [self.get_solidity_type(x) for x in typeEntry["components"]]
        else:
            components = []

        return SolidityType(
            typeEntry["type"],
            components,
            self.collect_array_dims(typeEntry["type"]),
            False,  # ABI functions cannot have storage parameters
            typeEntry["type"].startswith("tuple")
        )

    def normalize_type(self, typeEntry: Dict[str, Any]) -> str:
        if typeEntry["type"].startswith("tuple"):
            assert "components" in typeEntry, "Expected a non-empty tuple, but found %s" % typeEntry
            return re.sub('^tuple', "(" + ','.join([self.normalize_type(x) for x in typeEntry["components"]]) + ")",
                          typeEntry["type"])
        else:
            return typeEntry["type"]

    def collect_funcs(self, data: Dict[str, Any], contract_file: str, original_file: str) -> List[Func]:
        funcs = []
        abi = data["abi"]  # ["contracts"][contract]["abi"]
        hashes = data["evm"]["methodIdentifiers"]
        debug_print(abi)
        for f in filter(lambda x: x["type"] == "function", abi):
            inputs = f["inputs"]
            inputTypes = [self.normalize_type(x) for x in inputs]
            full_inputTypes = [self.get_solidity_type(x) for x in inputs]
            if "outputs" in f:
                outputs = f["outputs"]
                outputTypes = [json.dumps(self.collect_type(x)) for x in outputs]
            else:
                outputTypes = []
            if "payable" not in f:
                isNotPayable = False
            else:
                isNotPayable = not f["payable"]  # Only if something is definitely non-payable, we treat it as such

            if "stateMutability" not in f:
                stateMutability = "nonpayable"
            else:
                stateMutability = f["stateMutability"]
                # in solc6 there is no json field "payable", so we infer that if stateMutability is view or pure,
                # then we're also non-payable by definition
                # (stateMutability is also a newer field)
                sM = stateMutability  # Linters can be so annoying
                if not isNotPayable and (sM == "view" or sM == "pure" or sM == "nonpayable"):
                    isNotPayable = True  # definitely not payable

            # Nice to have hex too
            base = Func.compute_signature(f["name"], full_inputTypes)
            hash = keccak.new(digest_bits=256)
            hash.update(str.encode(base))
            hex = hash.hexdigest()[0:8]
            funcs.append(
                Func(
                    f["name"],
                    inputTypes,
                    full_inputTypes,
                    outputTypes,
                    hex,
                    isNotPayable,
                    True,
                    {"keyword": stateMutability}
                )
            )

        def get_original_def_node(reference: int) -> Dict[str, Any]:
            original_file_asts = self.asts[original_file]
            for c in original_file_asts:
                if reference in original_file_asts[c]:
                    return original_file_asts[c][reference]
            # error if got here
            fatal_error_if_not_library("Could not find reference AST node {}".format(reference))
            return {}

        # Add funcs from hashes (because of libraries for instance, that have empty ABI but do have hashes.)
        for funcstr, solchash in hashes.items():
            debug_print("Got hash for %s with hash %s" % (funcstr, solchash))
            # We assume funcstr hash structure name(arg,..)
            openParenIdx = funcstr.find("(")
            name = funcstr[0:openParenIdx]

            if funcstr in [x.signature() for x in funcs]:  # if function already appeared in ABI:
                prev_func = [x for x in funcs if x.signature() == funcstr][0]
                debug_print("Found another instance of %s" % (funcstr))
                # Make sure it has the same signature!
                assert prev_func.sighash == solchash, \
                    "There is already a function named %s, args %s (signature %s), " \
                    "hash %s, but found signature %s hash %s" % \
                    (name, prev_func.args, prev_func.signature(), prev_func.sighash, funcstr, solchash)
            else:  # Otherwise, add with available information
                debug_print("Found an instance of %s that did not appear in ABI" % (funcstr))
                # No other way but to got to the AST :((((
                # This is a temporary hack that assumes no tuples in library calls, and uses AST information in a very
                # limited way
                nodes = self.asts[original_file][contract_file]
                funcDef = nodes[list(filter(
                    lambda x: "name" in nodes[x] and nodes[x]["name"] == name and "nodeType" in nodes[x] and nodes[x][
                        "nodeType"] == "FunctionDefinition", nodes))[0]]
                params = [p for p in funcDef["parameters"]["parameters"]]

                def get_solidity_type_from_ast_param(p: Dict[str, Any]) -> SolidityType:
                    p_type = p["typeDescriptions"]["typeString"]
                    is_storage = p["storageLocation"] == "storage"
                    is_user_defined = "typeName" in p and "nodeType" in p["typeName"] and p["typeName"][
                        "nodeType"] == "UserDefinedTypeName"
                    if is_user_defined:
                        orig_user_defined_type = get_original_def_node(p["typeName"]["referencedDeclaration"])
                        is_struct = orig_user_defined_type is not None and "nodeType" in orig_user_defined_type
                        is_struct = is_struct and orig_user_defined_type["nodeType"] == "StructDefinition"
                    else:
                        is_struct = False

                    # For a struct parameter (which is NOT a storage pointer), recursively add a solidity type to its
                    # components list for each of its members.
                    def collect_struct_member_types() -> List[SolidityType]:
                        components = []
                        if is_struct:
                            struct_def_node_id = p["typeName"]["referencedDeclaration"]
                            struct_def_node = get_original_def_node(struct_def_node_id)  # type: Dict[str, Any]
                            assert ("nodeType" in struct_def_node and struct_def_node["nodeType"] == "StructDefinition")

                            if not struct_def_node:
                                fatal_error("Expected to find a definition of {} in the contracts asts".format(
                                    p_type))

                            # Proceed recursively on each member of the struct
                            components.extend(
                                [get_solidity_type_from_ast_param(struct_member) for struct_member in
                                 struct_def_node["members"]])

                        return components

                    if p_type.startswith("enum "):
                        p_type = "uint8"

                    array_dims = self.collect_array_dims(p_type)
                    return SolidityType(p_type, collect_struct_member_types(), array_dims, is_storage,
                                        is_struct)

                solidityTypeArgs = [get_solidity_type_from_ast_param(p) for p in params]
                debug_print(funcDef["name"])
                # Refer to https://github.com/OpenZeppelin/solidity-ast/blob/master/schema.json for more info
                debug_print(funcDef["returnParameters"]["parameters"])
                solidityTypeOuts = [
                    p["typeName"]["name"] if "name" in p["typeName"] else p["typeName"]["typeDescriptions"][
                        "typeIdentifier"] for p in
                    [x for x in funcDef["returnParameters"]["parameters"]]]
                func = Func(
                    funcDef["name"],
                    [],
                    solidityTypeArgs,
                    solidityTypeOuts,
                    solchash,
                    funcDef["stateMutability"] == "nonpayable",
                    False,
                    {"keyword": funcDef["stateMutability"]}
                )
                print("Found an instance of %s that is not part of the ABI, adding: %s" % (funcstr, func))
                funcs.append(
                    func
                )

        return funcs

    def collect_srcmap(self, data: Dict[str, Any]) -> Any:
        return data["evm"]["deployedBytecode"]["sourceMap"]  # data["contracts"][contract]["srcmap-runtime"]

    def collect_varmap(self, contract: str, data: Dict[str, Any]) -> Any:
        return data["contracts"][contract]["local-mappings"]

    def collect_storage_layout(self, data: Dict[str, Any]) -> Any:
        return data.get("storageLayout", None)

    def get_standard_json_data(self, sdc_name: str) -> Dict[str, Any]:
        with open("%s/%s.standard.json.stdout" % (self.config_path, sdc_name)) as standard_json_str:
            json_obj = json.load(standard_json_str)
            return json_obj

    @staticmethod
    def address_as_str(address: Union[str, int]) -> str:
        if isinstance(address, str):
            return address
        return "%0.40x" % (address)

    def find_contract_address_str(self,
                                  contractFile: str,
                                  contractName: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]]) -> str:
        address_and_contracts = [e for e in contracts_with_chosen_addresses
                                 if e[1] == "%s:%s" % (contractFile, contractName)]
        if len(address_and_contracts) == 0:
            msg = "Failed to find a contract named %s in file %s. " \
                  "Please make sure there is a file named like the contract, " \
                  "or a file containing a contract with this name. Available contracts: %s" % \
                  (contractName, contractFile, ','.join(map(lambda x: x[1], contracts_with_chosen_addresses)))
            fatal_error_if_not_library(msg)
        address_and_contract = address_and_contracts[0]
        address = address_and_contract[0]
        contract = address_and_contract[1].split(":")[1]
        debug_print("Custom addresses: %s, looking for a match of %s from %s in %s" %
                    (self.input_config.parsed_options[OPTION_ADDRESS], address_and_contract, contract,
                     self.input_config.parsed_options[OPTION_ADDRESS].keys()))
        if contract in self.input_config.parsed_options[OPTION_ADDRESS].keys():
            address = self.input_config.parsed_options[OPTION_ADDRESS][contract]
        debug_print("Candidate addresses for %s is %s" % (contract, address))
        # Can't have more than one! Otherwise we will have conflicting same address for different contracts
        assert len(set(address_and_contracts)) == 1
        return self.address_as_str(address)

    def collect_and_link_bytecode(self,
                                  contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]],
                                  bytecode: str,
                                  links: Dict[str, Any]
                                  ) -> str:
        debug_print("Working on contract {}".format(contract_name))
        debug_print("Contracts with chosen addresses: %s" %
                    ([("0x%X" % x[0], x[1]) for x in contracts_with_chosen_addresses]))

        if links:
            # links are provided by solc as a map file -> contract -> (length, start)
            # flip the links from the "where" to the chosen contract address (based on file:contract).
            linked_bytecode = bytecode
            replacements = {}
            for link_file in links:
                for link_contract in links[link_file]:
                    for where in links[link_file][link_contract]:
                        replacements[where["start"]] = {"length": where["length"],
                                                        "address": self.find_contract_address_str(
                                                            link_file,
                                                            link_contract,
                                                            contracts_with_chosen_addresses)
                                                        }
            debug_print("Replacements %s" % (replacements))
            where_list = list(replacements.keys())
            where_list.sort()
            where_list.reverse()
            for where in where_list:
                offset = where * 2
                len = replacements[where]["length"] * 2
                addr = replacements[where]["address"]
                debug_print("replacing in {} of len {} with {}".format(offset, len, addr))
                linked_bytecode = "{}{}{}".format(
                    linked_bytecode[0:offset],
                    addr,
                    linked_bytecode[(offset + len):]
                )
                self.library_addresses.append(addr)
            return linked_bytecode

        return bytecode

    def get_relevant_solc(self, contract: str) -> str:
        if contract in self.input_config.solc_mappings:
            base = self.input_config.solc_mappings[contract]
        else:
            base = self.input_config.parsed_options[OPTION_SOLC]
        if is_windows() and not base.endswith(".exe"):
            base = base + ".exe"
        return base

    def get_extra_solc_args(self) -> str:
        if OPTION_SOLC_ARGS in self.input_config.parsed_options:
            return self.input_config.parsed_options[OPTION_SOLC_ARGS]
        else:
            return ""

    # when calling solc with the standard_json api, instead of passing it flags we pass it json
    # to request what we want--currently we only use this to retrieve storage layout as this
    # is the only way to do that, it would probably be good to migrate entirely to this API
    def standard_json(self, contract_file: str, remappings: List[str]) -> Dict[str, Any]:
        sources_dict = {contract_file: {"urls": [contract_file]}}
        solc_args = self.get_extra_solc_args()
        debug_print("Adding solc args {}".format(solc_args))
        settings_dict = {"remappings": remappings,
                         "outputSelection": {
                             "*": {
                                 "*": ["storageLayout", "abi", "evm.deployedBytecode", "evm.methodIdentifiers"],
                                 "": ["id", "ast"]
                             }
                         }
                         }

        def split_arg_hack(arg_name: str, args_: str) -> str:
            return args_.split(arg_name)[1].strip().split(" ")[0].strip()  # String-ops FTW

        EVM_VERSION = "--evm-version"
        OPTIMIZE = "--optimize"
        OPTIMIZE_RUNS = "--optimize-runs"

        if EVM_VERSION in solc_args:
            evmVersion = split_arg_hack(EVM_VERSION, solc_args)
            settings_dict["evmVersion"] = evmVersion
        if OPTIMIZE in solc_args or OPTIMIZE_RUNS in solc_args:
            enabled = OPTIMIZE in solc_args
            if OPTIMIZE_RUNS in solc_args:
                runs = int(split_arg_hack(OPTIMIZE_RUNS, solc_args))
                settings_dict["optimizer"] = {"enabled": enabled, "runs": runs}
            else:
                settings_dict["optimizer"] = {"enabled": enabled}

        result_dict = {"language": "Solidity", "sources": sources_dict, "settings": settings_dict}
        debug_print("Standard json input")
        debug_print(json.dumps(result_dict, indent=4))
        return result_dict

    def get_compilation_path(self, sdc_name: str) -> str:
        return "%s/%s" % (self.config_path, sdc_name)

    def build_srclist(self, data: Dict[str, Any], sdc_name: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        # srclist - important for parsing source maps
        srclist = {data["sources"][k]["id"]: k for k in data["sources"]}
        debug_print("Source list: %s" % (srclist,))

        fetched_srclist = {}

        map_idx_in_src_list_to_orig_file = {v: k for k, v in srclist.items()}
        for orig_file in map_idx_in_src_list_to_orig_file:
            idx_in_src_list = map_idx_in_src_list_to_orig_file[orig_file]
            if "dont_fetch_sources" not in self.input_config.parsed_options:
                # Copy contract_file to compilation path directory
                new_name = "%d_%s.%s" % (idx_in_src_list, get_file_basename(orig_file),
                                         get_file_extension(orig_file))
                shutil.copy2(orig_file,
                             '%s/%s' % (self.get_compilation_path(sdc_name), new_name))
                fetched_source = '%s/%s' % (sdc_name, new_name)
            else:
                fetched_source = orig_file

            fetched_srclist[idx_in_src_list] = fetched_source

        return (srclist, fetched_srclist)

    # This function fetches the AST provided by solc and flattens it so that each node_id is mapped to a dict object,
    # representing the node's contents.
    # contract_sources represents the AST. Every sub-object with an "id" key is an AST node.
    # The ast object is keyed by the original file for which we invoked solc
    def collect_asts(self, original_file: str, contract_sources: Dict[str, Dict[str, Any]]) -> None:
        self.asts[original_file] = {}
        for c in contract_sources:
            debug_print("Adding ast of %s for %s" % (original_file, c))
            container = {}  # type: Dict[int, Any]
            self.asts[original_file][c] = container
            if "ast" not in contract_sources[c]:
                fatal_error_if_not_library(
                    "Invalid AST format for original file %s - got object that does not contain an \"ast\" %s" % (
                        original_file, contract_sources[c]))
            queue = [contract_sources[c]["ast"]]
            while queue:
                pop = queue.pop(0)
                if isinstance(pop, dict) and "id" in pop:
                    container[int(pop["id"])] = pop
                    for key, value in pop.items():
                        if isinstance(value, dict):
                            queue.append(value)
                        if isinstance(value, list):
                            queue.extend(value)

    @staticmethod
    def get_node_from_asts(asts: Dict[str, Dict[str, Dict[int, Any]]], original_file: str, node_id: int) -> Any:
        debug_print("Available keys in ASTs: %s" % (asts.keys()))
        debug_print("Available keys in AST of original file: %s" % (asts[original_file].keys()))
        for contract_file in asts[original_file]:
            node = asts[original_file].get(contract_file, {}).get(node_id)
            if node is not None:
                debug_print("In original %s in contract file %s found for node id %d the node %s" % (
                    original_file, contract_file, node_id, node))
                return node  # Found the ast node of the given node_id
        return {}  # an ast node with the given node_id was not found

    def collect_immutables(self,
                           contract_data: Dict[str, Any],
                           original_file: str
                           ) -> List[ImmutableReference]:
        out = []
        immutableReferences = contract_data["evm"]["deployedBytecode"].get("immutableReferences", [])
        # Collect and cache the AST(s). We collect the ASTs of ALL contracts' files that appear in
        # contract_sources; the reason is that a key of an item in immutableReferences
        # is an id of an ast node that may belong to any of those contracts.
        debug_print("Got immutable references in %s: %s" % (original_file, immutableReferences))
        for astnode_id in immutableReferences:
            astnode = self.get_node_from_asts(self.asts, original_file, int(astnode_id))
            name = astnode.get("name", None)
            if name is None:
                fatal_error_if_not_library(
                    "immutable reference does not point to a valid ast node {} in {}, node id {}".format(
                        astnode,
                        original_file,
                        astnode_id
                    )
                )

            debug_print("Name of immutable reference is %s" % (name))
            for elem in immutableReferences[astnode_id]:
                out.append(ImmutableReference(elem["start"],
                                              elem["length"],
                                              name
                                              )
                           )
        return out

    def address_generator(self) -> int:
        # 12,14,04,06,00,04,10 is 0xce4604a aka certora.
        const = (12 * 2 ** 24 + 14 * 2 ** 20 + 4 * 2 ** 16 + 6 * 2 ** 12 + 0 + 4 * 2 ** 4 + 10 * 2 ** 0)
        address = const * 2 ** 100 + self.address_generator_idx
        # Don't forget for addresses there are only 160 bits
        self.address_generator_idx += 1
        return address

    def collect_for_file(self, file: str, file_index: int) -> SDC:
        primary_contract = self.input_config.fileToContractName[file]
        sdc_name = "%s_%d" % (file.split("/")[-1], file_index)
        compilation_path = self.get_compilation_path(sdc_name)
        safe_create_dir(compilation_path)

        solc_ver_to_run = self.get_relevant_solc(primary_contract)

        file_abs_path = as_posix(os.path.abspath(file))

        packages = self.input_config.parsed_options.get(OPTION_PACKAGES, "").split(" ")
        remappings = sorted(list(filter(lambda package: "=" in package, packages)), key=str.lower)
        paths_for_remappings = map(lambda remap: remap.split("=")[1], remappings)

        # ABI and bin-runtime cmds preparation
        if OPTION_PACKAGES in self.input_config.parsed_options:
            join_remappings = ','.join(paths_for_remappings)
            debug_print("Join remappings: %s" % (join_remappings))
            collect_cmd = "%s -o %s/ --overwrite --allow-paths %s,%s,. --standard-json" % \
                          (solc_ver_to_run, compilation_path, self.input_config.parsed_options[OPTION_PATH],
                           join_remappings)
        else:
            collect_cmd = "%s -o %s/ --overwrite --allow-paths %s,. --standard-json" % \
                          (solc_ver_to_run, compilation_path, self.input_config.parsed_options[OPTION_PATH])

        # Standard JSON

        standard_json_input = json.dumps(self.standard_json(file_abs_path, remappings)).encode("utf-8")
        run_cmd(collect_cmd, "%s.standard.json" % (sdc_name), self.config_path,
                input=standard_json_input, shell=False)

        debug_print("Collecting standard json: %s" % (collect_cmd))
        standard_json_data = self.get_standard_json_data(sdc_name)
        # debug_print("Standard json data")
        # debug_print(json.dumps(standard_json_data, indent=4))

        for error in standard_json_data.get("errors", []):
            # is an error not a warning
            if error.get("severity", None) == "error":
                debug_print("Error: standard-json invocation of solc encountered an error: {}"
                            .format(error))
                friendly_message = "Got error from {} of type {}:\n{}".format(solc_ver_to_run,
                                                                              error["type"],
                                                                              error["formattedMessage"])
                fatal_error_if_not_library(friendly_message)

        # load data
        # data = get_combined_json_data(sdc_name)
        data = standard_json_data  # Note we collected for just ONE file
        self.collect_asts(file, data["sources"])
        contracts_with_libraries = {}
        # Need to add all library dependencies that are in a different file:
        seen_link_refs = {file_abs_path}
        contract_work_list = [file_abs_path]
        while (contract_work_list):
            contract_file = contract_work_list.pop()
            contract_list = [c for c in data["contracts"][contract_file]]
            contracts_with_libraries[contract_file] = contract_list

            for contract_name in contract_list:
                contractObject = data["contracts"][contract_file][contract_name]
                linkRefs = contractObject["evm"]["deployedBytecode"]["linkReferences"]
                for linkRef in linkRefs:
                    if (linkRef not in seen_link_refs):
                        contract_work_list.append(linkRef)
                        seen_link_refs.add(linkRef)

        debug_print("Contracts in %s: %s" % (sdc_name, contracts_with_libraries[file_abs_path]))

        contracts_with_chosen_addresses = \
            [(self.address_generator(), "%s:%s" % (contract_file, contract_name)) for contract_file, contract_list in
             contracts_with_libraries.items() for contract_name in contract_list]  # type: List[Tuple[int, Any]]

        debug_print("Contracts with their chosen addresses: %s" % (contracts_with_chosen_addresses,))

        srclist, fetched_srclist = self.build_srclist(data, sdc_name)
        fetched_source = fetched_srclist[[idx for idx in srclist if srclist[idx] == contract_file][0]]
        contracts_in_sdc = []
        debug_print("finding primary contract address of %s:%s in %s" %
                    (file_abs_path, primary_contract, contracts_with_chosen_addresses))
        primary_contract_address = \
            self.find_contract_address_str(file_abs_path,
                                           primary_contract,
                                           contracts_with_chosen_addresses)
        debug_print("For contracts of primary {}".format(primary_contract))

        for contract_file, contract_list in contracts_with_libraries.items():
            for contract_name in contract_list:
                contract_in_sdc = self.get_contract_in_sdc(
                    contract_file,
                    contract_name,
                    contracts_with_chosen_addresses,
                    data,
                    fetched_source,
                    primary_contract,
                    file
                )
                contracts_in_sdc.append(contract_in_sdc)

        debug_print("Contracts in SDC %s: %s" % (sdc_name, contracts_in_sdc))
        # Need to deduplicate the library_addresses list without changing the order
        deduplicated_library_addresses = list(OrderedDict.fromkeys(self.library_addresses))
        sdc = SDC(primary_contract,
                  primary_contract_address,
                  file,
                  srclist,
                  fetched_srclist,
                  sdc_name,
                  contracts_in_sdc,
                  deduplicated_library_addresses,
                  ' '.join(sys.argv),
                  {},
                  {})
        self.library_addresses.clear()  # Reset library addresses
        return sdc

    def get_contract_in_sdc(self,
                            contract_file: str,
                            contract_name: str,
                            contracts_with_chosen_addresses: List[Tuple[int, Any]],
                            data: Dict[str, Any],
                            fetched_source: str,
                            primary_contract: str,
                            original_file: str
                            ) -> ContractInSDC:
        contract_data = data["contracts"][contract_file][contract_name]
        debug_print("Name,File of contract: %s, %s" % (contract_name, contract_file))
        funcs = self.collect_funcs(contract_data, contract_file, original_file)
        debug_print("Functions of %s: %s" % (contract_name, funcs))
        srcmap = self.collect_srcmap(contract_data)
        debug_print("Source maps of %s: %s" % (contract_name, srcmap))
        if "varmap" in self.input_config.parsed_options:
            varmap = self.collect_varmap(contract_name, data)
            debug_print("Variable mappings of %s: %s" % (contract_name, varmap))
        else:
            varmap = ""
        bytecode_ = contract_data["evm"]["deployedBytecode"]["object"]
        bytecode = self.collect_and_link_bytecode(contract_name,
                                                  contracts_with_chosen_addresses,
                                                  bytecode_,
                                                  contract_data["evm"]["deployedBytecode"]["linkReferences"]
                                                  )
        if contract_name == primary_contract and len(bytecode) == 0:
            fatal_error_if_not_library("Error: Contract {} has no bytecode - is it abstract?"
                                       .format(contract_name))
        debug_print("linked bytecode for %s: %s" % (contract_name, bytecode))
        address = self.find_contract_address_str(contract_file,
                                                 contract_name,
                                                 contracts_with_chosen_addresses)
        storage_layout = \
            self.collect_storage_layout(contract_data)
        immutables = self.collect_immutables(contract_data, original_file)
        if OPTION_LINK_CANDIDATES in self.input_config.parsed_options:
            if contract_name in self.input_config.parsed_options[OPTION_LINK_CANDIDATES]:
                linkCandidates = self.input_config.parsed_options[OPTION_LINK_CANDIDATES][contract_name]
            else:
                linkCandidates = {}
        else:
            linkCandidates = {}
        return ContractInSDC(contract_name,
                             contract_file,
                             fetched_source,
                             address,
                             funcs,
                             bytecode,
                             srcmap,
                             varmap,
                             linkCandidates,
                             storage_layout,
                             immutables
                             )

    @staticmethod
    def get_sdc_key(contract: str, address: str) -> str:
        return "%s_%s" % (contract, address)

    @staticmethod
    def get_primary_contract_from_sdc(contracts: List[ContractInSDC], primary: str) -> List[ContractInSDC]:
        return [x for x in contracts if x.name == primary]

    def build(self) -> None:
        for i, f in enumerate(self.input_config.files):
            sdc = self.collect_for_file(f, i)

            # First, add library addresses as SDCs too (they should be processed first)
            debug_print("Libraries to add %s" % sdc.library_addresses)
            for library_address in sdc.library_addresses:
                library_contract_candidates = [contract for contract in sdc.contracts
                                               if contract.address == library_address]
                if len(library_contract_candidates) != 1:
                    fatal_error_if_not_library("Error: Expected to have exactly one library address for {}, got {}"
                                               .format(library_address, library_contract_candidates))

                library_contract = library_contract_candidates[0]
                debug_print("Found library contract %s" % (library_contract))
                # TODO: What will happen with libraries with libraries?
                sdc_lib = SDC(library_contract.name,
                              library_address,
                              library_contract.original_file,
                              sdc.original_srclist,
                              sdc.srclist,
                              "%s_%s" % (sdc.sdc_name, library_contract.name),
                              self.get_primary_contract_from_sdc(sdc.contracts, library_contract.name),
                              [],
                              sdc.generated_with,
                              {},
                              {})
                self.SDCs[self.get_sdc_key(sdc_lib.primary_contract, sdc_lib.primary_contract_address)] = sdc_lib

            # Filter out irrelevant contracts, now that we extracted the libraries, leave just the primary
            sdc.contracts = self.get_primary_contract_from_sdc(sdc.contracts, sdc.primary_contract)
            self.SDCs[self.get_sdc_key(sdc.primary_contract, sdc.primary_contract_address)] = sdc
        self.handle_links()
        self.handle_struct_links()

    def handle_links(self) -> None:
        # Link processing
        if OPTION_LINK in self.input_config.parsed_options:
            links = self.input_config.parsed_options[OPTION_LINK]
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(
                        "Not expecting to find multiple SDC matches {} for {}".format(sources_to_update, src_contract))
                if len(sources_to_update) == 0:
                    fatal_error("No contract to link to with the name {}".format(src_contract))
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    dst_address = dst  # Actually, just a number

                # Decide how to link
                matching_immutable = list({(c, x.varname) for c in self.SDCs[source_to_update].contracts for x in
                                           c.immutables
                                           if
                                           x.varname == reference_to_replace_with_link and c.name == src_contract})
                if len(matching_immutable) > 1:
                    fatal_error(
                        "Not expecting to find multiple immutables with the name {}, got matches {}".format(
                            reference_to_replace_with_link, matching_immutable)
                    )
                """
                Three kinds of links, resolved in the following order:
                1. Immutables. We expect at most one pair of (src_contract, immutableVarName) that matches
                2. Field names. Allocated in the storage - we fetch their slot number. (TODO: OFFSET)
                3. Slot numbers in EVM. Requires knowledge about the Solidity compilation. (TODO: OFFSET)
                """
                debug_print("Candidate immutable names: {}".format(matching_immutable))
                debug_print("Reference to replace with link: {}".format(reference_to_replace_with_link))
                if len(matching_immutable) == 1 and reference_to_replace_with_link == matching_immutable[0][1]:
                    contract_match = matching_immutable[0][0]

                    def map_immut(immutable_reference: ImmutableReference) -> ImmutableReference:
                        if immutable_reference.varname == reference_to_replace_with_link:
                            return PresetImmutableReference(
                                immutable_reference.offset,
                                immutable_reference.length,
                                immutable_reference.varname,
                                dst_address
                            )
                        else:
                            return immutable_reference

                    contract_match.immutables = [map_immut(immutable_reference) for immutable_reference in
                                                 contract_match.immutables]

                    continue
                elif not reference_to_replace_with_link.isnumeric():
                    # We need to convert the string to a slot number
                    resolved_src_slot = self.resolve_slot(src_contract, reference_to_replace_with_link)
                else:
                    resolved_src_slot = reference_to_replace_with_link
                debug_print("Linking slot %s of %s to %s" % (resolved_src_slot, src_contract, dst))
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print("Linking %s (%s) to %s in slot %s" %
                            (src_contract, source_to_update, dst_address, resolved_src_slot))
                self.SDCs[source_to_update].state[resolved_src_slot] = dst_address

    def handle_struct_links(self) -> None:
        # struct link processing
        if OPTION_STRUCT_LINK in self.input_config.parsed_options:
            debug_print('handling struct linking')
            links = self.input_config.parsed_options[OPTION_STRUCT_LINK]
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(
                        "Not expecting to find multiple SDC matches {} for {}".format(sources_to_update, src_contract))
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    dst_address = dst  # Actually, just a number

                debug_print("STRUCT Reference to replace with link: {}".format(reference_to_replace_with_link))

                if not is_hex(reference_to_replace_with_link):
                    # We need to convert the string to a slot number
                    fatal_error_if_not_library("error: struct link slot '%s' not a hexadecimal number" %
                                               reference_to_replace_with_link)
                else:
                    resolved_src_slot = reference_to_replace_with_link
                debug_print("STRUCT Linking slot %s of %s to %s" % (resolved_src_slot, src_contract, dst))
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print("STRUCT Linking %s (%s) to %s in slot %s" %
                            (src_contract, source_to_update, dst_address, resolved_src_slot))
                self.SDCs[source_to_update].structLinkingInfo[resolved_src_slot] = dst_address

    def has_sdc_name_from_SDCs_starting_with(self, potential_contract_name: str) -> bool:
        candidates = self.get_matching_sdc_names_from_SDCs(potential_contract_name)
        return len(candidates) > 0

    def get_one_sdc_name_from_SDCs(self, contract: str) -> str:
        return [k for k, v in self.SDCs.items() if k.startswith("%s_00000000ce4604a" % (contract,))][0]

    def get_matching_sdc_names_from_SDCs(self, contract: str) -> List[str]:
        return [k for k, v in self.SDCs.items() if k.startswith("%s_00000000ce4604a" % (contract,))]

    # Returns the resolved slot number as hex without preceding 0x
    def resolve_slot(self, primary_contract: str, slot_name: str) -> str:
        # TODO: Don't run this command every time
        debug_print("Resolving slots for %s out of %s" % (primary_contract, self.SDCs.keys()))
        sdc = self.SDCs[self.get_one_sdc_name_from_SDCs(primary_contract)]  # Enough to pick one
        file = sdc.sdc_origin_file
        solc_ver_to_run = self.get_relevant_solc(primary_contract)
        solc_add_extra_args = self.get_extra_solc_args()

        if OPTION_PACKAGES in self.input_config.parsed_options:
            asm_collect_cmd = "%s %s -o %s/ --overwrite --asm --allow-paths %s %s %s" % \
                              (solc_ver_to_run, solc_add_extra_args, self.config_path,
                               self.input_config.parsed_options[OPTION_PATH],
                               self.input_config.parsed_options[OPTION_PACKAGES], file)
        else:
            asm_collect_cmd = "%s %s -o %s/ --overwrite --asm --allow-paths %s %s" % \
                              (solc_ver_to_run, solc_add_extra_args, self.config_path,
                               self.input_config.parsed_options[OPTION_PATH], file)
        run_cmd(asm_collect_cmd, "%s.asm" % (primary_contract), self.config_path, shell=False)
        with open("%s/%s.evm" % (self.config_path, primary_contract), "r") as asm_file:
            debug_print("Got asm %s" % (asm_file))
            saw_match = False
            candidate_slots = []
            for line in asm_file:
                if saw_match:
                    candidate_slots.append(line)
                    saw_match = False
                else:
                    regex = r'/\* "[a-zA-Z0-9./_\-:]+":[0-9]+:[0-9]+\s* %s \*/' % (slot_name,)
                    saw_match = re.search(regex, line) is not None
                    if saw_match:
                        debug_print("Saw match for %s on line %s" % (regex, line))
            debug_print("Candidate slots: %s" % (candidate_slots))
            normalized_candidate_slots = [x.strip() for x in candidate_slots]
            debug_print("Candidate slots: %s" % (normalized_candidate_slots))
            filtered_candidate_slots = [x for x in normalized_candidate_slots if x.startswith("0x")]
            set_candidate_slots = set(filtered_candidate_slots)
            debug_print("Set of candidate slots: %s" % (set_candidate_slots))
            if len(set_candidate_slots) == 1:
                # Auto detect base (should be 16 though thanks to 0x)
                slot_number = hex(int(list(set_candidate_slots)[0], 0))[2:]
                debug_print("Got slot number %s" % (slot_number))
            else:
                raise Exception("Failed to resolve slot for %s in %s, valid candidates: %s" %
                                (slot_name, primary_contract, set_candidate_slots))

        return slot_number


class CertoraVerifyGenerator:
    def __init__(self, build_generator: CertoraBuildGenerator):
        self.build_generator = build_generator
        self.input_config = build_generator.input_config
        self.certora_verify_struct = []
        self.verify = {}  # type: Dict[str, List[str]]
        if OPTION_VERIFY in self.input_config.parsed_options or OPTION_ASSERT in self.input_config.parsed_options:
            if OPTION_VERIFY in self.input_config.parsed_options:
                verification_queries = self.input_config.parsed_options[OPTION_VERIFY]
                for verification_query in verification_queries:
                    vq_contract, vq_spec = verification_query.split(":", 2)
                    vq_spec = as_posix(os.path.abspath(vq_spec))  # get full abs path
                    if self.verify.get(vq_contract, None) is None:
                        self.verify[vq_contract] = []
                    self.verify[vq_contract].append(vq_spec)
                    self.certora_verify_struct.append(
                        {"type": "spec",
                         "primary_contract": vq_contract,
                         "specfile": self.get_path_to_spec(vq_contract, vq_spec)}
                    )

            if OPTION_ASSERT in self.input_config.parsed_options:
                for contractToCheckAssertsFor in self.input_config.parsed_options[OPTION_ASSERT]:
                    self.certora_verify_struct.append(
                        {"type": "assertion",
                         "primary_contract": contractToCheckAssertsFor}
                    )

        else:
            # if no --verify or --assert, remove verify json file
            try:
                os.remove('%s.json' % (self.input_config.parsed_options[OPTION_OUTPUT_VERIFY]))
            except OSError:
                pass

    def get_spec_idx(self, contract: str, spec: str) -> int:
        return self.verify[contract].index(spec)

    def get_path_to_spec(self, contract: str, spec: str) -> str:
        spec_basename = get_file_basename(spec)
        return "%s/%d_%s.spec" % (self.input_config.get_certora_config_dir(),
                                  self.get_spec_idx(contract, spec),
                                  spec_basename)

    def copy_specs(self) -> None:
        for contract, specs in self.verify.items():
            for spec in specs:
                shutil.copy2(spec, self.get_path_to_spec(contract, spec))

    def check(self) -> None:
        for contract in self.verify:
            if len(self.build_generator.get_matching_sdc_names_from_SDCs(contract)) == 0:
                fatal_error_if_not_library("Error: Could not find contract %s in contracts [%s]" %
                                           (contract, ','.join(map(lambda x: x[1].primary_contract,
                                                                   self.build_generator.SDCs.items())))
                                           )

    def dump(self) -> None:
        with open('%s.json' % (self.input_config.parsed_options[OPTION_OUTPUT_VERIFY]), 'w+') as output_file:
            json.dump(self.certora_verify_struct, output_file, indent=4, sort_keys=True)


def main_with_args(args: List[str], isLibrary: bool = False) -> None:
    global BUILD_IS_LIBRARY
    BUILD_IS_LIBRARY = isLibrary
    global DEBUG

    try:
        if "--help" in args:
            print_usage()
            exit_if_not_library(1)

        if "--debug" in args:
            DEBUG = True

        nestedOptionHack(args)
        # Must check legal args after handling the solc args
        check_legal_args(args, legal_build_args)

        input_config = InputConfig(args)

        # Store current options
        current_conf_to_file(input_config.parsed_options, input_config.files, input_config.fileToContractName)

        # Start to collect information from solc
        certora_build_generator = CertoraBuildGenerator(input_config)
        certora_build_generator.build()

        # if OPTION_ADDRESS in parsed_options:
        #     manual_addresses = parsed_options[OPTION_ADDRESS]
        #     for address_assignment in manual_addresses:
        #         contract,address = address_assignment.split(":",2)
        #         debug_print("Setting address of %s to %s" %(contract,address))
        #         contracts_to_update = get_matching_sdc_names_from_SDCs(contract)
        #         for contract_to_update in contracts_to_update:
        #             debug_print("Setting address of %s (%s) to address %s" % (contract_to_update, contract, address))
        #             SDCs[contract_to_update]["address"] = address

        # Build certora_verify
        certora_verify_generator = CertoraVerifyGenerator(certora_build_generator)
        certora_verify_generator.check()
        certora_verify_generator.copy_specs()
        certora_verify_generator.dump()

        # Output
        if OPTION_OUTPUT in input_config.parsed_options:  # will never be false because of default
            with open('%s.json' % (input_config.parsed_options[OPTION_OUTPUT]), 'w+') as output_file:
                json.dump({k: v.asdict() for k, v in certora_build_generator.SDCs.items()},
                          output_file,
                          indent=4,
                          sort_keys=True)
        else:
            print("SDCs:")
            print(certora_build_generator.SDCs)

    except Exception:
        print("Encountered an error configuring the verification environment:")
        print(traceback.format_exc())
        print_usage()
        exit_if_not_library(1)


def main() -> None:
    main_with_args(sys.argv[1:])


if __name__ == '__main__':
    main()
