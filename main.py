#!/usr/bin/env python3
from itertools import product, combinations
import random


class Deck():
    def __init__(self):
        # ♥, ♦, ♣, ♠
        self.suits = ['Heart', 'Diamond', 'Club', 'Spade']
        self.nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = []

        self.generate_deck()
        random.shuffle(self.deck)

    def view_deck(self):
        return self.deck

    def generate_deck(self):
        self.deck = []
        for suit, num in product(self.suits, self.nums):
            self.deck.append(num + '-' + suit)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self):
        assert len(self.deck) >= 0

        card = self.deck[-1]
        self.deck.pop()
        return card


class Player():
    class BlackJack(Deck):
        def __init__(self):
            # Inherit deck for self.suits
            super().__init__()

            # black jack AA
            self.black_jack_AA_cases = set()
            for suit_1, suit_2 in combinations(self.suits, 2):
                self.black_jack_AA_cases.add( ('A' + '-' + suit_1, 'A' + '-' + suit_2) )

            # normal blackjack: A + (10,J,Q,K)
            self.black_jack_cases = set()
            for suit_1, num_1 in product(self.suits, ['10', 'J', 'Q', 'K']):
                for suit_2, num_2 in product(self.suits, ['A']):
                    self.black_jack_cases.add( (num_1 + '-' + suit_1,  num_2 + '-' + suit_2)  )
                    self.black_jack_cases.add( (num_2 + '-' + suit_2, num_1 + '-' + suit_1) )

    def __init__(self, risky_level):
        self.risky_level = risky_level
        self.hands = []

        black_jack = self.BlackJack()
        self.black_jack_cases = black_jack.black_jack_cases
        self.black_jack_AA_cases = black_jack.black_jack_AA_cases

    def __get_score_dp(self, hands):
        cur = set([0])
        nex = set()
        for card in hands:
            for x in cur:
                if card == 'A':
                    nex.add(x + 1)
                    nex.add(x + 10)
                    nex.add(x + 11)
                elif card in set(['J', 'Q', 'K']):
                    nex.add(x + 10)
                else:
                    nex.add(x + int(card))

            cur = nex
            nex = set()

        res_small = -1
        res_big = 999
        for x in cur:
            if x <= 21: res_small = max(res_small, x)
            else: res_big = min(res_big, x)
        return res_small if res_small != -1 else res_big

    def get_score(self):
        assert len(hands) <= 5

        # Solve stage 1
        if len(self.hands) == 0: return '0'
        if len(self.hands) == 2 and (self.hands[0], self.hands[1]) in self.black_jack_AA_cases: return 'BLACK_JACK_AA'
        if len(self.hands) == 2 and (self.hands[0], self.hands[1]) in self.black_jack_cases: return 'BLACK_JACK'


        # Get score
        hands = [x.split('-')[0] for x in self.hands]
        score = self.__get_score_dp(hands)

        # Solve stage 2
        if len(self.hands == 5) and score <= 21: return 'FIVE_ELITES'

        return str(score)

    def draw_card(self):
        pass

    def debug(self):
        print(self.black_jack_cases)
        # print(self.black_jack_cases)





# ----------------------------------- MAIN ----------------------------------- #
if __name__ == "__main__":
    deck = Deck()
    player = Player(15)

    player.debug()

