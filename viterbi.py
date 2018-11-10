import itertools
import random
from math import pi, exp
import math
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.integrate

matplotlib.rcParams.update({'axes.titlesize': 22, 'axes.labelsize': 22, 'legend.shadow': True, 
                            'legend.framealpha': 1.0, 'legend.fancybox': True, 'legend.fontsize':16,
                           'figure.figsize': (15.0, 6.0), 'xtick.labelsize' : 17, 'ytick.labelsize' : 17})

def viterbi(seq, error_vector):
    FSM = [('00', {'0' : ('00', 0), '1' : ('11', 1)}),
       ('10', {'0' : ('10', 3), '1' : ('01', 2)}),
       ('11', {'0' : ('01', 1), '1' : ('10', 2)}),
       ('01', {'0' : ('11', 0), '1' : ('00', 1)})]
    FSM2 = [('00', {'00' : ('0', 0),'11' : ('1', 1)}),
	   ('10', {'10' : ('0', 3), '01' : ('1', 2)}),
	   ('11', {'01' : ('0', 1), '10' : ('1', 2)}),
	   ('01', {'11' : ('0', 0), '00' : ('1', 1)})]
    curState = 0 
    output = ''

    for i in seq:
        output += FSM[curState][1].get(i)[0]
        curState = FSM[curState][1].get(i)[1]

    print("coder input: %s" % seq)
    print("coder output: %s" % output)
    def distance(a, b): 
        return sum([1 for i in zip(a, b) if i[0] != i[1]])
    def corrupt(seq, err): 
        return ''.join(['1' if i[0] != i[1] else '0' for i in zip(seq, err) ])
    def splitBy2(seq): 
        return [seq[i:i+2] for i in range(0, len(seq), 2)]
    seq2 = output
    seq2 = corrupt(seq2, error_vector)
    seq2 = splitBy2(seq2)
    combo = [''.join(i) for i in list(itertools.product('01', repeat=(len(seq2) * 2) ))]
    total = []

    for j in combo:
        SEQ = splitBy2(j)
        Out = ''
        curState = 0
        score = 0
        states = ''
        try:
            for p, s in zip(SEQ, seq2):
                Out += FSM2[curState][1].get(p)[0]
                states += FSM2[curState][0]
                curState = FSM2[curState][1].get(p)[1]
                score += distance(p, s)

            total.append([score, Out, j, states])
        except Exception:
            continue

    total.sort()
    coordY = [0, 1, 2, 3]
    coordX = [0, 0, 0, 0]
    ax = plt.figure(1).add_subplot(1, 1, 1)
    ax.set_title(r"$\rm{Viterbi  \, \, decoder}$", fontsize=25)
    for i in xrange(len(seq)):
        ax.scatter(4 * [i], coordY, s=90)
        for k in coordY: 
            ax.text(i - 0.3, k + 0.1, format(3 - k, '#04b')[2:], fontsize=20)
    for i in total: 
        ax.plot([3 - int(j, 2) for j in splitBy2(i[3])],'k', alpha=0.5)
    ax.plot([3 - int(j, 2) for j in splitBy2(total[0][3])],color='red', lw=3)
    plt.axis('off')
    plt.show()
    plt.close()

if __name__ == "__main__":
    viterbi(seq='1100011', error_vector='00000000010')
