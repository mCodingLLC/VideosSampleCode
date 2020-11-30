import time

from turing_machine import TuringMachine


def main():
    tm = TuringMachine(states={'i', 'a', 'b', 'c', 'd', 'e', 'H'},
                       symbols={'0', '1'},
                       blank_symbol='0',
                       input_symbols={'1'},
                       initial_state='i',
                       accepting_states={'H'},
                       transitions={
                           ('i', '0'): ('H', '0', 1),
                           ('i', '1'): ('a', '0', 1),
                           ('a', '1'): ('a', '1', 1),
                           ('a', '0'): ('b', '0', 1),
                           ('b', '1'): ('b', '1', 1),
                           ('b', '0'): ('c', '1', 1),
                           ('c', '0'): ('d', '1', -1),
                           ('c', '0'): ('d', '1', -1),
                           ('d', '1'): ('d', '1', -1),
                           ('d', '0'): ('e', '0', -1),
                           ('e', '1'): ('e', '1', -1),
                           ('e', '0'): ('i', '0', 1),
                       })
    tm.initialize({i: '1' for i in range(5)})
    # or a nicer way to input a string
    # tm.initialize(dict(enumerate("11111")))


    while not tm.halted:
        tm.print()
        tm.step()
        time.sleep(.3)

    print(tm.accepted_input())


if __name__ == '__main__':
    main()
