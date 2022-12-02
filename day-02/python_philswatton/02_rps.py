from argparse import ArgumentParser

# Usage: python 02_rps.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="Calculate total score based on a sequence of Rock Paper Scissors Moves")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Function to convert opponent moves to RPS (not strictly necessary, but makes easier)
def opp_to_moves(strategy_list: list[str]) -> list[str]:
    return list(map(lambda strategy: strategy.replace("A", "R").replace("B", "P").replace("C", "S"), strategy_list))

# Part 1: Rock (A, X), Paper (B, Y), Scissors (C, Z)
def strategy_to_game_1(strategy_list: list[str]) -> list[str]:
    strategy_list = opp_to_moves(strategy_list)
    return list(map(lambda strategy: strategy.replace("X", "R").replace("Y", "P").replace("Z", "S"), strategy_list))

# Part 2: dict mapping move to move it will beat
rps_dict = {
    "R": "P",
    "P": "S",
    "S": "R"
}

# Part 2: compute move that will produce a win (Z), loss (X), or draw (Y)
def compute_move(strategy: str) -> str:
    if strategy[2] == "Y":
        move = strategy[0:2] + strategy[0]
    elif strategy[2] == "X":
        move = strategy[0:2] + [mov for mov, opp in rps_dict.items() if opp == strategy[0]][0]
    else:
        move = strategy[0:2] + rps_dict[strategy[0]]
    return move

# Part 2: function that maps the above across a list of strategies
def strategy_to_game_2(strategy_list: list[str]) -> list[str]:
    strategy_list = opp_to_moves(strategy_list)
    return list(map(compute_move, strategy_list))


# Function to score a round of Rock-Paper Scissors.
# Rock 1, Paper 2, Scissors 3
# Rock beats scissors (1 > 3), paper beats rock (2 > 1), scissors beats paper (3 > 2)
# 0 for loss, 3 for draw, 6 for win
def game_to_score(result: str) -> int:
    # Compute win/draw/loss score
    if result[0] == result[2]:
        score = 3
    elif (result[0] == "R" and result[2] == "S") or (result[0] == "P" and result[2] == "R") or (result[0] == "S" and result[2] == "P"):
        score = 0
    else:
        score = 6
    # Add score based on move played
    if result[2] == "R":
        score += 1
    elif result[2] == "P":
        score += 2
    else:
        score += 3
    return score

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        # Process input
        strategy_guide = input_file.read().rstrip()
        strategy_list = strategy_guide.split("\n")
        
        # Part 1: assume X=rock, Y=paper, Z=scissors
        game_list_1 = strategy_to_game_1(strategy_list)
        score_list_1 = list(map(game_to_score, game_list_1))
        print("Part 1 total score: " + str(sum(score_list_1)))
        
        # Part 2: X means lose, Y means draw, Z means win
        game_list_2 = strategy_to_game_2(strategy_list)
        score_list_2 = list(map(game_to_score, game_list_2))
        print("Part 2 total score: " + str(sum(score_list_2)))
        
# Run
if __name__ == "__main__":
    main()