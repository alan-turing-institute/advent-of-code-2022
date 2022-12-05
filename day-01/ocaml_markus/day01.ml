open Aoc22_ocaml

let main () =
  let lines = Utils.load_input_lines "day01" in
  let calorie_counts =
    Utils.split_list "" lines
    |> List.map (List.map int_of_string)
    |> List.map (List.fold_left ( + ) 0)
  in
  let result_part1 = List.fold_left max 0 calorie_counts in
  let result_part2 = Utils.find_top_n 3 calorie_counts |> List.fold_left ( + ) 0 in
  print_endline @@ Int.to_string result_part1;
  print_endline @@ Int.to_string result_part2
;;

let () = main ()
