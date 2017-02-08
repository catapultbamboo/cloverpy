import sys
import xml.etree.ElementTree as ET
import argparse

template = """\
<?xml version="1.0"?>
<coverage generated="{timestamp}" clover="3.3">
    <project timestamp="{timestamp}">
        <metrics packages="{packages}" files="{files}" classes="{files}" complexity="0" loc="{loc}" ncloc="{loc}"  elements="{loc}" statements="{loc}" coveredelements="{elements}" coveredstatements="{elements}" coveredconditionals="0" conditionals="0" methods="0" coveredmethods="0"/>
    </project>
</coverage>"""


def convert(coverage_xml):
    tree = ET.parse(coverage_xml).getroot()
    root = tree
    timestamp = root.attrib.get('timestamp')

    """
    Dictionary in the format
    {
      (str) class_name: {
        (str) line_number: (bool) was_line_hit
      }
    }
    """
    class_files = {}

    # Iterate through all class tags in the XML (some classes may be present multiple times)
    for class_file in root.findall('.//class'):
        filename = class_file.get('name')

        # Initialize class names that haven't been seen before
        if not filename in class_files:
            class_files[filename] = {}

        # Store the class loc coverage dict
        class_coverage = class_files[filename];

        # Iterate over all lines of code for this instance of the class in the XML
        for loc in class_file.findall('.//line'):
            line_number = loc.get('number')

            # Initialize lines in the code that haven't been seen before as not hit
            if not line_number in class_coverage:
                class_coverage[line_number] = False

            # If the line has been hit, mark it as such
            if loc.get('hits') != '0':
                class_coverage[line_number] = True

    # Count the unique lines of code and the number of hit lines of code
    hit_loc = 0
    total_loc = 0
    for class_file in class_files.keys():
        for loc in class_files[class_file].keys():
            total_loc += 1

            if class_files[class_file][loc]:
                hit_loc += 1

    class_file_count = len(class_files)
    package_count = len(root.findall('.//package'))

    return template.format(**{
        'timestamp': timestamp,
        'files': class_file_count, 'packages': package_count,
        'loc': total_loc, 'elements': hit_loc})


def argument_parser():
    parser = argparse.ArgumentParser(
        description='convert a coverage.xml file of coverage to clover format')
    parser.add_argument(
        'coverage', type=argparse.FileType('r'),
        help='name of the coverage xml file')
    parser.add_argument(
        '--clover', '-o', type=argparse.FileType('w'),
        help='name of the clover xml file')
    return parser


def main(argv=None):
    args = argument_parser().parse_args(argv)
    clover_xml = convert(args.coverage)
    if args.clover:
        args.clover.write(clover_xml)
    else:
        sys.stdout.write(clover_xml)

if __name__ == '__main__':
    main()
