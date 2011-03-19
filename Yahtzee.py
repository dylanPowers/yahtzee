'''
Created on Mar 14, 2011

@author: Dylan
'''

import random
def main():

    title("Let's Play Yahtzee!")
    num_players = get_number_of_players()
    if num_players > 1:
        player_to_go_first(num_players)    
    
    player_scores = {}
    for i in range(13):
        
        for player in range(num_players):
            
            player = player + 1
            if player == 1:
                print("\n"*5 + "<---Player %s's Turn--->" %player)
            else:
                print("\n"*5 + "<---Player %s's Turn--->" %player)
            input("Press ENTER to continue")
            
            dice_shown = roll_dice(range(1,6),{})
                       
            if player_scores.get(player) != None:
                scores = player_scores.get(player)
            else:
                scores = {"1": " ", "2": " ", "3": " ", '4': " ", '5': " ", 
                          '6': " ", 
                          "upper total": " ", "3k": " ",
                          "4k": " ", "full h": " ", "sm straight": " ", 
                          "lg straight": " ", "yahtzee": " ", "?": " "}    
            
            dice = reroll(dice_shown, scores) 
            scores = score_eval(dice, scores)
            player_scores[player]= scores
            scorecard(scores,None)
            input("Press ENTER to complete your turn.")
            
    final_score(player_scores, None)
    input('Press ENTER when finished and your scores will be saved to '
          'a txt file.')
    from datetime import datetime
    date = datetime.now()
    date_name = str(date)
    date_name = date_name.replace(" ", "_")
    date_name = date_name.replace(":", "-")
    scores_to_save = open("Yahtzee_scores_"+date_name+".txt", "w")
    final_score(player_scores, scores_to_save)
    print("\n\n\n\nThe date and time played was", date, file=scores_to_save)
    scores_to_save.close()
    
    

