import itertools
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'axes.titlesize': 22, 'axes.labelsize': 22, 'legend.shadow': True, 
                            'legend.framealpha': 1.0, 'legend.fancybox': True, 'legend.fontsize':16,
                           'figure.figsize': (15.0, 6.0), 'xtick.labelsize' : 17, 'ytick.labelsize' : 17})

def distance(a, b): 
    return sum([1 for i,j in zip(a, b) if i is not j])
def corrupt(seq, err): 
    return ''.join(['1' if i is not j else '0' for i,j in zip(seq, err) ])
def splitBy2(seq): 
    return [seq[i:i+2] for i in range(0, len(seq), 2)]

def encode(seq):
    FSM = [('00', {'0' : ('00', 0), '1' : ('11', 1)}),
       ('10', {'0' : ('10', 3), '1' : ('01', 2)}),
       ('11', {'0' : ('01', 1), '1' : ('10', 2)}),
       ('01', {'0' : ('11', 0), '1' : ('00', 1)})]
    curState = 0 
    output = ''

    for i in seq:
        output += FSM[curState][1].get(i)[0]
        curState = FSM[curState][1].get(i)[1]

    print("coder input: %s" % seq)
    print("coder output: %s" % output)
    return output

def decode(seq):    
    FSM = [('00', {'00' : ('0', 0),'11' : ('1', 1)}),
	   ('10', {'10' : ('0', 3), '01' : ('1', 2)}),
	   ('11', {'01' : ('0', 1), '10' : ('1', 2)}),
	   ('01', {'11' : ('0', 0), '00' : ('1', 1)})]

    seq = splitBy2(seq)
    combo = [''.join(i) for i in list(itertools.product('01', repeat=(len(seq) * 2) ))]
    total = []

    for j in combo:
        SEQ = splitBy2(j)
        Out = ''
        curState = 0
        score = 0
        states = ''
        try:
            for p, s in zip(SEQ, seq):
                Out += FSM[curState][1].get(p)[0]
                states += FSM[curState][0]
                curState = FSM[curState][1].get(p)[1]
                score += distance(p, s)

            total.append([score, Out, j, states])
        except Exception:
            continue
    total.sort()
    return total


def plot(total):
    coordY = [0, 1, 2, 3]
    coordX = [0, 0, 0, 0]
    ax = plt.figure(1).add_subplot(1, 1, 1)
    ax.set_title(r"$\rm{Viterbi  \, \, decoder}$", fontsize=25)
    for i in xrange(len(total[0][1])):
        ax.scatter(4 * [i], coordY, s=90)
        for k in coordY: 
            ax.text(i - 0.3, k + 0.1, format(3 - k, '#04b')[2:], fontsize=20)
    for i in total: 
        ax.plot([3 - int(j, 2) for j in splitBy2(i[3])],'k', alpha=0.5)
    ax.plot([3 - int(j, 2) for j in splitBy2(total[0][3])],color='red', lw=3)
    plt.axis('off')
    plt.show()
    plt.close()


def viterbi(seq, error_vector):
    output = encode(seq)
    corruptedVec = corrupt(output, error_vector)
    total = decode(corruptedVec)
    plot(total)


if __name__ == "__main__":
    viterbi(seq='1100011', error_vector='000000000100')
