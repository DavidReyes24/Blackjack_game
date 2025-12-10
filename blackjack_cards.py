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
    for suit in suits:
        for rank in ranks:
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


def main():
    deck = create_deck()
    print(f"Deck is {len(deck)} cards long")

main()