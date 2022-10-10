#---------------------------#
#---- B L A C K J A C K ----#
#---------------------------#
# 8 decks
# Dealer plays 3:2 on blackjack
# Dealer stands on 17

import random
import time

def create_decks(number_of_decks):
    """
    Given a number_of_decks, create that many decks of playing cards. Each deck is 50 cards (excluding jokers)
    """
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

def shuffle_deck(deck): 
    """
    Given a card deck, return the deck shuffled, and provide the card with its index
    """
    shuffled_deck = random.sample(deck,len(deck))
    shuffled_indexed_deck = []
    for card in shuffled_deck:
        index_payload = {
            "index":shuffled_deck.index(card),
            "card_data":card
        }
        shuffled_indexed_deck.append(index_payload)
    return shuffled_indexed_deck
 
def deal_card(deck,number_of_cards):
    """
    Return number_of_cards cards from a given deck
    """
    cards = deck[0:number_of_cards]
    for i in range(number_of_cards):
        deck.pop(0)
    return cards, deck

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
        
def calculate_hand_value(hand):
    """
    Given a hand, calculate the point value of the hand.
    """
    # handle for ace
    if 11 in hand and sum(hand) > 21:
         hand.remove(11)
         hand.append(1)
         hand_value = sum(hand)
    else: 
        hand_value = sum(hand)
    return hand_value

def calculate_winner(dealer_points,player_points,dealer_bust,player_bust):
    """
    Given the point values for the dealer and player hands, determine who won
    """
    dealer_points = calculate_hand_value(dealer_points)
    player_points = calculate_hand_value(player_points)
    if (player_bust or dealer_points > player_points) and not dealer_bust:
        print("-------------------------------------------")
        print(f"DEALER WINS :( {dealer_points} - {player_points}")
        print("-------------------------------------------")
        return "LOSS"
    elif dealer_bust or dealer_points < player_points:
        print("-------------------------------------------")
        print(f"{player} WINS! {player_points} - {dealer_points}")
        print("-------------------------------------------")
        return "WIN"
    else:
        print("-------------------------------------------")
        print(f"PUSH {player_points} - {dealer_points} - you get your money back *rolling my eyes* ")
        print("-------------------------------------------")
        return "PUSH"
        
def update_wallet_value(result,player_wallet,player_blackjack):
    """
    Update the value of the player's wallet depending on the game result
    """
    # player_wins
    if result == 'WIN':
        if player_blackjack:
            new_wallet_value = player_wallet[0] + bet_amount*1.5
        else:
            new_wallet_value = player_wallet[0] + bet_amount
        player_wallet.pop(0)
        player_wallet.append(new_wallet_value)
        return f"{bet_amount*2} added to wallet"

    elif result == 'LOSS': 
        new_wallet_value = player_wallet[0] - bet_amount
        player_wallet.pop(0)
        player_wallet.append(new_wallet_value)
        return f"{bet_amount} subtracted from wallet"
    else: 
        return f"{bet_amount} returned to wallet"


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
# initialize the game
if round == 0:
    print("starting new round")
    time.sleep(.5)
    print("here's 100 bucks, you filthy animal.")
    # add 100 starting points to the player's wallet
    player_wallet.append(100)
print(f"{player}'s wallet: {sum(player_wallet)}")

# play until there are no more cards left in the deck, or the player has no more points
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


    # Tell the user the dealer's first card
    for card in dealer_hand:
        dealer_points.append(card.get('card_data').get('points'))
        if dealer_hand.index(card) == 0:
            print(f"DEALER HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")    
    total_dealer_points = calculate_hand_value([dealer_points[0]])
    print(f"DEALER TOTAL: {total_dealer_points}")

    # Tell the player what cards they have
    for card in player_hand:
        player_points.append(card.get('card_data').get('points'))
        print(f"{player} HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")
    total_player_points = calculate_hand_value(player_points)
    print(f"PLAYER TOTAL: {total_player_points}")

    # check for blackjacks on the first draw
    player_blackjack = False
    dealer_blackjack = False
    if total_player_points == 21 and total_dealer_points != 21: 
        print(f"{player} BLACKJACK")
        player_blackjack = True
    elif total_player_points != 21 and total_dealer_points == 21: 
        print("DEALER BLACKJACK")
        dealer_blackjack = True
    
    ### PLAYER ###
    # ask the player to hit or stand
    player_stand = False
    player_bust = False
    while not player_stand and not player_bust and not player_blackjack and not dealer_blackjack:
        # player busts
        if sum(player_points) > 21: 
            print(f"{player} BUSTS WITH {calculate_hand_value(player_points)} points!")
            player_bust = True
            break
        hit_stand_input = input('Hit(h) or Stand(s)')
        # player hits
        if hit_stand_input.lower() == "h":
            player_card, current_deck = deal_card(current_deck,1)
            player_hand.extend(player_card)
            player_points.append(player_card[0].get('card_data').get('points'))
            print(f"{player} received a {player_card[0].get('card_data').get('card')} of {player_card[0].get('card_data').get('suit')}")
            print(f"{player} HAS: {calculate_hand_value(player_points)}")
        # player stands
        else:
            print(f"{player} stands with total {calculate_hand_value(player_points)}")
            player_stand = True



    ### DEALER ### 
    # Show dealer next card
    dealer_next_card = dealer_hand[1]
    print(f"DEALER second card was a {dealer_next_card.get('card_data').get('card')} of {dealer_next_card.get('card_data').get('suit')}")
    
    # dealer plays out
    dealer_stand = False
    dealer_bust = False
    time.sleep(.5)
    while not dealer_blackjack and not dealer_stand and not dealer_bust and not player_blackjack and not player_bust:
        time.sleep(1)
        if calculate_hand_value(dealer_points) > 21: 
            print(f"DEALER BUSTS with {calculate_hand_value(dealer_points)}")
            dealer_bust = True
        if calculate_hand_value(dealer_points) < 17: 
            dealer_card, current_deck = deal_card(current_deck,1)
            print(f"DEALER received a {dealer_card[0].get('card_data').get('card')} of {dealer_card[0].get('card_data').get('suit')}")
            dealer_hand.extend(dealer_card)
            dealer_points.append(dealer_card[0].get('card_data').get('points'))
        else: 
            print(f"DEALER HAS {calculate_hand_value(dealer_points)}")
            dealer_stand = True

    # determine the winner, update the player's wallet, and print the results
    play_result = calculate_winner(dealer_points,player_points,dealer_bust,player_bust)
    update_wallet_value(play_result, player_wallet,player_blackjack)
    print(f"CURRENT WALLET VALUE: {player_wallet[0]}")
    print("-------------------------------------------")
    print("-------------------------------------------")
    round +=1
print("GAME OVER")