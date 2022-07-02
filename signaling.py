import random
import argparse

def create_urns(urn_types, ball_types):
    urns = {}
    for t in urn_types:
            for b in ball_types:
                if not t in urns:
                    urns[t] = {}
                urns[t][b] = 1
    return urns

class UrnLearner():
    def __init__(self, urn_types, ball_types):
        self.urns = create_urns(urn_types, ball_types)
        self.urn_types = urn_types
        self.ball_types = ball_types
   
    def choose_ball(self, urn_type):
        urn = self.urns[urn_type]
        total = sum([ urn[k] for k in urn ])
        weights = [ urn[k]/total for k in urn ]
        # hacky, but works: last element is 1 - sum of other elements
        weights[len(weights)-1] = 1 - sum(weights[0:len(weights)-1])
        if not sum(weights) == 1:
            print(weights)
            print(sum(weights))
            raise ValueError('Sum of weights must equal 1')
        return random.choices(self.ball_types, weights=weights)[0]

    def put_ball(self, urn_type, ball_type):
        self.urns[urn_type][ball_type] += 1

    def remove_but_one(self, urn_type, ball_type):
        if self.urns[urn_type][ball_type] > 1:
            self.urns[urn_type][ball_type] += 1
        
class Sender(UrnLearner):
    def signal(self, state):
        return self.choose_ball(state)

class Receiver(UrnLearner):
    def act(self, signal):
        return self.choose_ball(signal)

class Strategy:
    def apply(self, state, sender, receiver):
        raise NotImplementedError

class PositiveStrategy(Strategy):
    def apply(self, state, sender, receiver):
        signal = sender.signal(state)
        act = receiver.act(signal)
        if state == act:
            sender.put_ball(state, signal)    
            receiver.put_ball(signal, state)
            return True
        return False

class PositiveNegativeStrategy(PositiveStrategy):
    def apply(self, state, sender, receiver):
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

def randomize_urn_learner(learner, interval):
    a = interval[0]
    b = interval[1]
    for urn_type in learner.urn_types:
        for ball_type in learner.ball_types:
            randomized = learner.urns[urn_type][ball_type] * random.uniform(a, b)
            learner.urns[urn_type][ball_type] = randomized

class RandPositiveStrategy(PositiveStrategy):
    def __init__(self, interval):
        self.interval = interval 

    def apply(self, state, sender, receiver):
        result = super().apply(state, sender, receiver)
        randomize_urn_learner(sender, self.interval) 
        randomize_urn_learner(receiver, self.interval) 
        return result
    
            
def main():
    parser = argparse.ArgumentParser(description='A Lewis singaling game simulation')
    parser.add_argument('-r', '--runs', dest='runs', action='store', default='1000', help='Number of runs', type=int)
    parser.add_argument('-s', '--states', dest='states', action='store', default='2', help='Number of states', type=int)
    parser.add_argument('-t', '--terms', dest='terms', action='store', default='2', help='Number of terms (signals)', type=int)
    parser.add_argument('-l', '--learning', dest='learning', action='store', default='positive', help='Type of learning', type=str,
        choices=['positive', 'positive_negative', 'randomized'])
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
            strategy = PositiveStrategy()
        elif args.learning == 'positive_negative':
            strategy = PositiveNegativeStrategy() 
        elif args.learning == 'randomized':
            strategy = RandPositiveStrategy((0.8, 1.2))
        else:
            raise TypeError('Unknown payoff type, supported: positive, positive_negative, randomized')

        if strategy.apply(state, sender, receiver):
            successes += 1
        total += 1

    print('Sender:')
    for st in states:
        print(f'\tState {st}:')
        for sg in signals:
            count = sender.urns[sg][st]
            print(f'\t\tSignal {sg} count: {count}') 
    print('Receiver:')
    for sg in signals:
        print(f'\tSignal {sg}:')
        for st in states:
            count = receiver.urns[st][sg]
            print(f'\t\tState {st} count: {count}') 
    print(f'Success rate: {successes/total}')

if __name__=='__main__':
    main()
