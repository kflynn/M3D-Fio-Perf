#!python

import sys
import re

lines = []

class Gcode (object):
    layerNum = None

    def __init__(self, line):
        self.layerNum = Gcode.layerNum
        self.codes = {}
        self.order = []
        self.empty = True
        self.parsedOK = False
        self.errorText = None

        self.parse(line)

    def mkLexer(self, line):
        for c in line:
            yield c

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

        self.lexer = self.mkLexer(line)
        self.buffered = None
        self.chunk = ''

        # print("<<< %s" % line)

        while True:
            if not self.parseElement():
                break

    def nextChar(self):
        if self.buffered:
            c = self.buffered
            self.buffered = None
        else:
            try:
                c = next(self.lexer)
            except StopIteration:
                c = None

        return c

    def pushBack(self, c):
        self.buffered = c

    def parseElement(self):
        cmd = self.nextChar()

        if cmd is None:
            self.finish()
            return

        if not cmd.isalpha() or not cmd.isupper():
            return self.error("need uppercase letter, got " + c)

        num = self.parseNum()

        if num is None:
            return self.error("no integer after %s" % cmd)

        needWhiteSpace = True

        if cmd == 'G':
            # G code.  
            code = "%s%d" % (cmd, num)
            arg = True
        elif cmd == 'M':
            # M code.  Some of these have a magic arg.
            code = "%s%d" % (cmd, num)

            if (num == 23) or (num == 28) or (num == 29) or (num == 30) or (num == 32) or (num == 117):
                # It's magic.  Read the rest of the line.
                arg = self.parseToEOF()

                if not arg:
                    return self.error("no argument for " + code)

                # This does NOT need whitespace.
                needWhiteSpace = False
            else:
                arg = True
        else:
            # Ordinary command.
            code = cmd
            arg = num

        # If we need whitespace, look for it.
        if needWhiteSpace:
            if not self.parseWhiteSpace():
                return self.error("no whitespace after " + code)

        if code in self.codes:
            return self.error("duplicate %s code" % code)

        # print("--- %s %s" % (code, arg))

        self.codes[code] = arg
        self.order.append(code)
        self.empty = False

        return True

    def parseNum(self):
        num = ''

        while True:
            c = self.nextChar()

            if not c:
                break

            if c.isdigit() or (c == '.'):
                num += c
            else:
                self.pushBack(c)
                break

        if len(num) == 0:
            # Oops.
            return None

        return float(num)

    def parseWhiteSpace(self):
        gotSome = False

        while True:
            c = self.nextChar()

            if not c:
                # Treat this as getting some whitespace, simply 'cause it makes
                # end-of-line handling much easier.
                gotSome = True
                break

            if not c.isspace():
                self.pushBack(c)
                break

            gotSome = True

        return gotSome

    def parseToEOF(self):
        gotSome = False

        while True:
            c = self.nextChar()

            if not c:
                break

            gotSome = True

        return gotSome

    def finish(self):
        self.parsedOK = True

    def error(self, msg):
        self.errorText = msg
        self.parsedOK = False
        self.empty = True

        return False

    def __str__(self):
        output = []

        for code in self.order:
            arg = self.codes[code]

            if arg == True:
                output.append(code)
            elif code[0] == 'M':
                output.append("%s %s" % (code, arg))
            else:
                output.append("%s%s" % (code, arg))

        return " ".join(output)

for line in open(sys.argv[1], "ru"):
    gcode = Gcode(line)

    if not gcode.empty:
        lines.append(gcode)

for i in range(10):
    layerStr = ""

    if lines[i].layerNum is not None:
        layerStr = "(%4d)" % lines[i].layerNum

    print("%-6s %s" % (layerStr, lines[i]))
