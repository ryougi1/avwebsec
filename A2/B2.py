#!/usr/bin/env python

from pcapfile import savefile
import netaddr
import sys

stored_scum = []
unallowed_sets = []
init = False
index = 0

nazir_ip = sys.argv[2]
mix_ip = sys.argv[3]
nr_partners = sys.argv[4]


def create_sets (potential_scum, packets_from_nazir):
    for key in potential_scum:
        if potential_scum[key] == packets_from_nazir:
            stored_scum.append(set(key))

def check_scum (potential_scum, packets_from_nazir):
    matches = []
    found_match = False
    for key in potential_scum:
        if potential_scum[key] == packets_from_nazir:
            print(key)
            matches.append(key)
    for current_set in stored_scum:
        if len(current_set) < nr_partners:
            unallowed_sets.append(matches)
            for match in matches:
                if match in current_set:
                    matches.remove(match)
                    found_match = True

            if found_match == False:
                for match in matches:
                    new_set = set(current_set)
                    new_set.add(match)
                    print(new_set)
                    allowed = True
                    for i in unallowed_sets:
                        if len(new_set.intersection(i)) > 1:
                            allowed = False
                            break
                    if allowed:
                        stored_scum.append(new_set)
                stored_scum.remove(current_set)
            found_match = False





def print_output ():
    if len(stored_scum) == nr_partners:
        ip_sum = 0
        for ip in stored_scum:
            ip_sum += int(netaddr.IPAddress(ip))

    else:
        print(len(stored_scum))

        #for s in stored_scum:
        #    print(s)
        print("FAIL")


testcap = open(sys.argv[1], 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

packets_from_nazir = 0
potential_scum = {}

# print the packets
#print ('timestamp\teth src\t\t\teth dst\t\t\tIP src\t\tIP dst')
for pkt in capfile.packets:
    timestamp = pkt.timestamp
    ip_src = str(pkt.packet.payload.src.decode('UTF8'))
    ip_dst = str(pkt.packet.payload.dst.decode('UTF8'))

    if ip_dst == mix_ip:
        if potential_scum:
            if init:
                check_scum(potential_scum, packets_from_nazir)
            elif packets_from_nazir != 0:
                create_sets(potential_scum, packets_from_nazir)
                init = True
            packets_from_nazir = 0
            potential_scum = {}
        if ip_src == nazir_ip:
            packets_from_nazir += 1

    elif ip_src == mix_ip:
        potential_scum[ip_dst] = potential_scum.get(ip_dst, 0) + 1

print_output()
    # all data is ASCII encoded (byte arrays). If we want to compare with strings
    # we need to decode the byte arrays into UTF8 coded strings
    #eth_src = pkt.packet.src.decode('UTF8')
    #eth_dst = pkt.packet.dst.decode('UTF8')
    #print ('{}\t\t{}\t{}\t{}\t{}'.format(timestamp, eth_src, eth_dst, ip_src, ip_dst))
