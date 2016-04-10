import sys
import codecs

def _raw_bytes_to_str(bytes):
    return ''.join(map(chr, bytes))

PKG_MARKER = _raw_bytes_to_str(codecs.BOM_UTF8)

def usage():
    print('Usage: swf_code_split.py FILE');

def find_class(file):
    CLASS_MARKER_REGEX_STR = '\tpublic (class)|(namespace) (?P=class)'
    for line in file:
        if line.startswith(CLASS_MARKER):
            return line[len(CLASS_MARKER):]
    return None
    
def find_package(file):
    PKG_MARKER_REGEX_STR = 'package (?P=package)'
    return rx.match(PKG_MARKER_REGEX_STR)['package']

def process_file(file):
    print(file.split('\n')[0])

def code_split(path):
    with open(path) as fp:
        contents = fp.read()
        packed_files = contents.split(PKG_MARKER)
        for item in packed_files:
            if len(item.strip())!=0:
                process_file(item)
    return 0

def main():
    if len(sys.argv) != 2:
        usage();
        sys.exit(1)
    else:
        sys.exit(code_split(sys.argv[1]))

if __name__ == '__main__':
    main()