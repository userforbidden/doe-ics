import re
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os, fnmatch
import glob
import shutil
import sys
import re

maxWidth = 1000      # Later, calculate dynamically upon the longest rung in the file
rung_left_margin = 70
rung_left_line_len = 25

rung_right_margin = 30
rung_right_line_len = 20

height_offset = Image.open(os.getcwd()+"/symbols/XIC.jpg").size[1]/4

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, operator):
        self.stack.append(operator)

    def pop(self):
        return self.stack.pop()

    def size(self):
        return len(self.stack)

    def top(self):
        return self.stack[-1]

def postfixRung(tokens):
    postfix_rung = []
    
    if len(tokens) == 2:        # the last rung only contains END
        postfix_rung.append(tokens[-1])
    else:
        stack = Stack()
        for i in range(len(tokens)):     
            if tokens[i] == "(":
                stack.push(tokens[i])
            elif tokens[i] == ")":
                for j in range(stack.size()):
                    t = stack.pop()
                    if t == "(":
                        break
                    postfix_rung.append(t)
            elif tokens[i] == "AND" or tokens[i] == "OR" or tokens[i] == "-->":
                if stack.size() != 0:
                    t = stack.top()    
                    if t == "AND" or t == "OR" or tokens[i] == "-->":
                        postfix_rung.append(stack.pop())
                stack.push(tokens[i])
            else:                            # operand       
                postfix_rung.append(tokens[i])

        for i in range(stack.size()):
            postfix_rung.append(stack.pop())

    return postfix_rung

class merge():
    def __init__(self):
        #self.paper = Image.new("L", (maxWidth, 100), "white")
        self.rungImgList = []
        self.rungCnt = 0

    def mergeRungs(self):
        total_height = 0

        for rung in self.rungImgList:
            total_height += rung.size[1]

        paper = Image.new("L", (maxWidth, total_height), "white")

        height_offset=0

        for rung in self.rungImgList:
            paper.paste(rung, (0, height_offset))
            height_offset += rung.size[1]

        # draw vertical line
        draw = ImageDraw.Draw(paper)

        left_a = (rung_left_margin - rung_left_line_len, 0)
        left_b = (rung_left_margin - rung_left_line_len, paper.size[1])
        draw.line((left_a, left_b), width=3)

        right_a = (maxWidth - rung_right_margin + rung_right_line_len, 0)
        right_b = (maxWidth - rung_right_margin + rung_right_line_len, paper.size[1])
        draw.line((right_a, right_b), width=3)       

        #paper.show()
        paper.save(os.getcwd() + "/output.jpg")

    def drawRung(self, rung):
        if (len(rung) == 1):        # the last rung contains only END
            END_img = self.makeInstImage(rung[0])
            rung_img = Image.new("L", (maxWidth, END_img.size[1]), "white")
        
            rung_img.paste(END_img, (maxWidth-END_img.size[0]-rung_right_margin, 0))

            draw = ImageDraw.Draw(rung_img)

            # draw left and right end margin line
            left_a = (rung_left_margin - rung_left_line_len, height_offset)
            left_b = (maxWidth - END_img.size[0] - rung_right_margin, height_offset)
            draw.line((left_a, left_b), width=3)

            right_a = (maxWidth - rung_right_margin, height_offset)
            right_b = (maxWidth - rung_right_margin + rung_right_line_len, height_offset)
            draw.line((right_a, right_b), width=3)

        else:       
            stack = Stack()
            for token in rung:  
                if token == "AND" or token == "OR" or token == "-->":
                    second = stack.pop()
                    first = stack.pop()
                    combined_image = self.combineImages(first, second, token)
                    stack.push(combined_image)
                else:
                    stack.push(self.makeInstImage(token))

            rung_img = stack.pop()

        fonts_path = "/AbyssinicaSIL-R.ttf"
        rungNum_font = ImageFont.truetype(fonts_path, 20)

        draw = ImageDraw.Draw(rung_img)
        draw.text((10, height_offset-10), str(self.rungCnt), 0, font=rungNum_font)

        #rung_img.show()
        self.rungCnt += 1

        self.rungImgList.append(rung_img)

    def makeInstImage(self, inst):
        if inst == "END":
            opcode = inst
            symbolFile = os.getcwd() + "/symbols/" + opcode + ".jpg"
            img = Image.open(symbolFile)

            img = img.resize(tuple(t/2 for t in img.size), Image.LANCZOS)     # NO hard cording => 1/2
        else:
            opcode = inst[0:inst.find("/")]
            operand = inst[inst.find("/")+1:]

            symbolFile = os.getcwd() + "/symbols/" + opcode + ".jpg"
            img = Image.open(symbolFile)

            if opcode == "XIC" or opcode == "XIO" or opcode == "OTE":
                img = img.resize(tuple(t/2 for t in img.size), Image.LANCZOS)     # NO hard cording => 1/2
            elif opcode == "TON":
                img = img.resize(tuple(t/2 for t in img.size), Image.LANCZOS)

            fonts_path = "/AbyssinicaSIL-R.ttf"
            operand_font = ImageFont.truetype(fonts_path, 20)
    #        opcode_font = ImageFont.truetype(fonts_path, 17)

            draw = ImageDraw.Draw(img)

            if opcode == "TON": 
                timer, timerbase, preset, acc = list(filter(lambda x: x!='', re.split("/|\[|]", operand)))
                draw.text((130, 60), timer, (0,0,0), font=operand_font)
                draw.text((130, 90), timerbase, (0,0,0), font=operand_font)
                draw.text((130, 120), preset, (0,0,0), font=operand_font)
                draw.text((130, 150), acc, (0,0,0), font=operand_font)

            else:
                draw.text((22, 2), operand, (0,0,0), font=operand_font)
    #            draw.text((2,50), opcode, (0,0,0), font=opcode_font
    #        img.show()
        return img
            
    def combineImages(self, first, second, connector):
        AND_line_len = 30
        OR_margin = 10

        if connector == "AND":
            new_width = first.size[0] + second.size[0] + AND_line_len
            new_height = max(first.size[1], second.size[1])
            new_img = Image.new("L", (new_width, new_height), "white")

            new_img.paste(first)
            new_img.paste(second, (first.size[0]+AND_line_len, 0))

            a = (first.size[0], height_offset)
            b = (first.size[0]+AND_line_len, height_offset)

            draw = ImageDraw.Draw(new_img)
            draw.line((a,b), width=3)
            
            #new_img.show()

        elif connector == "OR":
            new_width = max(first.size[0], second.size[0])
            new_height = first.size[1] + second.size[1] + OR_margin
            new_img = Image.new("L", (new_width, new_height), "white")

            new_img.paste(first)
            new_img.paste(second, (0, first.size[1]+OR_margin))            

            a = (1, height_offset)
            b = (1, first.size[1]+OR_margin+height_offset)
            draw = ImageDraw.Draw(new_img)
            draw.line((a,b), width=3)

            c = (new_width-1, height_offset)
            d = (new_width-1, first.size[1]+OR_margin+height_offset)
            draw.line((c,d), width=3)


            # When two images have different width: "BELOW CODE NEED TO BE TESTED"
            if (first.size[0] < new_width):
                e = (first.size[0], height_offset)
                f = (new_width, height_offset)
                draw.line((e,f), width=3)

            elif (second.size[0] < new_width):
                e = (second.size[0], first.size[1]+OR_margin+height_offset)
                f = (new_width, first.size[1]+OR_margin+height_offset)
                draw.line((e,f), width=3)

