import random
import time

def print_ver(card):
    return str(card[0])+card[1]

def print_res(res):
    if res == 'l':
        print('You lost.')
    elif res == 't':
        print('It is a tie.')
    elif res == 'w':
        print('You won.')
    elif res == 'bj':
        print('You won 3 to 2.')
    elif res == 'ins': #  option to win insurance
        print('You lost your original bet.')

def quit():
    dec = input("Are you sure you want exit a game. Press 'Enter' if yes or any other keybord to return back in the game.")
    if dec == '':
        return True
    else:
        return False

def place_bet(points):
    ''' Asks user for bet, control input and return bet '''
    max_bet = 200 # setup manualy
    if points < max_bet:
        max_bet = points//10*10
    try:
        x = int(input('Press 0 to exit game.\nNew bet: '))
    except ValueError:
        print(f"Insert a number betwenn 10 and {max_bet} divisible by 10.")
        return place_bet(points)
    else:
        if x == 0 : # ask user if he wants to exit a game
            if quit() == True:
                return x # x = 0 -> exit a game
            else:return place_bet(points)
        elif x < 10 or x > max_bet or x % 10 != 0:
            print(f"Insert a number betwenn 10 and {max_bet} divisible by 10.")
            return place_bet(points)
        elif x > points:
            print(f"You have {points} points. You can't bet more than you currently have.")
            return place_bet(points)
        else:
            return x

def ins_bet(points,bet):
    ''' Asks user for insurance_bet, control input and return insurance_bet '''
    if points < 5:
        return 0
    print('Do you want place your insurance bet? If dealer draw BlackJack you lose your original bet, but you win your insurance bet 2 to 1.')
    max_bet = int(bet/2)
    if max_bet > points:
        print(f'You have {points} left on your account.')
        max_bet = points

    while True:
        if bet == 10 or points <= 10:
            print(f"Insert 0 for NO INSURANCE or {max_bet} for INSURANCE.")
        else:
            print(f"Insert 0 for NO INSURANCE or any number divisible by 5 up to {max_bet} for INSURANCE.")

        y = input("Your insurance: ")
        try:
            x =int(y)
        except ValueError:
            print('Incorrect input. ',end='')
            continue
        if x<= max_bet and x%5==0:
            return x
        else:
            print('Incorrect input. ',end='')
            continue

def decision(double_down=False,split = False):
    '''Ask user for decision depending on current options, control input'''
    if double_down:
        if split:
            dec = input("Hit('H') or Stand('S') or Double('D') or Split('B')?: ").lower().strip()
        else:
            dec = input("Hit('H') or Stand('S') or Double('D') ?: ").lower().strip()
    else:
        dec = input("Hit('H') or Stand('S'):  ").lower().strip()
    try:
        x = dec[0]
    except IndexError:
        print("Please write 'H' or 'Hit' if you want another card or 'S' or 'Stand' if you don't.")
        if double_down:print("In case you want to double your bet, write 'D' or 'Double.")
        if split:print("In case you want to split your cards, write 'B' or 'Break.")
        return decision(double_down,split)
    if x == 'h':
        return dec[0]
    elif x == 's':
        return dec[0]
    elif x == 'b' and split:
        return dec[0]
    elif x == 'd' and double_down:
        return dec[0]
    else:
        print("Please write 'H' or 'Hit' if you want another card or 'S' or 'Stand' if you don't.")
        if double_down:print("In case you want ot double your bet, write 'D' or 'Double.")
        if split:print("In case you want to split your cards, write 'B' or 'Beak.")
        return decision(double_down,split)



def burn_three_cards():
    ''' move three cards from deck to locked'''
    for i in range(3):
        locked.append(deck.pop())

def new_shuffle():
    ''' move all cards from locked to deck and shuffle '''
    for i in range(len(locked)):
        deck.append(locked.pop())
    print()
    print('NEW SHUFFLE')
    print()
    time.sleep(1)
    random.shuffle(deck)

def deal():
    ''' give two cards from deck to player and one to dealer'''
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())
    player_cards.append(deck.pop())

def total(cards):
    ''' return (['BJ|soft|hard'],sum(value of all cards))'''
    if len(cards)==2:
        if cards[0][0] == 'A' and cards[1][0] in [10,'J','Q','K'] or cards[1][0] == 'A' and cards[0][0] in [10,'J','Q','K']:
            return ('BJ',21)
    total = 0
    num_aces = 0
    for card in cards:
        if card[0] in ['J','Q','K']:
            total += 10
        elif card[0] == 'A':
            num_aces += 1
        else:
            total += card[0]

    if num_aces > 0: # only one ace can have value of 11 not to be over 21
        if total + 11 + (num_aces - 1)*1 <= 21:
            aces_value = 11 + (num_aces - 1)*1
            return ('soft',total+aces_value)
        else:
            aces_value = num_aces*1
            return ('hard',total+aces_value)

    return ('hard',total)

def split_available(cards):
    ''' Return true if two cards has same value '''
    tens = [10,'J','Q','K']
    if cards[0][0] == cards[1][0]:
        return True
    elif cards[0][0] in tens and cards[1][0] in tens:
        return True
    else: return False

