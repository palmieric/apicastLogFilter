#!/usr/bin/python3

import argparse
import sys
from datetime import datetime
from sortedcontainers import SortedDict, SortedList

class DateValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value = datetime.strptime(values, '%Y/%m/%d %H:%M:%S')
        setattr(namespace, self.dest, value)

parser = argparse.ArgumentParser(
    description='Sort and filter an unsorted APICAST log file')
parser.add_argument('-i', '--input', type=str, help='Input file', required=True)
parser.add_argument('-o', '--output', type=str, help='Output file', default=None)
parser.add_argument('-s', '--start', type=str, help='The start of the interval to '
    'extract in the format %%Y/%%m/%%d %%H:%%M:%%S e.g. 2020/01/08 08:30:05', action=DateValidator)
parser.add_argument('-e', '--end', type=str, help='The end of the interval to '
    'extract in the format %%Y/%%m/%%d %%H:%%M:%%S e.g. 2020/01/09 08:30:05', action=DateValidator)

args = parser.parse_args()

s = SortedDict()

#06/Aug/2020:14:15:23 +0000

fmts = ['"%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '[%d/%b/%Y:%H:%M:%S', '"[%d/%b/%Y:%H:%M:%S']

with open(args.input) as f:
    for line in f:
        for fmt in fmts:
            try:
                s[datetime.strptime(line[0:len(datetime.today().strftime(fmt))], fmt)].append(line)
                break
            except ValueError:
                pass
            except KeyError:
                s[datetime.strptime(line[0:len(datetime.today().strftime(fmt))], fmt)] = [line]
                break

keys = (SortedList(s.keys()).irange(args.start, args.end) 
    if args.start else s.keys())

f = open(args.output, 'w') if args.output else sys.stdout 

for k in keys:
    for i in s[k]:
        f.write(i)
f.close()