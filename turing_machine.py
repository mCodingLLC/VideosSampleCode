import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class TuringMachine:
    states: set[str]
    symbols: set[str]
    blank_symbol: str
    input_symbols: set[str]
    initial_state: str
    accepting_states: set[str]
    transitions: dict[tuple[str, str], tuple[str, str, int]]
    # state, symbol -> new state, new symbol, direction

    head: int = field(init=False)
    tape: defaultdict[int, str] = field(init=False)
    current_state: str = field(init=False)
    halted: bool = field(init=False, default=True)

    def initialize(self, input_symbols: dict[int, str]):
        self.head = 0
        self.halted = False
        self.current_state = self.initial_state
        self.tape = defaultdict(lambda: self.blank_symbol, input_symbols)

    def step(self):
        if self.halted:
            raise RuntimeError('Cannot step halted machine')

        try:
            state, symbol, direction = self.transitions[(self.current_state, self.tape[self.head])]
        except KeyError:
            self.halted = True
            return
        self.tape[self.head] = symbol
        self.current_state = state
        self.head += direction


    def accepted_input(self):
        if not self.halted:
            raise RuntimeError('Machine still running')
        return self.current_state in self.accepting_states

    def print(self, window=10):
        print('... ', end='')
        print(' '.join(self.tape[i] for i in range(self.head - window, self.head + window + 1)), end='')
        print(f' ... state={self.current_state}')
        print(f'{" " * (2 * window + 4)}^')


if __name__ == '__main__':
    tm = TuringMachine(states={'a', 'b', 'c', 'H'},
                       symbols={'0', '1'},
                       blank_symbol='0',
                       input_symbols={'1'},
                       initial_state='a',
                       accepting_states={'H'},
                       transitions={
                           ('a', '0'): ('b', '1', 1),
                           ('a', '1'): ('c', '1', -1),
                           ('b', '0'): ('a', '1', -1),
                           ('b', '1'): ('b', '1', 1),
                           ('c', '0'): ('b', '1', -1),
                           ('c', '1'): ('H', '1', 1),
                       })
    tm.initialize({0: '1', 2: '1'})

    while not tm.halted:
        tm.print()
        tm.step()
        time.sleep(1)

    print(tm.accepted_input())






