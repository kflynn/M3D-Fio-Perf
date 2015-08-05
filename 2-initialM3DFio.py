#!python

import sys
import re

class Gcode (object):
    layerNum = None

    def __init__(self, line):
        self.layerNum = Gcode.layerNum
        self.codes = []
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

        dataType = 0x1080
        parsed = False
        parameterValue = []
        parameterIdentifier = None

        for i in xrange(16) :
            parameterValue.append(str(""))

        index = 0
        while index <= len(line) :
            # Check if a parameter is detected
            if index == 0 or index == len(line) or (line[index] >= 'A' and line[index] <= 'Z') or line[index] == ';' or line[index] == '*' or line[index] == ' ' :
            
                # Check if a value has been obtained for the parameter
                if index > 0 :
                    # Enforce parameter order as N, M, G, X, Y, Z, E, F, T, S, P, I, J, R, D then string
                    if parameterIdentifier == 'N' :
                    
                        # Set data type
                        dataType |= 1
                        
                        # Store parameter value
                        parameterValue[0] = currentValue
                    
                    elif parameterIdentifier == 'M' :
                    
                        # Set data type
                        dataType |= (1 << 1)
                        
                        # Store parameter value
                        parameterValue[1] = currentValue
                    
                    elif parameterIdentifier == 'G' :
                    
                        # Set data type
                        dataType |= (1 << 2)
                        
                        # Store parameter value
                        parameterValue[2] = currentValue
                    
                    elif parameterIdentifier == 'X' :
                    
                        # Set data type
                        dataType |= (1 << 3)
                        
                        # Store parameter value
                        parameterValue[3] = currentValue
                    
                    elif parameterIdentifier == 'Y' :
                    
                        # Set data type
                        dataType |= (1 << 4)
                        
                        # Store parameter value
                        parameterValue[4] = currentValue
                    
                    elif parameterIdentifier == 'Z' :
                    
                        # Set data type
                        dataType |= (1 << 5)
                        
                        # Store parameter value
                        parameterValue[5] = currentValue
                    
                    elif parameterIdentifier == 'E' :
                    
                        # Set data type
                        dataType |= (1 << 6)
                        
                        # Store parameter value
                        parameterValue[6] = currentValue
                    
                    elif parameterIdentifier == 'F' :
                    
                        # Set data type
                        dataType |= (1 << 8)
                        
                        # Store parameter value
                        parameterValue[7] = currentValue
                    
                    elif parameterIdentifier == 'T' :
                    
                        # Set data type
                        dataType |= (1 << 9)
                        
                        # Store parameter value
                        parameterValue[8] = currentValue
                    
                    elif parameterIdentifier == 'S' :
                    
                        # Set data type
                        dataType |= (1 << 10)
                        
                        # Store parameter value
                        parameterValue[9] = currentValue
                    
                    elif parameterIdentifier == 'P' :
                    
                        # Set data type
                        dataType |= (1 << 11)
                        
                        # Store parameter value
                        parameterValue[10] = currentValue
                    
                    elif parameterIdentifier == 'I' :
                    
                        # Set data type
                        dataType |= (1 << 16)
                        
                        # Store parameter value
                        parameterValue[11] = currentValue
                        
                    
                    elif parameterIdentifier == 'J' :
                    
                        # Set data type
                        dataType |= (1 << 17)
                        
                        # Store parameter value
                        parameterValue[12] = currentValue
                    
                    elif parameterIdentifier == 'R' :
                    
                        # Set data type
                        dataType |= (1 << 18)
                        
                        # Store parameter value
                        parameterValue[13] = currentValue
                    
                    elif parameterIdentifier == 'D' :
                    
                        # Set data type
                        dataType |= (1 << 19)
                        
                        # Store parameter value
                        parameterValue[14] = currentValue
                
                # Reset current value
                currentValue = ""
                
                # Check if a string is required
                if parameterIdentifier == 'M' and (parameterValue[1] == "23" or parameterValue[1] == "28" or parameterValue[1] == "29" or parameterValue[1] == "30" or parameterValue[1] == "32" or parameterValue[1] == "117") :
                
                    # Get string data
                    while index < len(line) and line[index] != ';' and line[index] != '\r' and line[index] != '\n' :
                        currentValue += str(line[index])
                        index += 1
                
                    # Check if a string exists
                    if currentValue != "" :
                
                        # Set data type
                        dataType |= (1 << 15)
                
                        # Store parameter value
                        parameterValue[15] = currentValue
                
                # Check if a comment or checksum is detected
                if index < len(line) and (line[index] == ';' or line[index] == '*') :
        
                    # Stop parsing
                    break
            
                # Set parameter identifier
                if index < len(line) :
                    parameterIdentifier = line[index]
            
            # Otherwise check if value isn't whitespace
            elif line[index] != ' ' and line[index] != '\t' and line[index] != '\r' and line[index] != '\n' :

                # Get current value
                currentValue += str(line[index])
            
            # Increment index
            index += 1

        for i in range(16):
            if parameterValue[i]:
                param = "NMGXYZEFTSPIJRD?"[i]

                self.codes.append("%s%s" % (param, parameterValue[i]))
                self.empty = False

lines = []

for line in open(sys.argv[1], "ru"):
    gcode = Gcode(line)

    if not gcode.empty:
        lines.append(gcode)

for line in lines:
    layerStr = ""

    if line.layerNum is not None:
        layerStr = "(%4d)" % line.layerNum

    print("%-6s %s" % (layerStr, " ".join(line.codes)))


