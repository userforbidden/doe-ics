import pyshark
import filecap
import sys, os
import shutil


# if len(sys.argv) < 3 :
# print "Usage python extractor.py capturefile storage path "
# print " Capture File is the Network Capture"
# print " Storage path is where the PLC file dumps are stored"
# sys.exit()
# else:
# capturefile = str(sys.argv[1])
# filepath = str(sys.argv[2])
# print filepath
class extractor():
    def __init__(self):
        pass

    # ready the capture file for analysis
    def extract_from_pcap(self, capturefile, filepath):
        cap = pyshark.FileCapture(capturefile)
        cap.apply_on_packets(filecap.get_enip_packets, timeout=100)

        # incremental variables
        i_0f = i_4f = i_06 = i_46 = i_other = 0

        # declare variables
        pkt_count = len(filecap.allpkts)
        allpkts = filecap.allpkts
        req_pkts = []
        res_pkts = []
        other_cmd_pkts = []
        other_reply_pkts = []
        chng_mode_detect = []
        chng_border = []

        print "pkt_count: ", pkt_count

        # classify packets further as req_pkts:command packets res_pkts:reply packets
        try:
            for i in range(0, pkt_count):
                #          print "Hello again~~~~~~~~~~~~~~~~~"
                if allpkts[i][0] == "0f":  # command packets has 0f in their first field cpf data
                    allpkts[i].insert(0, i_0f)
                    req_pkts.append(allpkts[i])  # command packets are stored to req_pkts
                    i_0f += 1
                #	    print i
                elif allpkts[i][0] == "4f":  # reply packets has 4f in their first field of cpf data
                    allpkts[i].insert(0, i_4f)
                    res_pkts.append(allpkts[i])
                    i_4f += 1
                elif allpkts[i][0] == "06":  # Echo packets
                    allpkts[i].insert(0, i_06)
                    other_cmd_pkts.append(allpkts[i])
                    i_06 += 1
                else:
                    allpkts[i].insert(0, i_46)  # Echo response and other packets
                    other_reply_pkts.append(allpkts[i])
                    i_46 += 1
        except IndexError as e1:
            pass  # Ignore filter unwanted packets

        reqpkt_count = len(req_pkts)

        for j in range(0, reqpkt_count):
            if req_pkts[j][5] == "80":
                print "Mode detect: ", j
                chng_mode_detect.append(req_pkts[j][0])
                print "chng_mode_detect: ", chng_mode_detect

        # Detect both Program mode and Run mode
        if len(chng_mode_detect) == 2:
            print "Mode Change Detected at these request packets      : ",
            chng_border = filecap.borders(chng_mode_detect, 2)
            print chng_border
        # Can't detect mode change -> set the border as the first packet and the last packet
        else:
            print "Fail to find two mode change. Set the border as the first and the last packet: ", 
            chng_mode_detect = []
            chng_mode_detect.append(0)      
            chng_mode_detect.append(reqpkt_count-1)
            chng_border = filecap.borders(chng_mode_detect, 2)
            print chng_border

        for idx in chng_border:
            print "**************************************************\n"
            print "data {} : " + str(idx) + "Size : " + str(idx[1] - idx[0])
            print "**************************************************\n"

        for idx2 in range(idx[0], idx[1] + 1):
            filecap.print_details(req_pkts[idx2], res_pkts[idx2], idx, filepath)
        print "***************************************************\n"


def main():
    # check for command line arguments
    if len(sys.argv) < 2:
        print "Usage python extractor.py capturefile storage path "
        print " Capture File is the Network Capture"
        print " Storage path is where the PLC file dumps are stored"
        sys.exit()
    else:
        capturefile = str(os.path.abspath(sys.argv[1]))
        print capturefile
        # filepath = str(sys.argv[2])
        fileDir = capturefile.split("/")
        filelen = len(fileDir)
        saveDir = ""
        dirName = fileDir[filelen - 1].split(".")
        # print dirName[0]
        for fol in range(1, (filelen - 1)):
            saveDir += "/" + str(fileDir[fol])
        filepath = str(saveDir) + "/" + str(dirName[0]) + "res"
        # print filepath
        if os.path.isdir(filepath):
            print "Result directory exist removing and recreating"
            shutil.rmtree(filepath)
            dial1 = extractor()
            dial1.extract_from_pcap(capturefile, filepath)
        else:
            print "Result Directory Don't exist, Creating and extracting results to " + str(filepath)
            dial1 = extractor()
            dial1.extract_from_pcap(capturefile, filepath)


if __name__ == '__main__':
    main()
