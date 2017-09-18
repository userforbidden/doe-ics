import pyshark
import filecap_up
import sys, os
import shutil

class extractor():
    def __init__(self):
        pass
    def extract_from_pcap(self, capturefile, outPath):
        cap = pyshark.FileCapture(capturefile)
        cap.apply_on_packets(filecap_up.get_enip_packets, timeout=100)

        print "Number of communication pair: ", len(filecap_up.net_addr)
        
        for comm_num in range(len(filecap_up.net_addr)):
            allpkts = filecap_up.allpkts[comm_num]
            net_addr = filecap_up.net_addr[comm_num]

            pkt_count = len(allpkts)
            
            # ip_src (eth_src)  <-----> ip_dst (eth_dst)
            print "{0} ({1}) <-----> {2} ({3}) ".format(net_addr[2], net_addr[0], net_addr[3], net_addr[1])
            print "packet count: ", pkt_count

            fileTransStart = False

            for i in range(pkt_count):
                if allpkts[i][0] == "0f":       # command
                    if fileTransStart == True:
                        nextFileNum = allpkts[i][6]
                        nextFileType = allpkts[i][7]
                    elif allpkts[i][6:10] == ["00","03","34","00"]:    # Request length of file type 3. this can be considered as a signal of file transfer start.
                        fileTransStart = True
                        nextFileNum = allpkts[i][6]
                        nextFileType = allpkts[i][7]
                elif allpkts[i][0] == "4f":     # reply
                    if fileTransStart == True:  
                        try:
                            filePath = outPath + "/upload" + str(comm_num) + "/file:" + nextFileNum + "-Type:" + nextFileType
                            print filePath
                            if not os.path.exists(os.path.dirname(filePath)):
                                try:
                                    os.makedirs(os.path.dirname(filePath))
                                except OSError as exc:
                                    if exc.errno != errno.EEXIST:
                                        raise
                            try:
                                with open(filePath, 'a') as f:
                                    print str(filePath) + " created"

                                    for byte in allpkts[i][4:]:
                                        f.write(byte.decode('hex'))
                                f.close()
                            except IndexError as ie:
                                print "IndexError"
                                pass
                        except:
                            print "Other Error: ", sys.exc_info()[0]

def main():
    if len(sys.argv) < 2:
        print "Usage pthon extractor_up.py capturefile "
        print " Capture File is the Network Capture"
        sys.exit()
    else:
        capturefile = str(os.path.abspath(sys.argv[1])) 
        outPath = capturefile.split(".")[0] + "res"
        if os.path.isdir(outPath):
            print "Result directory exist. Removing and recreating"
            shutil.rmtree(outPath)
        else:
            print "Result Directory doesn't exist. Creating " + str(outPath)
        dial1 = extractor()
        dial1.extract_from_pcap(capturefile, outPath)

if __name__ == '__main__':
    main()
