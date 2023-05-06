import requests

# Cards values
cards = {
    'ACE': 11, 
    '2': 2, 
    '3': 3, 
    '4': 4, 
    '5': 5, 
    '6': 6, 
    '7': 7, 
    '8': 8, 
    '9': 9, 
    '10': 10, 
    'JACK': 10, 
    'QUEEN': 10, 
    'KING': 10
}

# Create deck
response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
deck = response.json()
deck_id = deck['deck_id']

class Card:
    def __init__(self, deck_id = deck_id):
        response_card = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
        full_card = response_card.json()['cards'][0]
        self.card_suit = full_card['suit']              # Suit
        self.card_rank = full_card['value']             # Rank
        self.card_value = cards.get(self.card_rank)     # Value

class Hand:
    def __init__(self):
        self.cards = []     # Cards on the hand
        self.points = 0     # Hand total value

    # Add card to Hand    
    def add_card(self, card):
        self.cards.append(card)
        self.points += card.card_value

# Start a new game
def newGame():
    # Create Hands
    global player_hand 
    global dealer_hand 
    player_hand = Hand()
    dealer_hand = Hand()
    
    print('Starting a new game...')

    # Distribute initial cards
    for i in range(2):
        # Your cards
        newCard = Card()
        player_hand.add_card(newCard)

        # Dealer cards
        newCard = Card()
        dealer_hand.add_card(newCard)

    print("Dealer cards:")
    print(f'Card: {dealer_hand.cards[0].card_rank} de {dealer_hand.cards[0].card_suit}')
    print("Card: <hidden>")

# Start
newGame()
while True:
    # Showing your cards and total value
    print(f'\nYour cards are:')
    for card in player_hand.cards:
        print(f'Card: {card.card_rank} of {card.card_suit}')
    
    print(f'Total value of your hand: {player_hand.points}')
    
    if player_hand.points > 21:
        print('\nYou busted! Good luck next time')
        break
    
    # Player decision (hit or stand)
    player_action = input(
            f'\nWrite: \n"H" to hit or \n"S" to stand:\n').upper()
    
    # Stand 
    if player_action == 'S':
        print(f'Your final points: {player_hand.points}')
        print(f"\nDealer's second card: {dealer_hand.cards[1].card_rank} of {dealer_hand.cards[1].card_suit}")

        # Dealer must buy if his hand is worth less than 17
        while dealer_hand.points <= 16:
            newCard = Card()
            dealer_hand.add_card(newCard)
            print(f'Dealer buys: {newCard.card_rank} of {newCard.card_suit}')
        
        print(f"Dealer's final points: {dealer_hand.points}")

        # Showing who won
        if dealer_hand.points > 21 and player_hand.points <= 21:
            print('\nDealer busted and you won!')
            break
        elif player_hand.points > dealer_hand.points:
            print('\nYou won!')
        else:
            print('\nYou lost! Good luck next time')
        break
    # Hit
    elif player_action == 'H':
        newCard = Card()
        player_hand.add_card(newCard)
