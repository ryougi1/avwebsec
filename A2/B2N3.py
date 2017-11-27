from __future__ import print_function
from pcapfile import savefile
import netaddr
import sys

nazir_ip = sys.argv[2]
mix_ip = sys.argv[3]
nr_partners = int(sys.argv[4])
sets = []

def test():
    print("Nr of sets captured: ", len(sets))
    for current_set in sets:
        print(current_set)
    #print(all_potential_scum)



def main ():
    testcap = open(sys.argv[1], 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

    current_potential_scum = set()
    last_sender = ""
    has_sent = False

    #Learning phase
    for pkt in capfile.packets:
        ip_src = str(pkt.packet.payload.src.decode('UTF8'))
        ip_dst = str(pkt.packet.payload.dst.decode('UTF8'))

        '''
        True if this is the first packet of a new batch where the the Mix is receiving.
        In which case save the set created in the previous batch, clear the set to prepare
        for reuse and reset has_sent flag and last_sender
        '''
        if last_sender == mix_ip and ip_dst == mix_ip and current_potential_scum:
            #print("Appended: ", current_potential_scum)
            sets.append(current_potential_scum)
            current_potential_scum = set()
            #print("After clearing: ", current_potential_scum)
            has_sent = False
            last_sender = ""

        #When Clients are sending to Mix, set flag has_sent if Nazir is one of them
        if ip_dst == mix_ip:
            if ip_src == nazir_ip:
                has_sent = True
        #When Mix is sending to Clients and flag has_sent is set, record all receivers
        elif ip_src == mix_ip:
            if has_sent:
                current_potential_scum.add(ip_dst)
            last_sender = mix_ip

    #Exluding phase
    isNotDone = True
    current_loop = 0
    while(isNotDone):
        print("Current loop:", current_loop)
        for i in range(len(sets)-2):
            RnRi = sets[i].intersection(sets[i + 1])
            RnRj = sets[i].intersection(sets[i + 2])
            if len(RnRi) > 0 and len(RnRj) == 0:
                #print("Found one")
                print("RnRi: ", RnRi)
                print("RnRj: ", RnRj)
                print(sets[i], "changed to:", RnRi)
                sets[i] = RnRi
            elif len(RnRj) > 0 and len(RnRi) == 0:
                print("RnRi: ", RnRi)
                print("RnRj: ", RnRj)
                print(sets[i], "changed to:", RnRj)
                sets[i] = RnRj

        current_loop += 1
        isNotDone = False
        for aset in sets:
            if len(aset) > nr_partners:
                isNotDone = True
                print("Set that is fucking us:", aset, "at index", sets.index(aset))
                break


    #test()
if __name__ == "__main__":
    main()
