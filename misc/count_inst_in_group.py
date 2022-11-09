#bit
#timer
#input/output
#Compare
#Compute
#Mve


import re
inst = []  # (count, min, max)


group_cnt = 0
inst_cnt = 0
min_size = 100
max_size = 0


def main():
    f = open("instructionsConfig2.ini", "r")
    for l in f:
        global inst_cnt
        global min_size
        global max_size
        global inst
        global group_cnt

        if l[0] == "#" and group_cnt == 0:  
            group_cnt += 1
            pass
        elif l[0] == "#" and group_cnt != 0:
            inst.append((inst_cnt, min_size, max_size))
            inst_cnt = 0
            min_size = 100
            max_size = 0
            group_cnt += 1

        if l[0] == "[":
            inst_cnt+=1

        t = filter(None, re.split("=|;|,|\n| ",l))
        print t
        if len(t) >=2 and t[0] == "size":   
            size = int(t[1])
            if size > max_size:
                max_size = size
            elif size < min_size:
                min_size = size

    inst.append((inst_cnt, min_size, max_size))
    print inst       
    total = 0
    for i in inst:
        total += i[0]
    print total


if __name__ == '__main__':
    main()
