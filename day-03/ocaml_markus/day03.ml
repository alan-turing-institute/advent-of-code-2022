open Aoc22_ocaml

(* Encoding:
   1: Rock
   2: Paper
   3: Scissors
*)

let example_lines =
  [ "vJrwpWtwJgWrhcsFMMfFFhFp"
  ; "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"
  ; "PmmdzqPrVvPwwTWBwg"
  ; "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"
  ; "ttgJtRGJQctTZtZT"
  ; "CrZsJsPPZsGzwwsLwLmpwMDw"
  ]
;;

let split_compartments line =
  let l = String.length line in
  let () = assert (l mod 2 = 0) in
  let half_l = l / 2 in
  [ Str.first_chars line half_l; Str.last_chars line half_l ]
;;

module CharSet = Set.Make (Char)

let find_shared sl =
  let csl = List.map (fun x -> CharSet.of_seq (String.to_seq x)) sl in
  List.fold_left CharSet.inter (List.hd csl) (List.tl csl)
;;

let score_priority_char c =
  let code = Char.code c in
  (* Use the ASCII ranges for lower and uppercase. *)
  if 96 < code && code < 123 then code - 96 else code - 38
;;

let score_priority_set charset =
  (* This actually supports multiple failures of the rule in the same rucksack, but
     there's no harm in that. *)
  CharSet.to_seq charset |> Seq.map score_priority_char |> Seq.fold_left ( + ) 0
;;

let solve_part1 lines =
  let result =
    List.map split_compartments lines
    |> List.map find_shared
    |> List.map score_priority_set
    |> List.fold_left ( + ) 0
  in
  print_endline @@ Int.to_string result
;;

let solve_part2 lines =
  let result =
    List.to_seq lines
    |> Utils.sublists_of_size_n 3
    |> List.map find_shared
    |> List.map score_priority_set
    |> List.fold_left ( + ) 0
  in
  print_endline @@ Int.to_string result
;;

let main () =
  let lines = Utils.load_input_lines "day03" in
  (* Part 1 *)
  solve_part1 example_lines;
  solve_part1 lines;
  (* Part 2 *)
  solve_part2 example_lines;
  solve_part2 lines
;;

let () = main ()
