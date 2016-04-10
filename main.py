import sys
import codecs
import re
import os.path

def _raw_bytes_to_str(bytes):
    return ''.join(map(chr, bytes))

PKG_MARKER = _raw_bytes_to_str(codecs.BOM_UTF8)

def usage():
    print('Usage: swf_code_split.py FILE');

def find_class(file):
    CLASS_MARKER_REGEX_STR = (
        r'\n\s*'
        '(public )?(final )?(dynamic )?'
        '(class |namespace |interface |function )'
        '(?P<class>\w+?)'
        '(\s|\().*\n'
    )
    match = re.search(CLASS_MARKER_REGEX_STR, file)
    if match:
        return match.group('class')
    return None
    
def find_package(file):
    PKG_MARKER_REGEX_STR = (
        r'^package '
        '((?P<package>(\w|\.)+?) )'
        '{\n'
    )
    match = re.match(PKG_MARKER_REGEX_STR, file)
    if match is None:
        return None
    return match.group('package')

def process_file(file):
    return find_package(file), find_class(file)

def create_path(package, klass):
    if package is None:
        path = ''
    else:
        path = package.replace('.', '/')
        path += '/'
    file = klass + '.as'
    return path + file

def make_file_path(path):
    path = os.path.dirname(path)
    if len(path) >= 1 and not os.path.exists(path):
        os.makedirs(path)

def write_file(path, contents):
    for_real = True
    if for_real:
        make_file_path(path)
        with open(path, 'w') as fh:
            fh.write(contents)
    else:
        bytes = str(len(contents)) + ' bytes'
        print('write: ' + path + ' (' + bytes + ')')

def code_split(path):
    with open(path) as fp:
        contents = fp.read()
        packed_files = contents.split(PKG_MARKER)
        for item in packed_files:
            if len(item.strip())!=0:
                package, klass = process_file(item)
                path = create_path(package, klass)
                write_file(path, item)
    return 0

def main():
    if len(sys.argv) != 2:
        usage();
        sys.exit(1)
    else:
        sys.exit(code_split(sys.argv[1]))

if __name__ == '__main__':
    main()