import random

from netaddr import IPNetwork

from fingerprint import read_fingerprints
from reassembler import Reassembler
from scenario import create_network, draw_network, generate_attack_fingerprint

random.seed(12)

if __name__ == '__main__':
    G = create_network([IPNetwork("10.0.0.0/16"), IPNetwork("55.0.0.0/8"),  IPNetwork("71.220.0.0/16"), IPNetwork("72.220.0.0/16"), IPNetwork("73.220.0.0/16"), IPNetwork("74.220.0.0/16"), IPNetwork("75.220.0.0/16")],  max_clients=5)
    # draw_network(G)

    clients = [n for n, data in G.nodes(data=True) if data['client']]
    sources = random.sample(clients, 10)
    possible_targets = [n for n, data in G.nodes(data=True) if data['client'] and not data.get('spoofed', False) and not n in sources]
    target = random.choice(possible_targets)

    print("Creating scenario with sources \n", [G.nodes(data=True)[s].get('spoofed_ip', s) for s in sources], "\n and target", target)

    fingerprints = generate_attack_fingerprint(G, sources, target, num_background_fp=100, output_folder='fingerprints')

    reassembler = Reassembler("./fingerprints")
    #reassembler.drop_fingerprints(0.9)
    reassembler.reassemble()
