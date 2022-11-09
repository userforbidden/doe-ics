import pyshark
import sys
import os, errno

# import time	# HY

allpkts = []
frame_cnt = 0


def get_enip_packets(pkt):
    #    print "IN>> get_enip_packets"
    try:
        global frame_cnt
        #        time.sleep(1)
        #        frame_cnt += 1
        #        print "## ", frame_cnt, " ##"
        enip_lay = pkt.layers

        #        print "layer 0: ", enip_lay[0]
        #        print "layer 1: ", enip_lay[1]
        #        print "layer 2: ", enip_lay[2]
        #        print "layer 3: ", enip_lay[3]
        #        print "cpf_data: ", enip_lay[3].cpf_data
        #        sys.exit()

        try:
            cpfdata = enip_lay[3].cpf_data
            alternatefield = str(cpfdata.alternate_fields)

            only_data = alternatefield[28:].split(">]")
            hex_bytes = only_data[0].split(":")
            allpkts.append(hex_bytes)
        except:
            cipdata = enip_lay[5].cip_data
            hex_bytes = cipdata.split(":")
            pcccdata = hex_bytes[7:]
            #            print "===pcccdata", pcccdata
            allpkts.append(pcccdata)

        #	print "## ", frame_cnt, " ##"
    except AttributeError as e:
        # ignore packets that aren't ENIP
        pass
    except IndexError as e2:
        # ignoring out of index packets
        pass


def print_details(a, b, c, filepath):
    try:
        # inspect the packets to determine to which mode it is been changed
        if a[5] == "80" and a[6] == "01":
            print "The PLC is entering Programing mode\n"
        elif a[5] == "80" and a[6] == "06":
            print " PLC is entering back to RUN Mode\n"
        elif a[5] == "aa":
            fn = filepath + "/download-" + str(c) + "/file:" + str(a[7]) + "-Type:" + str(a[8])
            if not os.path.exists(os.path.dirname(fn)):
                try:
                    os.makedirs(os.path.dirname(fn))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            with open(fn, 'a') as filc:
                print str(fn) + " created"
                # when file size is larger than (0xff X 2), context/offset/ack/whatever(?) field size become 3 bytes
                if a[10] == "ff":
                    for ff in a[13:]:
                        filc.write(ff.decode('hex'))      
                else:
                    for ff in a[11:]:
                        filc.write(ff.decode('hex'))
            filc.close()
            # elif a[5] == "8f":
            # print "Applying Port Configuration"
            # elif a[5] == "11":
            # print "Get Edit Resource"
            # elif a[5] == "12":
            # print "Return Edit Resource"
            # elif a[5] == "a2":
            # print "Read Detected"
            # print "Data : ",
            # for ff in b[5:]:
            # print ff,
            # print "  is read from file no " + str(a[7]) + " of file type " + str(a[8])
            # elif a[5] == "52":
            # print "DOWNLOAD COMPLETED"
            # else:
            # print a
            # print b
    except IndexError as ie:
        pass


def borders(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
