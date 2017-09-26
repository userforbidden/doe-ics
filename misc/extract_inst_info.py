#bit
#timer
#input/output
#Compare
#Compute
#Mve


import re
inst = []  # (short form of opcode, 2 byte codes, size)

def main():
    f = open("instructionsConfig2.ini", "r")
    for l in f:
        t = filter(None, re.split("=|;|,|\n| ",l))
        if len(t) > 0 and len(t[0]) >= 4:
            if t[0][0] == "[":
                byteCode = ''.join((filter(None, re.split("\[|\]", t[0]))))
            if t[0] == "inscode":
                insCode = t[1]
            if t[0] == "size":
                size = t[1]
                inst.append((insCode, byteCode, size))

    for i in inst:
        print i[0], ",", i[1], ",", i[2]


if __name__ == '__main__':
    main()
