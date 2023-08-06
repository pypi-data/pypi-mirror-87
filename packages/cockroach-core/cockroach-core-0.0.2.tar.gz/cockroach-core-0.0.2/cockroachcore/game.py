from itertools import cycle
from enum import Enum
from random import choice
from cockroachcore.cards import deck


class InvalidActionException(Exception):
    pass


Action = Enum('Action', 'PLAY CALL PASS')


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tabled = {}

    def table(self, card):
        try:
            self.tabled[card] = self.tabled[card] + 1
        except KeyError:
            self.tabled[card] = 1

    def __eq__(self, other):
        try:
            return self.name == other.name and \
                    self.hand == other.hand and \
                    self.tabled == other.tabled
        except Exception:
            return False

    def __repr__(self):
        return 'Player(name={}, hand={}, tabled={})'.format(
                self.name, self.hand, self.tabled)


class Game:
    def __init__(self):
        self.players = {}
        self.turn = None

    def join(self, player_name):
        self.players[player_name] = Player(player_name)

    def deal(self):
        for player, card in zip(cycle(self.players.values()), deck()):
            player.hand.append(card)
        self.turn = Turn(choice(list(self.players.keys())))  # nosec

    def play(self, to, card, claim):
        # TODO: validate play
        self.players[self.turn.player].hand.remove(card)
        self.turn.play(to, card, claim)

    def call(self, agree):
        # TODO: validate call
        if self.turn.call(agree):
            self.players[self.turn.played[-1]].table(self.turn.card)
            self.turn = Turn(self.turn.played[-1])
            return True
        else:
            self.players[self.turn.player].table(self.turn.card)
            self.turn = Turn(self.turn.player)
            return False

    def pass_to(self, to, claim):
        self.turn.pass_to(to, claim, len(self.players))

    def check_loser(self):
        for p in self.players.values():
            if [v for v in p.tabled.values() if v >= 4]:
                return p.name
        return None


class Turn:
    def __init__(self, player):
        self.actions = {Action.PLAY}
        self.player = player
        self.played = []
        self.card = None
        self.claim = None

    def play(self, to, card, claim):
        self.card = card
        self.claim = claim
        self.played.append(self.player)
        self.player = to
        self.actions = {Action.CALL, Action.PASS}

    def call(self, agree):
        if (agree and self.card == self.claim) or \
                (not agree and self.card != self.claim):
            return True
        else:
            return False

    def pass_to(self, to, claim, total_players):
        self.played.append(self.player)
        self.player = to
        self.claim = claim
        self.actions = {Action.CALL}
        if len(self.played) < total_players - 1:
            self.actions.add(Action.PASS)
