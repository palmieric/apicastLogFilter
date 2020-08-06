#!/usr/bin/python3

import argparse
from datetime import datetime
from sortedcontainers import SortedDict, SortedList

class DateValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value = datetime.strptime(values, '%Y/%m/%d %H:%M:%S')
        setattr(namespace, self.dest, value)

parser = argparse.ArgumentParser(
    description='Sort and filter an unsorted APICAST log file')
parser.add_argument('--input', type=str, help='Input file', required=True)
parser.add_argument('--out', type=str, help='Output file', default='output.log')
parser.add_argument('--start', type=str, help='The start of the interval to '
    'extract in the format %%Y/%%m/%%d %%H:%%M:%%S e.g. 2020/01/08 08:30:05', action=DateValidator)
parser.add_argument('--end', type=str, help='The end of the interval to '
    'extract in the format %%Y/%%m/%%d %%H:%%M:%%S e.g. 2020/01/09 08:30:05', action=DateValidator)

args = parser.parse_args()

s = SortedDict()

with open(args.input) as f:
    for line in f:
        try:
            s[datetime.strptime(line[1:20], '%Y/%m/%d %H:%M:%S')].append(line)
        except ValueError:
            print("Value removed")
            pass
        except KeyError:
            s[datetime.strptime(line[1:20], '%Y/%m/%d %H:%M:%S')] = [line]

keys = SortedList(s.keys()).irange(args.start, args.end) if args.start else s.keys()



with open(args.out, 'w') as f:
    for k in keys:
        for i in s[k]:
            f.write(i)

print("END")