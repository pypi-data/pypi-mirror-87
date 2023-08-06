from enum import Enum
from functools import reduce
from operator import add
from random import sample


Suit = Enum('Suit', 'RAT COCKROACH BAT FLY SCORPION STINKBUG SPIDER TOAD')

all_cards = reduce(add, [[s]*8 for s in Suit])


def deck():
    return sample(all_cards, len(all_cards))
