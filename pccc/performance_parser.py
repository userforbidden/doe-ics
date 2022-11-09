from subprocess import call
import os
import time



def main():
    of = open("performance_parser.txt", "w")

    for filename in os.listdir(os.getcwd() + "/captures/internet/"):
        if filename[-3:] == "res":
            path = os.getcwd() + "/captures/internet/" + filename
            filepath = path + "/" + os.listdir(path)[0] + "/file:02-Type:22"        
            #outpath = path + "/" + os.listdir(path)[0] + "/" + filename + ".txt"

            start_time = time.time()
            #call(["python", "fileparse_new.py", "22", filepath, ">", outpath])
            call(["python", "fileparse_new.py", "22", filepath])
            t = time.time() - start_time

            string = filename + "," + str(t) + "\n"
            of.write(string)

    of.close()

if __name__ == '__main__':
    main()
