from .log import setup_logger
import logging
import re
import shutil

logger = logging.getLogger('DSCA')


class Analyzer:
    def __init__(self, file_collection, logger_file, log_tag):
        self.source_type = file_collection.source_type
        self.path = file_collection.path
        self.log_tag = log_tag
        setup_logger(logger_file)
        logger.debug("Scan {}: {}".format(self.source_type, self.path))
        self.files = file_collection.collect_files()
        logger.debug("Found: %s files for analysis." % len(self.files))

    def run(self):
        for file in self.files:
            logger.debug(f'Starting {self.log_tag} for: {file}')
            self.run_file(file)
        pass

    def run_file(self, file):
        pass

    pass


class VerifyAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_verification.log", "verification")
        pass

    def run_file(self, file):
        verify_file(file)
        pass


class FixAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_fixing.log", "fixing")
        pass

    def run_file(self, file):
        fix_file(file)
        pass

    pass


def fix_file(file):
    new_file = fix_file_names(file)
    with open(new_file) as f:
        lines = f.readlines()
        new_lines = []
        need_fixing = False
        for num, code_line in enumerate(lines, start=1):
            if code_line.strip().startswith("//"):
                new_lines.append(code_line)
            else:
                new_code_line = fix_camel_case_types(new_file, num, code_line)
                new_code_line = fix_camel_case_extensions(new_file, num, new_code_line)
                new_code_line = fix_library_prefixes(new_file, num, new_code_line)
                new_code_line = fix_constant_identifier_names(new_file, num, new_code_line)

                new_lines.append(new_code_line)
                if new_code_line != code_line:
                    need_fixing = True

        if need_fixing:
            out = open(re.sub(r'\.dart', "_fix.dart", new_file), "w")
            out.writelines(new_lines)
            out.close()
        else:
            logger.debug(f'{new_file}: no changes.')


def verify_file(file):
    verify_file_names(file)
    with open(file) as f:
        lines = f.readlines()
        for num, code_line in enumerate(lines, start=1):
            if not code_line.strip().startswith("//"):
                verify_line_length(file, num, code_line)
                verify_package_imports(file, num, code_line)
                verify_camel_case_types(file, num, code_line)
                verify_camel_case_extensions(file, num, code_line)
                verify_library_names(file, num, code_line)
                verify_library_prefixes(file, num, code_line)
                verify_constant_identifier_names(file, num, code_line)
                verify_curly_braces_in_flow_control_structures(file, num, code_line)
                verify_slash_for_doc_comments(file, num, code_line)
                verify_is_empty_collection(file, num, code_line)
                verify_is_not_empty_iterable(file, num, code_line)
                verify_lib_relative_imports(file, num, code_line)
                verify_adjacent_string_concatenation(file, num, code_line)
                verify_interpolation_to_compose_strings(file, num, code_line)
                verify_unnecessary_brace_in_string_interps(file, num, code_line)
                verify_iterable_where_type(file, num, code_line)
                verify_collection_literals(file, num, code_line)
                verify_init_to_null(file, num, code_line)
                verify_catching_errors(file, num, code_line)
                verify_function_literals_in_foreach_calls(file, num, code_line)
                verify_function_declarations_over_variables(file, num, code_line)
                verify_unnecessary_new(file, num, code_line)
                verify_unnecessary_const(file, num, code_line)
                verify_catches_without_on_clauses(file, num, code_line)


def verify_line_length(file, num, code_line):
    if len(code_line) > 80:
        logger.info(f'{file}: Line:{num} - lines_longer_than_80_chars: Avoid lines longer than 80 characters.')


def verify_package_imports(file, num, code_line):
    match = re.search(r'import\s+\'([^\']*)\'', code_line)
    if match:
        import_name = match.group(1)
        if import_name.find(":") > 0:
            logger.info(f'{file}: Line:{num} - always_use_package_imports: DO avoid relative imports for '
                        f'files in lib/.')


def verify_camel_case_types(file, num, code_line):
    match = re.search(r'(class|typedef)\s+(\w+)(<[^>]*>)?\s*({|extends)', code_line)
    if match:
        class_name = match.group(2)
        if not is_camel_case(class_name):
            logger.info(f'{file}: Line:{num} - camel_case_types: DO name types using UpperCamelCase.')


def fix_camel_case_types(file, num, code_line):
    match = re.search(r'(class|typedef)\s+(\w+)(<[^>]*>)?\s*({|extends)', code_line)
    if match:
        class_name = match.group(2)
        if not is_camel_case(class_name):
            new_class_name = to_camel_case(class_name)
            logger.info(f'{file}: Line:{num} - Class {class_name} updated to CamelCase: {new_class_name}.')
            return re.sub(class_name, new_class_name, code_line)
    return code_line


