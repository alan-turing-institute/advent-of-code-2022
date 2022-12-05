(* Advent of Code - Day 2
Rock, Paper, Scissors strategy guide.
*)

let INPUT_FILEPATH = "day-02/fsharp_lannelin/input.txt"

// map the text of opp moves to consistent
let OPP_MOVE_MAP =
    [ 'A', 'R'; 'B', 'P'; 'C', 'S' ] // R: rock, P: paper, S: scissors
    |> dict

// map the text of our moves to consistent (part 1)
let OUR_MOVE_MAP =
    [ 'X', 'R'; 'Y', 'P'; 'Z', 'S' ] // R: rock, P: paper, S: scissors
    |> dict

// map the text of outcomes to scores (part 2)
let OUTCOME_MAP =
    [ 'X', 0; 'Y', 3; 'Z', 6 ] // 0: loss, 3: draw, 6: win
    |> dict

// each item has a score for just playing it
let PLAY_SCORE_MAP =
    [ 'R', 1; 'P', 2; 'S', 3 ] // R: 1, P: 2, S: 3
    |> dict


// parse each line into tuple - format "{opponent move} {our move}"
let parseLinePart1 (roundString: string) =
    ((OPP_MOVE_MAP.Item roundString[0]), OUR_MOVE_MAP.Item roundString[2])


// parse each line into tuple - format "{opponent move} {desired outcome}"
let parseLinePart2 (roundString: string) =
    ((OPP_MOVE_MAP.Item roundString[0]), OUTCOME_MAP.Item roundString[2])

// take a string input, trim and split, parse each line
let parseInput (input: string) (lineParser) =
    // trim and split by line
    input.Trim().Split "\n" |> Array.map (fun line -> lineParser line) // TODO why can't I just use `lineParser line` rather than lambda?


// produce a score for win,loss,draw
// round will be of format
let scoreRound (round: char * char) =
    // directly index string to check for draw
    if fst round = snd round then
        3 //draw
    else
        match round with
        | ('S', 'R') -> 6 // rock beats scissors
        | ('R', 'P') -> 6 // paper beats rock
        | ('P', 'S') -> 6 // scissors beats paper
        | _ -> 0


// short input given to us as part of the challenge to dev against
let debugInput: string =
    "A Y
B X
C Z"

let getAnswer1 (input: string) =
    (parseInput input parseLinePart1)
    |> Array.map (fun round -> (scoreRound round) + (PLAY_SCORE_MAP.Item(snd round)))
    |> Array.sum



let dayInput: string = System.IO.File.ReadAllText INPUT_FILEPATH

printfn "answer 1 DEBUG: %d ...  should be 15" (getAnswer1 debugInput)
printfn "answer 1: %d" (getAnswer1 dayInput)


// allow match failures here if we get them
let produceOutcome round =
    // directly index string to check for draw
    if snd round = 3 then // draw
        fst round // return same

    elif snd round = 0 then //loss
        match fst round with
        | ('R') -> 'S' // rock beats scissors
        | ('P') -> 'R' // paper beats rock
        | ('S') -> 'P' // scissors beats paper

    else // win
        match fst round with
        | ('S') -> 'R' // rock beats scissors
        | ('R') -> 'P' // paper beats rock
        | ('P') -> 'S' // scissors beats paper

// part 2, turns out we should actually look up what move we should make, we're not told
let getAnswer2 (input: string) =
    (parseInput input parseLinePart2)
    |> Array.map (fun round -> (snd round) + (PLAY_SCORE_MAP.Item(produceOutcome round)))
    |> Array.sum

printfn "answer 2 DEBUG: %d ...  should be 12" (getAnswer2 debugInput)
printfn "answer 2: %d" (getAnswer2 dayInput)