#            new_img.show()

        else:       # "-->"
            new_height = max(first.size[1], second.size[1])
            new_img = Image.new("L", (maxWidth, new_height), "white")
        
            new_img.paste(first, (rung_left_margin, 0))
            new_img.paste(second, (maxWidth-second.size[0]-rung_right_margin, 0))

            draw = ImageDraw.Draw(new_img)

            if (first.size[0] + second.size[0] + rung_left_margin + rung_right_margin >= maxWidth):
                print "Width of rung image exceed or equal to the max width: ", maxWidth

            else:
                a = (rung_left_margin+first.size[0], height_offset)
                b = (maxWidth-second.size[0]-rung_right_margin, height_offset)
                draw.line((a,b), width=3)

            # draw left and right end margin line
            left_a = (rung_left_margin - rung_left_line_len, height_offset)
            left_b = (rung_left_margin, height_offset)
            draw.line((left_a, left_b), width=3)

            right_a = (maxWidth - rung_right_margin, height_offset)
            right_b = (maxWidth - rung_right_margin + rung_right_line_len, height_offset)
            draw.line((right_a, right_b), width=3)

            #new_img.show()
            

        return new_img

def main():
    m = merge()
    arg = sys.argv[1]
    z = open(arg, 'r+')
    runglist = []
    for line in z.readlines():  # listing the lines of text file
        rung = list(filter(lambda x: x != '', [x.strip() for x in line.split(" ")])) 
        runglist.append(rung)

    for rung in runglist:
        postfix_rung = postfixRung(rung[1:])        # 0 index is "Rung-x"
#        print postfix_rung
        m.drawRung(postfix_rung)

    m.mergeRungs()

if __name__ == '__main__':
    main()