def player_draw(cards,points,bet,split,no_more_split,aces):
    ''' return Split, Double or None, depens on players decision.
    Repeating till player has over 21 or he decided not to take anymore cards'''
    no_more_card =  False # is True when player double_down
    while True:
        current = total(cards)
        if current[0] == 'BJ' and not split :
            print('You have BJ')
            break
        elif current[1] > 21:
            print('You have too many.')
            if no_more_card:return 'double'
            break
        elif current[1] == 21:
            print('You have 21')
            if no_more_card:return 'double'
            break
        else:
            if current[0] == 'hard' or no_more_card == True or aces:
                print(f'You have {current[1]}. ',end='')
                if aces:
                    print('')
                    break
                if no_more_card:
                    print('No more cards')
                    return 'double'
            elif current[0] == 'soft':
                print(f'You have {current[1]-10} or {current[1]}. ',end='')

            if split_available(player_cards) and points >= bet and not no_more_split:
                 print('Split available')
                 possible_split = True # this option will be in decision()
            else:possible_split = False

            if len(cards) == 2 and points >= bet: # player can double eny two cards
                possible_double_down = True # this option will be in decision()
            else:
                possible_double_down = False

            d = decision(possible_double_down,possible_split)
            if d == 'b':#split
                return 'split'
            elif d == 's':# no more cards
                break
            elif d =='h': # taking new card
                new_card = deck.pop()
                print(f'Your new card is {print_ver(new_card)}.')
                cards.append(new_card)
            elif d =='d':#double,only one card
                new_card = deck.pop()
                print(f'Double down = only one card. Your card is {print_ver(new_card)}. ')
                cards.append(new_card)
                no_more_card =  True

def dealer_draw(cards,ins=None):
    if ins is not None:
        # runs only when player is over 21 and need to check if insurance_bet won,
        # if next cards value is 10, it is BJ.
        new_card = deck.pop()
        print(f'Dealer has Ace. He takes another card. It is {print_ver(new_card)}.')
        cards.append(new_card)
        current = total(cards)
        if current[0] == 'BJ':
            print('Dealer has BJ')
        else: # no need to take more cards
            print('No Black Jack for dealer.')
        return None
    while True: # taking cards until 17.
        current = total(cards)
        if current[0] == 'BJ':
            print('Dealer has BJ')
            break
        elif current[1] > 21:
            print('Dealer has too many.')
            break
        elif current[0] == 'soft' and current[1] <= 17: #He must hit on soft 17
            new_card = deck.pop()
            print(f'Dealer has {current[1]-10} or {current[1]}. He takes another card. It is {print_ver(new_card)}.')
            cards.append(new_card)
        elif current[0] == 'hard' and current[1] < 17:
            new_card = deck.pop()
            print(f'Dealer has {current[1]}. He takes another card. It is {print_ver(new_card)}.')
            cards.append(new_card)
        else:
            print(f'Dealer has {current[1]}. He stays.')
            break

def compare(dc,pl):
    ''' decide if dealer is better than player. Return l|w|t '''
    dealer = dc[1]
    player =pl[1]
    if player > 21 or dc[0]== 'BJ':
        return 'l'
    elif dealer > 21 or player>dealer:
        return 'w'
    elif player == dealer:
        return 't'
    else:return 'l' # dealer > player,but not over 21

def update_points(res,points,bet):
        if res == 'l':
            return points
        elif res == 't':
            return points+bet # get his bet back
        elif res == 'w':
            return points+bet+bet # get his bet back + win
        elif res == 'bj':
            return int(points+bet+bet*1.5) # get his bet back + win 150%
        elif res == 'ins':# in case you lose game but won insurance
            return points

def boxes_vs_dealer(points,boxes_res,dc):
    ''' loop throuh all boxes, decides if box is better than dealer and update points'''
    points_in_game = points
    for key,value in boxes_res.items():
        if len(value) == 0:break

        score = value[1]
        if score > 21: score ='Over 21'
        bet = value[0]
        res = compare(dc,value)
        print(key.replace('res','BOX'),f'bet {bet}, {score} points. ',end='')
        print_res(res)
        points_in_game = update_points(res,points_in_game,bet)
    return points_in_game

def collect_cards(cards):
    '''Move cards after the game to locked '''
    for i in range(len(cards)):
        locked.append(cards.pop())












# create one deck of cards
o_deck = [(value,suit) for suit in ["\u2660", "\u2665", "\u2666", "\u2663"] for value in ['A']+list(range(2,11))+['J','Q','K']]

n_decks = 6 # with how many deck of cards do we play
deck = [card for card in o_deck for o_deck in range(n_decks)] # o_deck* 6
locked = []
dealer_cards = []
player_cards = []
points = 100 # can be change.game setup: minbet= 10, max_bet = 200
next_game = True

#_________ new shuffle_________
new_shuffle()
burn_three_cards()

