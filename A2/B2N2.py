#!/usr/bin/env python

from pcapfile import savefile
import netaddr
import sys

#calculates the sum of all perpetrators IP address and prints the result
def print_output (sets):
    ip_sum = 0
    for ip in sets:
        print(ip)
        if len(ip) > 1:
            print("Fail: one or more of the sets contains more than 1 IP")
            #break
        else:
            ip_sum += int(netaddr.IPAddress(ip.pop()))
    else:
        print("Result: ", ip_sum)

def check (potential_scum, sets):
    for i in xrange(len(sets)):
        if sets[i]:
            print("intersection: ",sets[i].intersection(potential_scum))
            print("A_set: ", i, sets[i])
            if len(sets[i].intersection(potential_scum)) > 0:
                print("length was: ", len(sets[i].intersection(potential_scum)))
                sets[i] = sets[i].intersection(potential_scum)
                break
            else:
                # No matches
                print("No Match")
        else:
            # No previous elements, initialize new set
            sets[i] = set(potential_scum)
            print("Initialize new set: ", i, sets[i])
            break

def main ():
    nazir_ip = sys.argv[2]
    mix_ip = sys.argv[3]
    nr_partners = int(sys.argv[4])

    index = 0
    sets = [set() for _ in xrange(nr_partners)]

    testcap = open(sys.argv[1], 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

    packets_from_nazir = 0
    destinations = {}

    for pkt in capfile.packets:
        timestamp = pkt.timestamp
        ip_src = str(pkt.packet.payload.src.decode('UTF8'))
        ip_dst = str(pkt.packet.payload.dst.decode('UTF8'))

        # Packets sent TO the mixer
        if ip_dst == mix_ip:
            if destinations and packets_from_nazir != 0:
                potential_scum = [dest for dest in destinations if destinations[dest] == packets_from_nazir]
                check(potential_scum, sets)
                packets_from_nazir = 0
                destinations = {}
            if ip_src == nazir_ip:
                packets_from_nazir += 1

        # Packets sent FROM the mixer
        elif ip_src == mix_ip:
            destinations[ip_dst] = destinations.get(ip_dst, 0) + 1

    print_output(sets)

if __name__ == "__main__":
    main()
