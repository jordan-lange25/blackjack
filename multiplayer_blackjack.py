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

def place_bet(player_name,wallet_value): 
    """
    Ensure the submitted input value is a number and that the player can afford the bet.
    """
    bet_input = ""
    sufficient_funds = False
    while type(bet_input) != int or sufficient_funds is False: 
        bet_input = input(f"{player_name} how much would you like to bet?")
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

def calculate_winner(player_name,dealer_points,player_points,dealer_bust,player_bust):
    """
    Given the point values for the dealer and player hands, determine who won
    """
    dealer_points = calculate_hand_value(dealer_points)
    player_points = calculate_hand_value(player_points)
    if (player_bust or (dealer_points > player_points and not dealer_bust)):
        print("-------------------------------------------")
        print(f"{player_name} LOSES :( {dealer_points} - {player_points}")
        return "LOSS"
    elif dealer_bust or dealer_points < player_points:
        print("-------------------------------------------")
        print(f"{player_name} WINS {player_points} - {dealer_points}")
        return "WIN"
    else:
        print("-------------------------------------------")
        print(f"{player_name} PUSH {player_points} - {dealer_points}")
        return "PUSH"

def update_wallet_value(bet_amount,result,player_wallet,player_blackjack):
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
print('''-----------------------------------------------------''')
print('''-----------------------------------------------------''')
print('''-----------WELCOME TO MULTIPLAYER BLACKJACK!---------''')
print('''-----------------------------------------------------''')
print('''-----------------------------------------------------''')
players = []
player_count = input("How many players?")
for player_num in range(1,int(player_count)+1):
    player_name = input(f"Player {player_num} what is your name?")
    player_obj = {
            "num": player_num,
            "name": player_name,
            "bet_amount":0,
            "wallet": [],
            "hand": [],
            "points": [],
            "blackjack": False,
            "bust": False,
            "stand": False,
            "out": False
            }
    players.append(player_obj)

# initialize the first round of the game
round = 0
if round == 0:
    print("starting new round")
    time.sleep(.5)
    print("Here's 100 bucks, you filthy animals.")
    # add 100 starting points to the player's wallet
    for player in players:
        wallet = player.get('wallet')
        wallet.append(100)
        print(f"{player.get('name')}'s wallet: {sum(wallet)}")
    print("")

# create the deck (8 hands)
playing_deck = create_decks(8)
shuffled_deck = shuffle_deck(playing_deck)
print("deck assembled! Let's begin.")
print("")
# play until there are no more cards left in the deck, or the player has no more points
while len(shuffled_deck) != 0:
    # INITIALIZE ROUND
    dealer_points = []
    dealer_hand = []
    dealer_cards, current_deck = deal_card(shuffled_deck,2)
    dealer_hand.extend(dealer_cards)
    dealer_blackjack = False
    dealer_bust = False
    
    # clear the hand and points 
    for player in players:
        if not player.get('out'):
            player.get('hand').clear()
            player.get('points').clear()
            player["bet_amount"] = 0
            player["blackjack"] = False 
            player["bust"] = False
            player["stand"] = False
                        
            # choose your bet
            bet_amount = place_bet(player.get('name'), sum(player.get('wallet')))
            player["bet_amount"] = bet_amount
            # deal two cards to the player and the dealer
            player_cards, current_deck = deal_card(current_deck,2)
            player.get('hand').extend(player_cards)
            # Tell the player what cards they have
            for card in player.get('hand'):
                player.get('points').append(card.get('card_data').get('points'))
                print(f"{player.get('name')} HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")
            total_player_points = calculate_hand_value(player.get('points'))
            print(f"{player.get('name')} TOTAL: {total_player_points}")
            print("")
    print("")

    # Tell the user the dealer's first card
    for card in dealer_hand:
        dealer_points.append(card.get('card_data').get('points'))
        if dealer_hand.index(card) == 0:
            print(f"DEALER HAS: {card.get('card_data').get('card')} of {card.get('card_data').get('suit')}")    
    total_dealer_points = calculate_hand_value([dealer_points[0]])
    print(f"DEALER TOTAL: {total_dealer_points}")
    print("")

    # check for any blackjacks
    for player in players:
        if not player.get('out'):
            if  sum(player.get('points'))== 21 and total_dealer_points != 21: 
                print(f"{player.get('name')} BLACKJACK")
                player["blackjack"] = True
            elif total_player_points != 21 and total_dealer_points == 21: 
                print("DEALER BLACKJACK")
                dealer_blackjack = True

        ### PLAYER ###
        # ask the player to hit or stand
        while not player.get('stand') and not player.get('bust') and not player.get('blackjack') and not dealer_blackjack:
            # player busts
            if sum(player.get('points')) > 21: 
                print(f"{player.get('name')} BUSTS WITH {calculate_hand_value(player.get('points'))} points!")
                player["bust"] = True
                break
            hit_stand_input = input(f"{player.get('name')} Hit(h) or Stand(s)?")
            # player hits
            if hit_stand_input.lower() == "h":
                player_card, current_deck = deal_card(current_deck,1)
                player.get('hand').extend(player_card)
                player.get('points').append(player_card[0].get('card_data').get('points'))
                print(f"{player.get('name')} received a {player_card[0].get('card_data').get('card')} of {player_card[0].get('card_data').get('suit')}")
                print(f"{player.get('name')} HAS: {calculate_hand_value(player.get('points'))}")
            # player stands
            else:
                print(f"{player.get('name')} stands with total {calculate_hand_value(player.get('points'))}")
                player["stand"] = True
        print("")
        print("")
    ### DEALER ### 
    # Show dealer next card
    dealer_next_card = dealer_hand[1]
    print(f"DEALER second card was a {dealer_next_card.get('card_data').get('card')} of {dealer_next_card.get('card_data').get('suit')}")
    print("")
    # dealer plays out
    dealer_stand = False
    dealer_bust = False
    time.sleep(.5)

    # Dealer plays out
    while not dealer_blackjack and not dealer_stand and not dealer_bust:
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
    
    # Calculate winners and losers
    # determine the winner, update the player's wallet, and print the results
    for player in players:
        if not player.get('out'):
            play_result = calculate_winner(player.get('name'),dealer_points,player.get('points'),dealer_bust,player.get('bust'))
            update_wallet_value(player.get('bet_amount'), play_result, player.get('wallet'),player.get('blackjack'))
            print(f"{player.get('name')} WALLET VALUE: {player.get('wallet')[0]}")
            if player.get('wallet')[0] <= 0:
                player["out"] = True
                print(f"{player.get('name')} IS OUT YOU FUCKIN LOSER")
    round +=1