#_______ new bets __________
while next_game:
    print()
    print(f'Current points: {points}')
    if points < 10: # end of game
        break
    bet = place_bet(points) # option to exit game by inserting 0
    if bet == 0:
        break
    points -= bet
    # vars needed for game
    insurance_bet = None
    double = False
    dealer_turn = False
    res = None
    split = False
    aces = False
    boxes_left = 1
    no_more_split = False

    if len(deck) < (n_decks*len(o_deck))/3: # less than 1/3 cards left
        new_shuffle()
        burn_three_cards()

    deal()
    # dealer_cards = [('A',"\u2660")]
    # player_cards = [(5,"\u2660"),(5,"\u2660")]
    print('player: ',[print_ver(x) for x in player_cards])
    print('dealer: ', [print_ver(x) for x in dealer_cards])

    # boxes will be used in case of split
    boxes= {'box1':[],'box2':[],'box3':[],'box4':[]}
    boxes_res = {'res1':[],'res2':[],'res3':[],'res4':[]}
    n = 1 # box numer

    if dealer_cards[0][0] == 'A' and total(player_cards)[0] != 'BJ':
        insurance_bet = ins_bet(points,bet) # ask for user input
        points -= insurance_bet

    while boxes_left > 0:

        if split:
            if len(player_cards) != 0:
                # moving players card into two different boxes
                boxes['box'+str(n)].append(player_cards.pop(0))
                if len(boxes['box'+str(n+1)]) == 0:# if next box is empty
                    boxes['box'+str(n+1)].append(player_cards.pop(0))
                elif len(boxes['box'+str(n+2)]) == 0:# or another box is empty
                    boxes['box'+str(n+2)].append(player_cards.pop(0))
                elif len(boxes['box'+str(n+3)]) == 0:
                    boxes['box'+str(n+3)].append(player_cards.pop(0))
                boxes_left += 1

            #another card for box n
            print('box'+str(n)+' taking another card ',end='')
            new_card = deck.pop()
            print(f'{print_ver(new_card)}.')
            boxes['box'+str(n)].append(new_card)

            #cards from box(n) becoming players card
            player_cards.append(boxes['box'+str(n)].pop(0))
            player_cards.append(boxes['box'+str(n)].pop(0))
            print('PLAYING BOX'+str(n),end = '')
            print(': ',[print_ver(x) for x in player_cards])

        if len(boxes['box4']) != 0:
            # Already splitted 3 times. No empty box. No more splits allowed.
            no_more_split = True

        game = player_draw(player_cards,points,bet,split,no_more_split,aces)


        if game =='split':
            if player_cards[0][0] == 'A' and player_cards[1][0] == 'A':# check for A,A
                aces = True
            split = True
            points -= bet
            continue # split game into more boxes

        if game == 'double':
            points -= bet
            bet += bet

        pl = total(player_cards)
        player = pl[1]

        if split: # saving results and players card into boxes_res
            boxes['box'+str(n)] = player_cards.copy()
            boxes_res['res'+str(n)].append(bet)
            boxes_res['res'+str(n)].append(player)
            player_cards.clear() # keep empty when next box is turn
            boxes_left -= 1
            if game == 'double':
                bet -= int(bet/2) # set bet to original in while loop
            n +=1 # box is done,move to next one
            if boxes_left == 0:# no more boxes to play
                dealer_turn = True
        else: # not split, regular game
            if pl[0] == 'BJ':
                if dealer_cards[0][0] not in [10,'J','Q','K','A']:
                    res = 'bj'
                else:
                    current = total(dealer_cards)
                    new_card = deck.pop()
                    print(f'Dealer has {current[1]}. He takes another card. It is {print_ver(new_card)}.')
                    dealer_cards.append(new_card)
                    if total(dealer_cards)[0] == 'BJ': res = 't'
                    else: res = 'bj'
            elif player > 21  and insurance_bet:
                res = 'ins'#  option to win insurance
                collect_cards(player_cards)
                dealer_draw(dealer_cards,insurance_bet)
            elif player > 21:
                res = 'l'
                collect_cards(player_cards)
            else:dealer_turn = True
            boxes_left -= 1

    #_______DEALER TURN
    #if all boxes by split are over 21 and insurance is placed
    if split and insurance_bet and all(point > 21 for point in [r[1] for r in list(boxes_res.values())if r]):
        dealer_draw(dealer_cards,insurance_bet)
        dealer_turn = False

    # if we need dealer to find out winner
    if dealer_turn:dealer_draw(dealer_cards)

    dc = total(dealer_cards)
    dealer =dc[1]

    #_______Final compare,printing results, and updating points
    if not split:
        if res is None:
            res = compare(dc,pl)
        print_res(res)
        points = update_points(res,points,bet)
    else: # split, compare each box individualy
        points = boxes_vs_dealer(points,boxes_res,dc)

    if insurance_bet and total(dealer_cards)[0]=='BJ':
        print('You won insurance bet 2 to 1')
        points += insurance_bet+insurance_bet*2
        insurance_bet = None

    # move all played cards to locked
    collect_cards(player_cards)
    for box,cards in boxes.items():
        collect_cards(cards)
    collect_cards(dealer_cards)
    print('===============================================')

print('Ended ')
