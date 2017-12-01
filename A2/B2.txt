from __future__ import print_function
import netaddr
import sys
from pcapfile import savefile

sets = []

'''
Returns True if every set in 'sets' is mutually disjointed with the set
potential_scum
'''
def is_disjoint(potential_scum):
	for aset in sets:
		if len(aset.intersection(potential_scum)) > 0:
			return False
	return True

'''
Compare current set potential_scum with each of the mutually disjointed sets in
'sets'. If there are multiple sets in 'sets' that intersect with potential_scum
we discard potential_scum. Else if there is exactly one set that intersects we
use potential_scum to narrow that set down.
'''
def exclude(potential_scum):
	index = 0
	matches = 0
	for aset in sets:
		if len(potential_scum.intersection(aset)) > 0:
			matches += 1
			if matches == 1:
				index = sets.index(aset)

	if matches == 1:
		print(sets[index], "CHANGED TO", potential_scum.intersection(sets[index]))
		sets[index] = potential_scum.intersection(sets[index])

'''
Returns True if every set in sets contains exactly one IP address.
'''
def is_done(potential_scum):
	for aset in sets:
		if len(aset) > 1:
			return False
	return True

def main():
	testcap = open(sys.argv[1], 'rb')
	capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

	nazir_ip = sys.argv[2]
	mix_ip = sys.argv[3]
	nr_partners = int(sys.argv[4])
	potential_scum = set()
	has_sent = False
	last_sender = ""

	'''
	While loop necessary since we need to iterate over all the packets multiple
	times.
	'''
	i = 0
	while i < len(capfile.packets):
		pkt = capfile.packets[i]
		ip_src = str(pkt.packet.payload.src.decode('UTF8'))
		ip_dst = str(pkt.packet.payload.dst.decode('UTF8'))

		#Packet is the first of a new batch where the Mix is the receiver. The Mix has previously been sending.
		if last_sender == mix_ip and ip_dst == mix_ip:
			if len(sets) >= nr_partners and has_sent:
				'''
				Exluding phase:
				Executes after we have found m number of mutually disjointed
				sets, where m is the nr of partners. At this point,	do not add
				any more sets. Instead, use any new set to trim the	previously
				saved ones.
				'''
				exclude(potential_scum)
				#Do a check to see if we are done.
				if is_done(potential_scum):
					break
				#Reset the flags and current set to prepare for next loop around.
				has_sent = False
				potential_scum = set()
			else:
				if has_sent and is_disjoint(potential_scum):
					'''
					Learning phase:
					Not enough mutually disjointed sets. Check if the
					current set is a mutually disjointed set and if it includes
					a flagged packet. If so	we add it.
					'''
					sets.append(potential_scum)
				#Reset the flags and current set to prepare for next loop around.
				has_sent = False
				potential_scum = set()

		#Packets are being sent from the Clients to the Mix. Check to see if Nazir is sending something. If so, flag it.
		if ip_src == nazir_ip:
			has_sent = True
		#Packets are being sent from the Mix to the Clients. Record all receivers
		if ip_src == mix_ip:
			potential_scum.add(ip_dst)
		#Keep track of last_sender in order to know when the batch ends
		last_sender = ip_src
		#The while loop breaks itself when it's done. Until then we simply increment i or reset i and go for another run.
		i += 1
		if i == len(capfile.packets):
			i = 0

	'''
	Once the excluding phase is over, the sets contain only one recipient, which
	is one of the partners. Add the IPs of these and return as result.
	'''
	print("The sets are now:")
	summed_ip = 0
	for aset in sets:
		print(aset)
		summed_ip += int(netaddr.IPAddress(list(aset)[0]))
	print("Sum of the IPs:", summed_ip)

if __name__ == "__main__":
    main()
