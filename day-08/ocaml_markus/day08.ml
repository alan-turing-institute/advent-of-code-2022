open Aoc22_ocaml

let load_input file_name =
  Utils.load_input_lines file_name
  |> List.to_seq
  |> Seq.map (fun x ->
       String.to_seq x |> Seq.map (fun x -> x |> Utils.string_of_char |> int_of_string))
;;

(* Part 1 *)
let check_row_part1 row =
  row
  |> Seq.scan
       (fun (max_found, _) this ->
         if this > max_found then this, true else max_found, false)
       (min_int, false)
  |> Seq.drop 1
  |> Seq.map snd
;;

let check_rows ~check_row ~aggregator mat =
  let from_left = Seq.map check_row mat in
  let from_right =
    Seq.map (fun x -> x |> Utils.reverse_seq |> check_row |> Utils.reverse_seq) mat
  in
  Utils.nested_map2 aggregator from_left from_right
;;

let check_and_aggregate ~check_row ~aggregator mat =
  let rows_checker = check_rows ~check_row ~aggregator in
  let rows = rows_checker mat in
  let cols = mat |> Seq.transpose |> rows_checker |> Seq.transpose in
  Utils.nested_map2 aggregator rows cols
;;

let solve_part1 mat =
  let visibles = check_and_aggregate ~check_row:check_row_part1 ~aggregator:( || ) mat in
  let folder acc x = if x then acc + 1 else acc in
  let result = Seq.fold_left (fun acc s -> Seq.fold_left folder acc s) 0 visibles in
  print_endline @@ Int.to_string result
;;

(* Part 2 *)
let check_row_part2 row =
  let scanner (viewing_dists, _) this =
    let this_distance = List.nth viewing_dists this in
    let new_dists = List.mapi (fun i d -> if i <= this then 1 else d + 1) viewing_dists in
    new_dists, this_distance
  in
  let initial_viewing_dists = List.init 10 (fun _ -> 0) in
  row |> Seq.scan scanner (initial_viewing_dists, 0) |> Seq.drop 1 |> Seq.map snd
;;

let solve_part2 mat =
  let scores = check_and_aggregate ~check_row:check_row_part2 ~aggregator:( * ) mat in
  let result = Seq.fold_left (fun acc s -> Seq.fold_left max acc s) 0 scores in
  print_endline @@ Int.to_string result
;;

(* Main *)
let main () =
  (* Part 1 *)
  load_input "day08_example" |> solve_part1;
  load_input "day08" |> solve_part1;
  (* Part 2 *)
  load_input "day08_example" |> solve_part2;
  load_input "day08" |> solve_part2
;;

let () = main ()
