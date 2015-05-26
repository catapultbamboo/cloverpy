import sys
import xml.etree.ElementTree as ET
import argparse

template = """\
<?xml version="1.0"?>
<coverage generated="{timestamp}" clover="3.3">
    <project timestamp="{timestamp}">
        <metrics packages="1" files="{files}" classes="{files}" complexity="0" loc="{loc}" ncloc="{loc}"  elements="{loc}" statements="{loc}" coveredelements="{elements}" coveredstatements="{elements}" coveredconditionals="0" conditionals="0" methods="0" coveredmethods="0"/>
    </project>
</coverage>"""


def convert(coverage_xml):
    tree = ET.parse(coverage_xml).getroot()
    root = tree
    timestamp = root.attrib.get('timestamp')
    files = len(root.findall('.//class'))
    loc = len(root.findall('.//line'))
    elements = len(filter(
        lambda x: x.attrib.get('hits') == '1',
        root.findall('.//line')))
    return template.format(**{
        'timestamp': timestamp,
        'files': files, 'loc': loc,
        'elements': elements})


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
