class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
        if self.suit not in ["Spades", "Clubs", "Hearts", "Diamonds"]:
            print(f"{suit} does not exist")
        if self.rank not in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            print(f"{rank} deos not exist")
    
    def __str__(self):
        return f"{self.rank} of {self.suit} with a value of {self.value}"


def create_deck():
    suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for i in range(8):                                  # A typical game of blackjack at a casino has at least 8 full
        for suit in suits:                              # decks of cards. So our deck will have 8 full deck of cards  
            for rank in ranks:                          # totalling 8 * 52 = 416 cards.    
                if rank == "A":
                    card = Card(suit, rank, 1)
                    deck.append(card)
                elif rank in ["10", "J", "Q", "K"]:
                    card = Card(suit, rank, 10)
                    deck.append(card)
                else:
                    card = Card(suit, rank, int(rank))
                    deck.append(card)
    return deck


if __name__ == "__main__":
    deck = create_deck()
    print(f"Deck is {len(deck)} cards long")
