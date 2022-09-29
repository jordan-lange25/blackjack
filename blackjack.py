#---------------------------#
#---- B L A C K J A C K ----#
#---------------------------#
# You know the rules
# 8 decks
# Dealer plays 3:2 on blackjack
# Dealer stands on all 17

import random
import time



# assemble the deck
def create_decks(number_of_decks):
    deck = []
    suits = ['Spades','Clubs','Diamonds','Hearts']
    cards = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
    points = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    for deck_num in range(number_of_decks): 
        for suit in suits:
            for card in cards:
                point = points[cards.index(card)]
                built_card = {}  
                built_card["card"] = card
                built_card["suit"] = suit
                built_card["points"] = point
                deck.append(built_card)
    return deck


# shuffle the deck and index
def shuffle_deck(deck): 
    shuffled_deck = random.sample(deck,len(deck))
    shuffled_indexed_deck = []
    for card in shuffled_deck:
        index_payload = {
            "index":shuffled_deck.index(card),
            "card_data":card
        }
        shuffled_indexed_deck.append(index_payload)
    return shuffled_indexed_deck
 

# take cards/deal from deck
def deal_card(deck,number_of_cards):
    cards = deck[0:number_of_cards]
    for i in range(number_of_cards):
        deck.pop(0)
    return cards, deck

# place a bet
def place_bet(wallet_value): 
    """
    Ensure the submitted input value is a number and that the player can afford the bet.
    """
    bet_input = ""
    sufficient_funds = False
    while type(bet_input) != int or sufficient_funds is False: 
        bet_input = input("How much would you like to bet?")
        try: 
            # check if the player submitted a number
            bet_input = int(bet_input)
            # if the player submitted a number, check if they can afford it
            if bet_input > wallet_value:
                print("You're a poor sack of shit aren't you? How about you enter a number you can afford?")
                pass
            else:
                sufficient_funds = True
                return bet_input
        except:
            print(f"oops! - please submit a number between 1 and {wallet_value}!")
            pass
        
# handle for Ace
def calculate_hand_value(hand):
    # handle for hace
    if 11 in hand and sum(hand) > 21:
         hand = hand.substitute(11,1)
         hand_value = sum(hand)
    else: 
        hand_value = sum(hand)
    return hand_value

# compare the two hands together
def calculate_winner(house_hand,player_hand):
    if house_hand > player_hand:
        status = "House wins"
    elif house_hand < player_hand: 
        status = "Player wins"
    else:
        status = "Push"
    return status


## Put it all together
print('''-----------------------------------------''')
print('''-----------------------------------------''')
print('''-----------WELCOME TO BLACKJACK!---------''')
print('''-----------------------------------------''')
print('''-----------------------------------------''')
player = input("What is your name?")
# create the deck (8 hands)
playing_deck = create_decks(8)
shuffled_deck = shuffle_deck(playing_deck)
player_wallet = []
print("deck assembled! Let's begin.")



round = 0
if round == 0:
    print("starting new round")
    time.sleep(.5)
    print("here's 100 bucks, you filthy animal.")
    player_wallet.append(100)
print(f"{player}'s wallet: {sum(player_wallet)}")

while len(shuffled_deck) != 0 and player_wallet[0] > 0:
    # INITIALIZE ROUND
    player_hand = []
    player_points = []
    dealer_points = []
    dealer_hand = []

    # choose your bet
    bet_amount = place_bet(sum(player_wallet))

    # deal two cards to the player and the dealer
    dealer_cards, current_deck = deal_card(shuffled_deck,2)
    player_cards, current_deck = deal_card(current_deck,2)
    dealer_hand.extend(dealer_cards)
    player_hand.extend(player_cards)


    # Tell the user what they have
    for card in dealer_hand:
        if dealer_hand.index(card) == 0:
            dealer_points.append(card.get('card_data').get('points'))
            print(f"DEALER HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")
    print(f"DEALER TOTAL: {sum(dealer_points)}")

    for card in player_hand:
        player_points.append(card.get('card_data').get('points'))
        print(f"{player} HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")
    print(f"PLAYER TOTAL: {sum(player_points)}")

    # ASK PLAYER TO HIT OR STAY
    stand = False
    while not stand:
        if sum(player_points) > 21: 
            print(f"{player} BUSTS WITH {sum(player_points)} points!")
            break
        hit_stand_input = input('Hit(h) or Stand(s)')
        if hit_stand_input.lower() == "h":
            player_card, current_deck = deal_card(current_deck,1)
            player_hand.extend(player_card)
            player_points.append(player_card[0].get('card_data').get('points'))
            print(f"{player} received a {player_card[0].get('card_data').get('card')} of {player_card[0].get('card_data').get('suit')}")
            print(f"{player} total => {sum(player_points)}")
        else:
            print(f"{player} stands with total {sum(player_points)}")
            stand = True

    # DEALER PLAYS OUT
    time.sleep(.5)
    while sum(dealer_points) < 17: 
        time.sleep(1)
        dealer_card, current_deck = deal_card(current_deck,1)
        print(f"DEALER received a {dealer_card[0].get('card_data').get('card')} of {dealer_card[0].get('card_data').get('suit')}")
        dealer_points.append(dealer_card[0].get('card_data').get('points'))
    if sum(dealer_points) > 21: 
        print(f"DEALER BUSTS with {sum(dealer_points)}")
    else: 
        print(f"DEALER HAS {sum(dealer_points)}")


    # COMPARE DEALER VALUE TO PLAYER VALUE
    if sum(dealer_points) > sum(player_points):
        new_wallet_value = player_wallet[0] - bet_amount
        player_wallet.pop(0)
        player_wallet.append(new_wallet_value)
        print("DEALER WINS :(")

    elif sum(dealer_points) < sum(player_points):
        new_wallet_value = player_wallet[0] + bet_amount
        player_wallet.pop(0)
        player_wallet.append(new_wallet_value)
        print(f"{player} WINS!")
    else:
        print("PUSH")
    print(f"CURRENT WALLET VALUE: {player_wallet[0]}")
    round +=1

print("GAME OVER")