def verify_camel_case_extensions(file, num, code_line):
    match = re.search(r'extension\s+(\w+)(<[^>]*>)?\s+on', code_line)
    if match:
        extension_name = match.group(1)
        if not is_camel_case(extension_name):
            logger.info(f'{file}: Line:{num} - camel_case_extensions: DO name extensions using UpperCamelCase.')


def fix_camel_case_extensions(file, num, code_line):
    match = re.search(r'extension\s+(\w+)(<[^>]*>)?\s+on', code_line)
    if match:
        extension_name = match.group(1)
        if not is_camel_case(extension_name):
            new_extension_name = to_camel_case(extension_name)
            logger.info(f'{file}: Line:{num} - Extension {extension_name} update to CamelCase {new_extension_name}')
            return re.sub(extension_name, new_extension_name, code_line)
    return code_line


def verify_library_names(file, num, code_line):
    match = re.search(r'library\s+(\w+)\s*;', code_line)
    if match:
        library_name = match.group(1)
        if not is_snake_case(library_name):
            logger.info(f'{file}: Line:{num} - library_names: DO name libraries using lowercase_with_underscores.')


def verify_file_names(file):
    match = re.search(r'(\w+).dart$', file)
    if match:
        file_name = match.group(1)
        if not is_snake_case_full(file_name):
            logger.info(f'{file}: file_names: DO name source files using lowercase_with_underscores.')


def fix_file_names(file):
    match = re.search(r'(\w+).dart$', file)
    if match:
        file_name = match.group(1)
        if not is_snake_case_full(file_name):
            new_file_name = "{0}.dart".format(to_snake_case(file_name))
            new_file_path = re.sub(file_name + r'\.dart', new_file_name, file)
            shutil.copyfile(file, new_file_path)
            logger.info(f'{file}: file_name changed to: {new_file_name}.')
            return new_file_path
    return file


def verify_library_prefixes(file, num, code_line):
    match = re.search(r'import\s+\'[^\']*\'\s+as\s+(\w+)\s*;', code_line)
    if match:
        library_prefix = match.group(1)
        if not is_snake_case(library_prefix):
            logger.info(f'{file}: Line:{num} - library_prefixes: DO use lowercase_with_underscores when specifying a '
                        f'library prefix.')


def fix_library_prefixes(file, num, code_line):
    match = re.search(r'import\s+\'[^\']*\'\s+as\s+(\w+)\s*;', code_line)
    if match:
        library_prefix = match.group(1)
        if not is_snake_case(library_prefix):
            new_library_prefix = to_snake_case(library_prefix)
            logger.info(f'{file}: Line:{num} - Prefix {library_prefix} changed to snake case {new_library_prefix}')
            return re.sub(library_prefix, new_library_prefix, code_line)
    return code_line


def verify_constant_identifier_names(file, num, code_line):
    match = re.search(r'(const|final)\s+(\w+)\s*=', code_line)
    if match:
        constant_name = match.group(2)
        if not is_lower_camel_case(constant_name):
            logger.info(
                f'{file}: Line:{num} - constant_identifier_names: PREFER using lowerCamelCase for constant names')


def fix_constant_identifier_names(file, num, code_line):
    match = re.search(r'(const|final)\s+(\w+)\s*=', code_line)
    if match:
        constant_name = match.group(2)
        if not is_lower_camel_case(constant_name):
            new_constant_name = to_lower_camel_case(constant_name)
            logger.info(f'{file}: Line:{num} - Const {constant_name} changed to snake case {new_constant_name}')
            return re.sub(constant_name, new_constant_name, code_line)
    return code_line


def verify_curly_braces_in_flow_control_structures(file, num, code_line):
    match = re.search(r'if \([^)]*\)\s+(.*)', code_line)
    if match:
        if not match.group(1).startswith("{"):
            check_curly_brace(file, num, match.group(1))
    else:
        match = re.search(r'else\s+(.*)', code_line)
        if match:
            check_curly_brace(file, num, match.group(1))


def check_curly_brace(file, num, line):
    if not line.startswith("{"):
        logger.info(
            f'{file}: Line:{num} - curly_braces_in_flow_control_structures: DO use curly braces for all flow control '
            f'structures.')


