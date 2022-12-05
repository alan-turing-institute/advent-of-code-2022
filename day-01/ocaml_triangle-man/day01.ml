(** Advent of Code: Day 1

    Shamelessly adapted (well, copied) from Evelina's F# code. *)

open List

let testInput = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"

(* It's "compare" backwards ... *)
let erapmoc a b = ~- (Int.compare a b) 

let input =
  testInput
  |> Str.split (Str.regexp "\n\n") 
  |> List.map (String.split_on_char '\n')

let elfCalories =
  input
  |> map (map int_of_string)
  |> map (fold_left (+) 0)

(* Part 1 *)

let maxCalories =
  elfCalories
  |> fold_left max min_int

(* Part 2 *)

let top3 =
  elfCalories
  |> sort erapmoc
  |> to_seq
  |> Seq.take 3
  |> Seq.fold_left (+) 0
