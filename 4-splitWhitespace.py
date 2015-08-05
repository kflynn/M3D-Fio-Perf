#!python

import sys
import re

reCode = re.compile(r'([A-Z]\d+(?:\.\d+)?)')

class Gcode (object):
    codeOrder = 'NMGXYZEFTSPIJRD'   # except magic M codes come last in ASCII

    validCodes = {
        'N': (1 << 0),
        'M': (1 << 1),
        'G': (1 << 2),
        'X': (1 << 3),
        'Y': (1 << 4),
        'Z': (1 << 5),
        'E': (1 << 6),
        'F': (1 << 8),  # NOT A TYPO.  Yes, we skip 7.
        'T': (1 << 9),
        'S': (1 << 10),
        'P': (1 << 11),
        'I': (1 << 16), # NOT A TYPE.  Yes, we skip 12-15.
        'J': (1 << 17),
        'R': (1 << 18),
        'D': (1 << 19),
    }

    magicMCodes = {
        'M23': True,
        'M28': True,
        'M29': True,
        'M30': True,
        'M32': True,
        'M117': True,
    }

    layerNum = None

    def __init__(self, line):
        self.layerNum = Gcode.layerNum
        self.codes = {}
        self.empty = True
        self.errorText = None
        self.failed = False
        self.stringArg = None

        self.parse(line)

    def parse(self, line):
        if self.failed:
            return

        # Ditch any comment...
        commentStart = line.find(';')

        if commentStart >= 0:
            # Remember if this mentions a layer number...
            if line[commentStart:].startswith(';LAYER:'):
                self.layerNum = int(line[commentStart + 7:])
                Gcode.layerNum = self.layerNum

            # ...and then ditch the comment.
            line = line[:commentStart]

        # # ...then go uppercase...
        # line = line.upper()

        # print("<<< %s" % line)

        # ...and split on whitespace.
        fields = line.split()

        # Ditch empty lines.
        if not fields:
            next

        # Next look at each field.
        
        i = 0

        while i < len(fields):
            field = fields[i][0].upper() + fields[i][1:]

            code = field[0]
            arg = field[1:]

            if field in Gcode.magicMCodes:
                # save the rest of the fields as our arg
                self.stringArg = ' '.join(fields[i+1:])
                i = len(fields)

            # print("--- %s%s%s%s" % 
            #       (code, arg,
            #        " " if (self.stringArg is not None) else "",
            #        self.stringArg if (self.stringArg is not None) else ""))

            if code in self.codes:
                self.error("duplicate %s code" % code)
                break

            self.codes[code] = arg
            self.empty = False

            i += 1

    def error(self, msg):
        self.errorText = msg
        self.failed = True
        self.empty = True

    def __str__(self):
        output = []
        deferred = []

        if self.failed:
            output.append("FAILED")

        for code in Gcode.codeOrder:
            arg = self.codes.get(code, None)

            if arg is not None:
                element = "%s%s" % (code, arg)

                if element in Gcode.magicMCodes:
                    deferred.append(element)
                else:
                    output.append(element)

        if deferred:
            output += deferred

            if self.stringArg:
                output.append(self.stringArg)

        return " ".join(output)

lines = []

for line in open(sys.argv[1], "ru"):
    gcode = Gcode(line)

    if gcode.failed:
        print("ERR %s:\n--- %s" % (gcode.errorText, line))
    elif not gcode.empty:
        lines.append(gcode)

for line in lines:
    layerStr = ""

    if line.layerNum is not None:
        layerStr = "(%4d)" % line.layerNum

    print("%-6s %s" % (layerStr, line))

