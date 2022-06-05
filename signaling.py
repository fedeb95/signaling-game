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

def positive_negative_strategy(state, sender, receiver): 
    signal = sender.signal(state)
    act = receiver.act(signal)
    if state == act:
        sender.put_ball(state, signal)    
        receiver.put_ball(signal, state)
    else:
        sender.remove_but_one(state, signal)
        receiver.remove_but_one(signal, state)

def main():
    parser = argparse.ArgumentParser(description='A Lewis singaling system simulation')
    parser.add_argument('-e', '--epochs', dest='epochs', action='store', default='1000', type=int)
    parser.add_argument('-st', '--states', dest='states', action='store', default='2', type=int)
    parser.add_argument('-sg', '--signals', dest='signals', action='store', default='2', type=int)
    parser.add_argument('-p', '--payoff', dest='payoff', action='store', default='positive', type=str)
    args = parser.parse_args()

    states = [ i for i in range(0, args.states) ]
    signals = [ i for i in range(0, args.signals) ]
    sender = Sender(states, signals)
    receiver = Receiver(signals, states)
    for i in range(0, args.epochs):
        state = random.choice(states) 
        if args.payoff == 'positive':
            positive_strategy(state, sender, receiver)
        elif args.payoff == 'positive_negative':
            positive_negative_strategy(state, sender, receiver)
        else:
            raise TypeError('Unknown payoff type, supported: positive, positive_negative')

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

if __name__=='__main__':
    main()
