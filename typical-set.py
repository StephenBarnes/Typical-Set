#!/usr/bin/env python2

import graphviz as gv
from math import log
from itertools import starmap

bernoulli_probability = 3. / 5
sequence_length = 5

def seq_probability(S):
    r = 1.
    for letter in S:
        if letter == 1:
            r *= bernoulli_probability
        else:
            assert letter == 0
            r *= 1 - bernoulli_probability
    return r

def all_binary_sequences(l):
    if l == 0:
        yield []
        return
    for seq in all_binary_sequences(l-1):
        yield seq + [0]
        yield seq + [1]

def seq_self_information(S):
    return -log(seq_probability(S), 2)

def seq_typicality(S):
    # largest epsilon such that S is in the typical set with that epsilon
    # ie, n H(X) - I(S), where I(S) = -log p(S) is the self-information
    # So if S is more likely, this is positive;
    # and if S is less likely, this is negative.
    iS = seq_self_information(S)
    n = len(S)
    hX = -bernoulli_probability * log(bernoulli_probability, 2) \
        - (1 - bernoulli_probability) * log(1 - bernoulli_probability, 2)
    return iS - n*hX

def seq_colors(Ss):
    typicalities = map(seq_typicality, Ss)
    max_color = 0xFF
    max_typicality = max(typicalities)
    min_typicality = min(typicalities)
    def color(S, t):
        if t >= 0:
            c = int(max_color * (t / max_typicality))
            return '#%s0000' % hex(c)[2:]
        if t < 0:
            c = int(max_color * (t / min_typicality))
            return '#0000%s' % hex(c)[2:]
    colors = [color(*args) for args in zip(Ss, typicalities)]
    return colors

def seq_str(S):
    return ''.join(map(str, S))

def draw():
    seqs = list(all_binary_sequences(sequence_length))
    colors = seq_colors(seqs)

    g = gv.Graph()
    for S, c in zip(seqs, colors):
        g.node(seq_str(S), color=c, style='filled', fontcolor='white')
    added = set()
    for S in seqs:
        for i, v in enumerate(S):
            S2 = S[:i] + [1-v] + S[i+1:]
            strS, strS2 = seq_str(S), seq_str(S2)
            if (strS, strS2) not in added:
                g.edge(strS, strS2)
                added.add((strS, strS2))
                added.add((strS2, strS))

    g.engine = 'dot'
    g.format = 'svg'
    g.render('/tmp/typical.gv', view=True)


draw()


