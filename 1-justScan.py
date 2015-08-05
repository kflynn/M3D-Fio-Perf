#!python

import sys
import re

reCode = re.compile(r'([A-Z]\d+(?:\.\d+)?)')

class Gcode (object):
    layerNum = None

    def __init__(self, line):
        self.layerNum = Gcode.layerNum
        self.codes = None
        self.empty = True

        self.parse(line)

    def parse(self, line):
        # Ditch any comment...
        commentStart = line.find(';')

        if commentStart >= 0:
            # Remember if this mentions a layer number...
            if line[commentStart:].startswith(';LAYER:'):
                self.layerNum = int(line[commentStart + 7:])
                Gcode.layerNum = self.layerNum

            # ...and then ditch the comment.
            line = line[:commentStart]

        # ...then ditch leading and trailing whitespace...
        line = line.strip().upper()

        # ...then ditch empty lines.
        if not line:
            next

        self.codes = reCode.findall(line)

        if self.codes:
            self.empty = False

lines = []

for line in open(sys.argv[1], "ru"):
    gcode = Gcode(line)

    if not gcode.empty:
        lines.append(gcode)

for i in range(50):
    layerStr = ""

    if lines[i].layerNum is not None:
        layerStr = "(%4d)" % lines[i].layerNum

    print("%-6s %s" % (layerStr, " ".join(lines[i].codes)))

