from collections import deque, Counter

import pylab
from networkx import DiGraph
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt


def parse_module(line):
    description = dict()
    name, destinations = line.strip().split(' -> ')
    if name[0] == '%':
        name = name[1:]
        description['type'] = 'flipflop'
        description['state'] = 'low'

    elif name[0] == '&':
        name = name[1:]
        description['type'] = 'conjunction'
        description['state'] = dict()

    else:
        assert name == 'broadcaster'
        description['type'] = 'broadcaster'

    destinations = destinations.split(', ')
    description['destinations'] = destinations

    return name, description


def process_pulse(pulses, modules, count):
    emitter_name, pulse, receiver_name = pulses.popleft()
    if receiver_name == 'rx':
        count.update([pulse])
    # print(f'{emitter_name} --> {pulse} --> {receiver_name}')
    receiver = modules.get(receiver_name)
    if receiver:

        match receiver['type']:

            case 'flipflop':
                if pulse == 'low':
                    receiver['state'] = 'low' if receiver['state'] == 'high' else 'high'
                    for destination in receiver['destinations']:
                        pulses.append((receiver_name, receiver['state'], destination))

            case 'conjunction':
                receiver['state'][emitter_name] = pulse
                if all(x == 'high' for x in receiver['state'].values()):
                    for destination in receiver['destinations']:
                        pulses.append((receiver_name, 'low', destination))

                else:
                    for destination in receiver['destinations']:
                        pulses.append((receiver_name, 'high', destination))

            case 'broadcaster':
                for destination in receiver['destinations']:
                    pulses.append((receiver_name, pulse, destination))


def main():
    modules = dict()
    graph = DiGraph(directed=True)
    with open('input/input.txt') as f:
        for line_ in f:
            name, thing = parse_module(line_)
            modules[name] = thing

    for module, thing in modules.items():
        for dest in thing['destinations']:
            dest = modules.get(dest)
            if dest and dest['type'] == 'conjunction':
                dest['state'][module] = 'low'

    print(modules)

    for module in modules:
        graph.add_node(module, label=module)

    for module, thing in modules.items():
        for dest in thing['destinations']:
            graph.add_edge(module, dest)

    nx.draw(graph, with_labels=True)
    pylab.show()

    # modules['button'] = {'destinations': ['broadcaster'], 'type': 'button'}
    pulses = deque()

    """for i in tqdm(range(10000000000)):
        count = Counter()
        pulses.append(('button', 'low', 'broadcaster'))
        while pulses:
            process_pulse(pulses, modules, count)

        if count['low']:
            print(i, count['low'])"""


if __name__ == "__main__":
    main()
