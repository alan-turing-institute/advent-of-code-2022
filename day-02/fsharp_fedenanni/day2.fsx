open System.IO
open System

// first Part

let data = File.ReadAllLines("input.txt") |> Array.toList

let rounds = data |> List.map (fun x -> x.Split([| ' ' |]))

let rec score (myStringArray: string[]) =
    let you = myStringArray.[0]
    let me = myStringArray.[1]

    if you = "A" then
        if me = "X" then 4
        else if me = "Y" then 8
        else 3
    else if you = "B" then
        if me = "X" then 1
        else if me = "Y" then 5
        else 9

    else if me = "X" then
        7
    else if me = "Y" then
        2
    else
        6

let scores: int = rounds |> List.map (fun x -> score x) |> List.sum

// second part

let rec remapScore (myStringArray: string[]) =
    let you = myStringArray.[0]
    let outcome: string = myStringArray.[1]

    if outcome = "X" then
        if you = "A" then 3
        else if you = "B" then 1
        else 2

    else if outcome = "Y" then
        if you = "A" then 4
        else if you = "B" then 5
        else 6

    else if you = "A" then
        8
    else if you = "B" then
        9
    else
        7

let second_scores = rounds |> List.map (fun x -> remapScore x) |> List.sum

Console.WriteLine second_scores
