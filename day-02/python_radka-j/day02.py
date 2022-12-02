# ROCK PAPER SCISSORS

# read input file
with open('input02.txt') as f:
    lines = f.read().splitlines()

# in part 1, interpret each letter as a move
map = {
    "A": "rock", 
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors"
}

# each move I can play has a score
scores = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

# dictionary of what each option wins/loses over
winning_combos = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
losing_combos = {v:k for k,v in winning_combos.items()}

# variables to track the final result
part_1_score = 0
part_2_score = 0

for line in lines:

    # parse what each player played
    opponent, me = line.split(" ")
    play_opponent = map[opponent]
    
    #========================================================
    # part 1: read X,Y,Z as what I should play + update score
    #========================================================
    play_me = map[me]
    part_1_score += scores[play_me]
    # draw
    if play_opponent == play_me:
        part_1_score += 3
    # win
    elif play_opponent == winning_combos[play_me]:
        part_1_score += 6
    # loss means score of 0, don't need to update

    #========================================================
    # part 2: X=lose, Y=draw, Z=win
    # --> determine what I should play and update score
    #========================================================
    if me == "Y":
        play_me = play_opponent
        part_2_score += scores[play_me]
        part_2_score += 3

    elif me == "X":
        play_me = winning_combos[play_opponent]
        part_2_score += scores[play_me]
        # loss so part_2_score += 0
    else:
        play_me = losing_combos[play_opponent]
        part_2_score += scores[play_me]
        part_2_score += 6
    

print("part 1:", part_1_score)
print("part 2:", part_2_score)
