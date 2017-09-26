import sys
import re

class Stack():
    def __init__(self):
        pass
    stack = []

    def push(self, operator):
        self.stack.append(operator)

    def pop(self):
        return self.stack.pop()

    def size(self):
        return len(self.stack)

    def top(self):
        return self.stack[-1]

def parseRung(rung):
    tokens = filter((lambda x: x!='' and x!= ' ' and x!="\n"), re.split(r"(\(|\)| |\n)", rung))
    postfix_rung = []    

    if len(tokens) == 2:        # the last rung only contains END
        postfix_rung.append(tokens[-1])

    else:
        stack = Stack()
        for i in range(1, len(tokens)-4):     # 0 is "Rung-x:", last 4 token is: -->, (, OUTPUT, ) 
            if tokens[i] == "(":
                stack.push(tokens[i])
            elif tokens[i] == ")":
                for j in range(stack.size()):
                    t = stack.pop()
                    if t == "(":
                        break
                    postfix_rung.append(t)
            elif tokens[i] == "AND" or tokens[i] == "OR":
                if stack.size() != 0:
                    t = stack.top()    
                    if t == "AND" or t == "OR":
                        postfix_rung.append(stack.pop())
                stack.push(tokens[i])
            else:                            # operand       
                postfix_rung.append(tokens[i])

        for i in range(stack.size()):
            postfix_rung.append(stack.pop())

        postfix_rung.append(tokens[-2])      # OUTPUT in rung
    return postfix_rung

def draw(prefix_rung_list):
    
    print "\n###### mock DRAWING #####"

    for rung in prefix_rung_list:
        if (len(rung) == 1):    # the last rung only contains END
            print rung[0]

        else:        
            stack = Stack()
            for i in range(len(rung)-1):         # except OUTPUT 
                token = rung[i]
                if token == "AND" or token == "OR":
                    second = stack.pop()
                    first = stack.pop()
                    draw_combined = first + " " + token + " " + second     # need actual drawing
                    stack.push(draw_combined)
                else:
                    stack.push(token)
            print stack.pop(), " --> ", rung[-1]    # rung[-1] is OUTPUT, need actual drawing

def main():
    if len(sys.argv) < 2:
        print "Usage python rungparser.py rungfile"
        sys.exit()
    
    else:
        rf = open(sys.argv[1], 'r')
        postfix_rung_list = []        
        for line in rf:
            postfix_rung_list.append(parseRung(line))

        print "###### postfixed form of rung ######"
        for rung in postfix_rung_list:
            print rung        

        draw(postfix_rung_list)     
    
if __name__ == '__main__':
    main()        

