open Aoc22_ocaml

let example_lines = [ "2-4,6-8"; "2-3,4-5"; "5-7,7-9"; "2-8,3-7"; "6-6,4-6"; "2-6,4-8" ]

type assignment =
  { low : int
  ; high : int
  }

let parse_assignment s =
  match Str.split (Str.regexp "-") s |> List.map int_of_string with
  | [ low; high ] -> { low; high }
  | _ -> raise (Invalid_argument s)
;;

let parse_assignment_pair line =
  Str.split (Str.regexp ",") line
  |> List.map parse_assignment
  |> function
  | [ a1; a2 ] -> a1, a2
  | _ -> raise (Invalid_argument line)
;;

let contains a1 a2 = a1.low <= a2.low && a2.high <= a1.high
let is_redundant (a1, a2) = contains a1 a2 || contains a2 a1
let precedes a1 a2 = a1.high < a2.low
let has_overlap (a1, a2) = not (precedes a1 a2 || precedes a2 a1)

let solve_part1 lines =
  let result =
    List.map parse_assignment_pair lines
    |> List.map is_redundant
    |> List.map Bool.to_int
    |> List.fold_left ( + ) 0
  in
  print_endline @@ Int.to_string result
;;

let solve_part2 lines =
  let result =
    List.map parse_assignment_pair lines
    |> List.map has_overlap
    |> List.map Bool.to_int
    |> List.fold_left ( + ) 0
  in
  print_endline @@ Int.to_string result
;;

let main () =
  let lines = Utils.load_input_lines "day04" in
  (* Part 1 *)
  solve_part1 example_lines;
  solve_part1 lines;
  (* Part 2 *)
  solve_part2 example_lines;
  solve_part2 lines
;;

let () = main ()
