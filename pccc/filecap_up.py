import pyshark
import sys, os
import time

allpkts = []
net_addr = []
#frame_cnt = 0

PCCC_PORT = 44818

def appendPkt(hex_bytes, eth_src, eth_dst, ip_src, ip_dst, tcp_srcport, tcp_dstport):
    addrTup = (eth_src, eth_dst, ip_src, ip_dst)
    addrTup_reverse = (eth_dst, eth_src, ip_dst, ip_src)
    exist = False
    for i in range(len(net_addr)):
        if net_addr[i] == addrTup or net_addr[i] == addrTup_reverse:
            allpkts[i].append(hex_bytes)
            exist = True
            break       
    
    if exist == False:
        if tcp_srcport == PCCC_PORT:
            net_addr.append(addrTup)
        else:
            net_addr.append(addrTup_reverse)
        allpkts.append([hex_bytes])

def get_enip_packets(pkt):
#    time.sleep(0.1)
#    global frame_cnt
#    frame_cnt += 1
#    print frame_cnt
    try:
        # pccc without CIP
        cpfdata = pkt.layers[3].cpf_data  # first cpf_data  

        eth_src = pkt.layers[0].src
        eth_dst = pkt.layers[0].dst
        ip_src = pkt.layers[1].src
        ip_dst = pkt.layers[1].dst

        tcp_srcport = int(pkt.layers[2].srcport)
        tcp_dstport = int(pkt.layers[2].dstport)

        alternatefield = str(cpfdata.alternate_fields)  # second cpf_data
        only_data = alternatefield[28:].split(">]")
        hex_bytes = only_data[0].split(":")
            
        appendPkt(hex_bytes, eth_src, eth_dst, ip_src, ip_dst, tcp_srcport, tcp_dstport)
    
    except AttributeError as e:     # don't have cpf_data field in pkt.layer[3]
        try:
            # pccc with CIP
            cipdata = pkt.layers[5].cip_data

            eth_src = pkt.layers[0].src
            eth_dst = pkt.layers[0].dst
            ip_src = pkt.layers[1].src
            ip_dst = pkt.layers[1].dst

            tcp_srcport = int(pkt.layers[2].srcport)
            tcp_dstport = int(pkt.layers[2].dstport)

            hex_bytes = cipdata.split(":")
            pcccdata = hex_bytes[7:]
            
            appendPkt(pcccdata, eth_src, eth_dst, ip_src, ip_dst, tcp_srcport, tcp_dstport)
        except:
            pass

    except IndexError as e2:
        try_decode_TCP_retrans(pkt)      
        pass
    except:
        print "Other Error: ", sys.exc_info()[0]
        pass

def try_decode_TCP_retrans(pkt):
    try:
        eth_src = pkt.layers[0].src
        eth_dst = pkt.layers[0].dst
        ip_src = pkt.layers[1].src
        ip_dst = pkt.layers[1].dst  

        tcp_srcport = int(pkt.layers[2].srcport)
        tcp_dstport = int(pkt.layers[2].dstport)

        # pccc always use port 44818?
        if tcp_srcport == PCCC_PORT or tcp_dstport == PCCC_PORT:
            # assume AB Micrologix 1400->RSLogix use pccc w/0 cip
            hex_bytes = str(pkt.layers[2].segment_data).split(":")
            pcccdata = hex_bytes[41:]

            appendPkt(pcccdata, eth_src, eth_dst, ip_src, ip_dst, tcp_srcport, tcp_dstport)   
    except:
        pass