def verify_slash_for_doc_comments(file, num, code_line):
    match = re.search(r'/\*\*', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - slash_for_doc_comments: PREFER using /// for doc comments.')


def verify_is_empty_collection(file, num, code_line):
    match = re.search(r'\.length\s*(==|!=)', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - prefer_is_empty: DON\'T use length to see if a collection is empty.')


def verify_is_not_empty_iterable(file, num, code_line):
    match = re.search(r'if\s*\(([^\)]*)\)', code_line)
    if match:
        for statement in re.split(r'(&&|\|\|)', match.group(1)):
            if re.search(r'^\s*!.*isEmpty\s*$', statement):
                logger.info(
                    f'{file}: Line:{num} - prefer_is_not_empty: PREFER x.isNotEmpty to !x.isEmpty for Iterable and '
                    f'Map instances.')


def verify_lib_relative_imports(file, num, code_line):
    match = re.search(r'import\s+\'([^\']*)\'', code_line)
    if match:
        library_name = match.group(1)
        if library_name.startswith("../") and library_name.find("/lib/") > 0:
            logger.info(f'{file}: Line:{num} - avoid_relative_lib_imports: DO avoid relative imports '
                        f'for files in lib/.')


def verify_adjacent_string_concatenation(file, num, code_line):
    match = re.search(r'\'[^\']*\'\s*\+\s*(.*)', code_line)
    if match:
        concatenation_subject = match.group(1)
        if concatenation_subject.startswith("'") or len(concatenation_subject) == 0:
            logger.info(f'{file}: Line:{num} - prefer_adjacent_string_concatenation: DO use adjacent strings '
                        f'to concatenate string literals.')


def verify_interpolation_to_compose_strings(file, num, code_line):
    match = re.search(r'\'[^\']*\'\s*\+\s*(.*)', code_line)
    if match:
        concatenation_subject = match.group(1)
        if not concatenation_subject.startswith("'") and len(concatenation_subject) > 0:
            logger.info(f'{file}: Line:{num} - prefer_adjacent_string_concatenation: PREFER using interpolation '
                        f'to compose strings and values.')


def verify_unnecessary_brace_in_string_interps(file, num, code_line):
    match = re.search(r'\'([^\']*)\'', code_line)
    if match:
        string = match.group(1)
        match = re.search(r'\${([^}]*)}', string)
        if match:
            variable = match.group(1)
            if not variable.find('.') > 0:
                logger.info(f'{file}: Line:{num} - unnecessary_brace_in_string_interps: AVOID using braces in '
                            f'interpolation when not needed.')


def verify_iterable_where_type(file, num, code_line):
    match = re.search(r'\.where\(\(', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - prefer_iterable_whereType: iterable.whereType<T>() over'
                    f' iterable.where((e) => e is T).')


def verify_collection_literals(file, num, code_line):
    if code_line.find("new List();") > 0 \
            or code_line.find("new Map();") > 0 \
            or code_line.find("new Set();") > 0 \
            or code_line.find("new LinkedHashSet();") > 0 \
            or code_line.find("new LinkedHashMap();") > 0:
        logger.info(f'{file}: Line:{num} - prefer_collection_literals: DO use collection literals when possible.')


def verify_init_to_null(file, num, code_line):
    match = re.search(r'\w+\s+\w+\s*=\s*null;', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - avoid_init_to_null: DON\'T explicitly initialize variables to null.')


def verify_catching_errors(file, num, code_line):
    match = re.search(r'\s+on\s+Error\s+catch', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - avoid_catching_errors: DON\'T explicitly catch Error or types '
                    f'that implement it.')


def verify_function_literals_in_foreach_calls(file, num, code_line):
    match = re.search(r'\.forEach\(\s*\(', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - avoid_function_literals_in_foreach_calls: AVOID using '
                    f'forEach with a function literal.')


def verify_function_declarations_over_variables(file, num, code_line):
    match = re.search(r'\w+\s+\w+\s*=\s*\(', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - prefer_function_declarations_over_variables: DO use a function declaration '
                    f'to bind a function to a name.')


def verify_unnecessary_new(file, num, code_line):
    match = re.search(r'=\s*new\s+\w+\(', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - unnecessary_new: AVOID new keyword to create instances.')


def verify_unnecessary_const(file, num, code_line):
    match = re.search(r'=const\s*\w+=\s*const', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - unnecessary_const: AVOID repeating const keyword in a const context.')


def verify_catches_without_on_clauses(file, num, code_line):
    match = re.search(r'on\s*\w+\s+catch', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - avoid_catches_without_on_clauses: AVOID catches without on clauses.')


def is_camel_case(word):
    if re.match(r'^[A-Z]+[a-zA-Z0-9]*$', word):
        return True
    else:
        return False


def is_lower_camel_case(word):
    if re.match(r'^[a-z]+[a-zA-Z0-9]*$', word):
        return True
    else:
        return False


def is_snake_case(word):
    if re.match(r'^[a-z_]+[a-z0-9_]*$', word):
        return True
    else:
        return False


def is_snake_case_full(word):
    if re.match(r'^[a-z0-9_]+$', word):
        return True
    else:
        return False


def to_snake_case(text):
    return re.sub(r'([A-Z])', r'_\1', text).lower()


def to_camel_case(text):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)


def to_lower_camel_case(text):
    new_text = to_camel_case(text)
    return new_text[0].lower() + new_text[1:]
