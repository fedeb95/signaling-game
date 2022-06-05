import random
import argparse

def create_urns(urn_types, ball_types):
    urns = {}
    for t in urn_types:
            for b in ball_types:
                if not t in urns:
                    urns[t] = []
                urns[t].append(b)
    return urns

class UrnLearner():
    def __init__(self, urn_types, ball_types):
        self.urns = create_urns(urn_types, ball_types)
   
    def choose_ball(self, urn_type):
        return random.choice(self.urns[urn_type]) 

    def put_ball(self, urn_type, ball_type):
        self.urns[urn_type].append(ball_type) 

    def remove_but_one(self, urn_type, ball_type):
        if len([ b for b in self.urns[urn_type] if b == ball_type ]) > 1:
            self.urns[urn_type].remove(ball_type)
        
class Sender(UrnLearner):
    def signal(self, state):
        return self.choose_ball(state)

class Receiver(UrnLearner):
    def act(self, signal):
        return self.choose_ball(signal)

def positive_strategy(state, sender, receiver):
    signal = sender.signal(state)
    act = receiver.act(signal)
    if state == act:
        sender.put_ball(state, signal)    
        receiver.put_ball(signal, state)
        return True
    return False

def positive_negative_strategy(state, sender, receiver): 
    signal = sender.signal(state)
    act = receiver.act(signal)
    if state == act:
        sender.put_ball(state, signal)    
        receiver.put_ball(signal, state)
        return True
    else:
        sender.remove_but_one(state, signal)
        receiver.remove_but_one(signal, state)
        return False

def main():
    parser = argparse.ArgumentParser(description='A Lewis singaling game simulation')
    parser.add_argument('-r', '--runs', dest='runs', action='store', default='1000', help='Number of runs', type=int)
    parser.add_argument('-s', '--states', dest='states', action='store', default='2', help='Number of states', type=int)
    parser.add_argument('-t', '--terms', dest='terms', action='store', default='2', help='Number of terms (signals)', type=int)
    parser.add_argument('-l', '--learning', dest='learning', action='store', default='positive', help='Type of learning', type=str,
        choices=['positive', 'positive_negative'])
    args = parser.parse_args()

    states = [ i for i in range(0, args.states) ]
    signals = [ i for i in range(0, args.terms) ]
    sender = Sender(states, signals)
    receiver = Receiver(signals, states)
    successes = 0
    total = 0
    for i in range(0, args.runs):
        state = random.choice(states) 
        if args.learning == 'positive':
            strategy = positive_strategy
        elif args.learning == 'positive_negative':
            strategy = positive_negative_strategy
        else:
            raise TypeError('Unknown payoff type, supported: positive, positive_negative')

        if strategy(state, sender, receiver):
            successes += 1
        total += 1

    print('Sender:')
    for st in states:
        print(f'\tState {st}:')
        for sg in signals:
            count = len([ el for el in sender.urns[st] if el == sg ])
            print(f'\t\tSignal {sg} count: {count}') 
    print('Receiver:')
    for sg in signals:
        print(f'\tSignal {sg}:')
        for st in states:
            count = len([ el for el in receiver.urns[sg] if el == st ])
            print(f'\t\tState {st} count: {count}') 
    print(f'Success rate: {successes/total}')

if __name__=='__main__':
    main()
