open Aoc22_ocaml

(* Encoding:
   1: Rock
   2: Paper
   3: Scissors
*)

let example_lines = [ "A Y"; "B X"; "C Z" ]

let map_opponent = function
  | "A" -> 1
  | "B" -> 2
  | "C" -> 3
  | x -> raise (Invalid_argument x)
;;

let map_me_part1 = function
  | "X" -> 1
  | "Y" -> 2
  | "Z" -> 3
  | x -> raise (Invalid_argument x)
;;

(* Assuming a game has been mapped with the two functions above, apply the correction
   learned in part 2. *)
let correct_mapping_part2 (opponent_choice, my_choice) =
  let my_new_choice =
    match opponent_choice, my_choice with
    | x, 1 -> x - 1
    | x, 2 -> x
    | x, 3 -> x + 1
    | _ -> raise (Invalid_argument "something rotten in correct_mapping_part2")
  in
  opponent_choice, ((my_new_choice + 2) mod 3) + 1
;;

(** Score based on win/lose/tie. *)
let score_outcome (opponent_choice, my_choice) =
  (my_choice - opponent_choice + 4) mod 3 * 3
;;

(** Score based on my choice. The coincidence with the encoding is coincidence. *)
let score_choice my_choice = my_choice

(* The mapping_correction is used in part two, by default does nothing. *)
let play ?(mapping_correction = fun x -> x) lines =
  let games =
    List.map (Str.split (Str.regexp " ")) lines
    |> List.map (function
         | [ x; y ] -> map_opponent x, map_me_part1 y
         | _ -> raise (Invalid_argument "Row too long"))
    |> List.map mapping_correction
  in
  let total_outcome_score = List.map score_outcome games |> List.fold_left ( + ) 0 in
  let total_choice_score =
    List.map (fun x -> score_choice snd x) games |> List.fold_left ( + ) 0
  in
  let result = total_outcome_score + total_choice_score in
  print_endline @@ Int.to_string result
;;

let main () =
  let lines = Utils.load_input_lines "day02" in
  (* Part 1 *)
  play example_lines;
  play lines;
  (* Part 2 *)
  play ~mapping_correction:correct_mapping_part2 example_lines;
  play ~mapping_correction:correct_mapping_part2 lines
;;

let () = main ()
