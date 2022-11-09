from subprocess import call
import os
import time
import pyshark

numOfPackets = 0

def count_pkt(pkt):
    global numOfPackets
    numOfPackets += 1        


def main():
    of = open("performance_extractor.txt", "w")

    for filename in os.listdir(os.getcwd() + "/captures/internet/"):
        if filename.split(".")[-1] == "pcap":
            global numOfPackets
            numOfPackets = 0

            filepath = os.getcwd() + "/captures/internet/" + filename          
            start_time = time.time()
            call(["python", "extractor.py", filepath])
            t = time.time() - start_time

            statinfo = os.stat(filepath)    # file size

            print filename
            cap = pyshark.FileCapture(filepath)
            cap.apply_on_packets(count_pkt, timeout=100)

            string = filename + "," + str(statinfo.st_size) + "," + str(numOfPackets) + "," + str(t) + "\n"
            of.write(string)

    of.close()

if __name__ == '__main__':
    main()