def title(title):
    print("*"*80)
    indent = " "*((80-len(title))//2-1)
    if len('*'+indent+title+indent+'*') == 80:
        print('*'+indent+title+indent+'*')
    elif len('*'+indent+title+indent+'*') == 79:
        print('*'+indent+title+indent+' *')
    else:
        print("Error:\n\tTitle programming error! \n\tTitle most likely" \
              " exceeded the maximum of 78 characters in length.")
    print("*"*80, "\n")

def get_number_of_players():
    error=True
    while error:        
        num_players = input("Please input the number of players:").strip()
        try:
            num_players = int(num_players)
            error = False
        
        except: 
            print("There was a problem interpreting how many players "
                  "there are.")
        
    return num_players

def player_to_go_first(num_of_players):
    
    print("\nFirst we need to decide who goes first. "
          "\nThe player with the highest point total later becomes "
          "Player 1.")
    
    player_points = []
    for player in range(num_of_players):
        player = player + 1
        
        print("\n--Player %s's Turn--" %player)
        input("Press ENTER to continue")
        
        dice_shown = roll_dice(range(1,6),{})
        die_points=0
        for die_key in dice_shown:
            die_points = dice_shown[die_key]+die_points
        print("Player %s's points are:" %player, die_points)
        player_points.append((player,die_points))
        
    player_points = dict(player_points)
    
    highest_points = 0
    for key in player_points:
        
        if player_points[key]>highest_points:
            highest_points = player_points[key]
            highest_player = key
            tie = False
            
        elif player_points[key] == highest_points:
            tie = True
            
    if tie:
        print("There was a tie. Deciding who goes first will now have to be "
              "rerun.")
        player_to_go_first(num_of_players)
    
    else:
        print("\nCongrats! Player %s is now Player 1. By any" %highest_player,
              "means necessary figure out who\nthe rest of the players are.")
        input("Press ENTER when you've figured it out.")    
    
def roll_dice(dice_rolled, dice_kept):
    
    print("\n*Shake...Shake...Shake* Your dice are:")
    dice_shown = []
    for dice in dice_rolled:        
        dice = int(dice)
        dice_number = random.randint(1,6)
        print("Die %s= " %dice, "[%s]" %dice_number)
        dice_shown.append((dice,dice_number))
        if dice in dice_kept:
            del dice_kept[dice]
    
    
    if len(dice_kept) > 0:
        print("\nYour previously kept dice are:")
        for die in dice_kept:            
            print("Die %s= " %die, "[%s]" %dice_kept[die])    
    
    dice_keys = list(dice_kept)
    for key in dice_keys:
        die_key_pair = (key, dice_kept[key])
        dice_shown.append(die_key_pair)
    dice_shown = dict(dice_shown)
    
    return dice_shown 

def reroll(dice_shown, scores):
    
    rolls = 1
    while rolls <=2:
        
        roll_again = input("\nWould you like to roll again?(y/n):").strip()
        roll_again = roll_again.lower()
        
        
        if roll_again == "y":
            error = True
            while error:
                reroll = input("Which dice would you like to roll again? "
                               '(Input in the form "1,2" or "all"): ').strip()
                reroll = reroll.lower()
                if reroll == "all":
                    reroll = range(1,6)
                    error = False
                else:
                    try:                        
                        reroll = reroll.replace(",", " ")
                        reroll = reroll.split(" ")
                        for die_num in reroll:
                            die_num = int(die_num)
                            if 0 < die_num <= 5:
                                error = False
                            else:
                                int("a")
                    
                    except:
                        error = True
                        print("\nThere was a problem, try re-inputting the dice"
                              " you would like to re-roll.\nA shortcut for "
                              "inputing your re-rolls is to "
                              "input with spaces instead of commas.\n")
            dice_shown = roll_dice(reroll, dice_shown)
            rolls = rolls +1
       
        elif roll_again == "n":
            return dice_shown        
        
        elif roll_again == "score":
            scorecard(scores, None)
        
        else:
            print("Was not able to handle your input try again.")
    return dice_shown

def score_eval(dice, score):
    die_nums = []
    for key in dice:
        die_nums.append(dice[key])
        
    three_kind = False
    four_kind = False
    full_house = False
    sm_straight = False
    lg_straight = False
    yahtzee = False
    aces = 0
    twos = 0
    threes = 0
    fours = 0
    fives = 0
    sixes = 0
    all_add = 0
    
    die_nums.sort()
    
    straight_die = 0
    previous_die = 100
    for die in die_nums:
        if die != previous_die:
            die_count = die_nums.count(die)
                   
            if die_count >= 3:
                three_kind = True
                die_pos = die_nums.index(die)
                if die_pos == 0:
                    if die_nums[3] == die_nums[4]:
                        full_house = True
                if die_pos == 2:
                    if die_nums[0] == die_nums[1]:
                        full_house = True
            
            if die_count >= 4:
                four_kind = True
                
            if die_count == 5: 
                yahtzee = True
        
        
        if die == previous_die +1:
            straight_die = straight_die +1
        
        if straight_die >= 3:
            sm_straight = True
        if straight_die == 4:
            lg_straight = True
        
        if die == 1:
            aces = aces + die            
        if die == 2:
            twos = twos + die            
        if die == 3:
            threes = threes + die
        if die == 4:
            fours = fours + die
        if die == 5:
            fives = fives + die
        if die == 6:
            sixes = sixes + die
        
        all_add = all_add + die
        previous_die = die    
    loop = True
    while loop:
        print("\nWhat would you like to input into your "
              'score card?\nType "score" to see your score'
              ' card. Options:\n\t1: Adds ones, 2: Add twos'
              ', 3: Add threes, 4: Add fours, 5: Add fives'
              ', 6: Add sixes \n\t3k: Three of a kind'
              ', 4k: Four of a kind, "Full H": Full house'
              '\n\t"Sm Straight": Small Straight(Sequence of four),'
              ' "Lg Straight": Large Straight(Sequence of five)'
              '\n\t"Yahtzee": Yahtzee(Five of a kind)'
              ', "?": Chance(Sum of all die)')
        scorecard_selection = input('\nYour Selection: ').strip()
    
        scorecard_selection = scorecard_selection.lower()        
        loop = scorecard_input_handler(scorecard_selection, score)
    if scorecard_selection == "1":
        score['1'] = aces
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = score["upper total"]+score['1']
    elif scorecard_selection == "2":
        score['2'] = twos
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = int(score["upper total"])+score['2']
    elif scorecard_selection == "3":
        score['3'] = threes
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = int(score["upper total"])+score['3']
    elif scorecard_selection == "4":
        score['4'] = fours
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = int(score["upper total"])+score['4']
    elif scorecard_selection == "5":
        score['5'] = fives
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = int(score["upper total"])+score['5']
    elif scorecard_selection == "6":
        score['6'] = sixes
        if score["upper total"] == " ":
            score["upper total"] = 0
        score["upper total"] = int(score["upper total"])+score['6']
    elif scorecard_selection == "3k":
        if three_kind == True:
            score["3k"] = all_add   
        else:
            score["3k"] = 0
            print("\nYou did not have a 3 of a kind so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "4k":
        if four_kind == True:
            score["4k"] = all_add
        else:
            score["4k"] = 0
            print("\nYou did not have a 4 of a kind so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "full h":
        if full_house == True:
            score["full h"] = 25
        else:
            score["full h"] = 0
            print("\nYou did not have a full house so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "sm straight":
        if sm_straight == True:
            score["sm straight"] = 30
        else:
            score["sm straight"] = 0
            print("\nYou did not have a small straight so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "lg straight":
        if lg_straight == True:
            score["lg straight"] = 40
        else:
            score["lg straight"] = 0
            print("\nYou did not have a large straight so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "yahtzee":
        if yahtzee == True:
            score["yahtzee"] = 50
        else:
            score["yahtzee"] = 0
            print("\nYou did not have a yahtzee so a 0 will be entered "
                  "in its place.")
    elif scorecard_selection == "?":
        score["?"] = all_add      
               
    return score


def scorecard(scores, file):
    print("\n-Upper Section-"
          "\nAces->\t\t [" + str(scores['1']) + "]"
          "\nTwos->\t\t [" + str(scores['2']) + "]"
          "\nThrees->\t [" + str(scores['3']) + "]"
          "\nFours->\t\t [" + str(scores['4']) + "]"
          "\nFives->\t\t [" + str(scores['5']) + "]"
          "\nSixes->\t\t [" + str(scores['6']) + "]"
          "\nUpper Total->\t [" + str(scores["upper total"]) + "]", file=file)
    try:
        if scores['upper total'] >=63:
            scores['up bonus'] = 35
            print("Bonus->\t\t [" + str(scores['up bonus']) + "]", file=file)
    except:
        pass
        
    print("-Lower Section-"
          "\nThree of a kind->[" + str(scores["3k"]) + "]"
          "\nFour of a kind-> [" + str(scores["4k"]) + "]"
          "\nFull House->\t [" + str(scores["full h"]) + "]"
          "\nSmall Straight-> [" + str(scores["sm straight"]) + "]"
          "\nLarge Straight-> [" + str(scores["lg straight"]) + "]"
          "\nYahtzee->\t [" + str(scores["yahtzee"]) + "]"
          "\nChance->\t [" + str(scores["?"]) + "]", file=file)

def scorecard_input_handler(scorecard_selection, score):
    if scorecard_selection == "score":
        scorecard(score, None)
        loop = True
        return loop
    selection = {"1": "Adds ones", '2': 'Add twos', '3': 'Add threes', 
                 '4': 'Add fours', '5': 'Add fives', '6': 'Add sixes', 
                 '3k': 'Three of a kind', '4k': 'Four of a kind', 
                 'full h': 'Full house', 
                 'sm straight': 'Small Straight(Sequence of four)', 
                 'lg straight': 'Large Straight(Sequence of five)', 
                 "yahtzee": 'Yahtzee(Five of a kind)', "?": 'Chance'}
    
    try:
        select_def = selection[scorecard_selection]
        print("You selected", select_def + "." )
        user_cont = input("Are you sure you want to make "
                          "this selection?(y/n):").strip().lower()
        if user_cont == "y":
            loop = False
            for key in score:
                if scorecard_selection == key:                    
                    if score[key] != " ":                        
                        loop = True
                        print("\nYou have already entered that selection into "
                              "your score card.\nYou can only enter each "
                              "selection once into your score card.")
                        
        else:
            print("Try again we go.")
            loop = True
        
        
    except:
        print("Your selection was not valid. Try again.") 
        loop = True     
        
    return loop

def final_score(player_scores, file):
    highest_points = 0
    for player in player_scores:
        scores = player_scores[player]
        print("\n\n-------->Player", str(player)+ "'s final score is:<--------",
              file = file)
        scorecard(scores, file)
        total_points = 0
        for points in scores:
            if points != "total points":
                if points != "upper total":
                    total_points = scores[points] + total_points
        print("##Total Points-> [" +str(total_points)+ ']', file=file)
        
        scores['total points'] = total_points
        
        if scores['total points'] > highest_points:
            highest_points = scores['total points']
            highest_player = player
            tie_players = [highest_player]
            tie = False
            
        elif scores['total points'] == highest_points:            
            tie_players.append(player)
            tie = True
    
    if tie == False:
        print("\n\n!!!!!!!!!!!!!Player", str(player),
              "is the WINNER!!!!!!!!!!!!!!!=D", file=file)
        
    elif tie == True:
        print("\n\nThere was a tie between players", end=" ", file=file)
        num_tied = len(tie_players)
        for i in tie_players:            
            if i == num_tied - 1:
                print(tie_players[i], end=" ", file=file)
            
            else:
                print(tie_players[i], "and", end=" ", file=file)
        print("!!!!!!!!!!!!!=O"
              "\nI guess you'll just have to share the trophy =|", file=file) 
            
if __name__ == '__main__':
    main()