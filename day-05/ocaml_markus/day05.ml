open Aoc22_ocaml

let example_lines =
  [ "    [D]    "
  ; "[N] [C]    "
  ; "[Z] [M] [P]"
  ; " 1   2   3 "
  ; ""
  ; "move 1 from 2 to 1"
  ; "move 3 from 1 to 3"
  ; "move 2 from 2 to 1"
  ; "move 1 from 1 to 2"
  ]
;;

let parse_setup_line qs line =
  let chunks = Utils.substrings_of_size_n 4 line in
  let push_chunk q chunk =
    match chunk with
    | "    " | "   " | " " -> q
    | s -> q @ [ String.get s 1 ]
  in
  List.map2 push_chunk qs chunks
;;

let parse_setup setup =
  let num_stacks = List.hd setup |> String.length |> fun l -> (l / 4) + 1 in
  let qs = List.init num_stacks (fun _ -> []) in
  let num_lines = List.length setup in
  List.to_seq setup |> Seq.take (num_lines - 1) |> Seq.fold_left parse_setup_line qs
;;

let transfer_one (source, destination) = List.tl source, List.hd source :: destination

let transfer_part1 how_many source destination =
  List.init how_many (fun _ -> ())
  |> List.fold_left (fun x _ -> transfer_one x) (source, destination)
;;

let transfer_part2 how_many source destination =
  let source_seq = List.to_seq source in
  let hd = Seq.take how_many source_seq |> List.of_seq in
  let new_source = Seq.drop how_many source_seq |> List.of_seq in
  let new_destination = hd @ destination in
  new_source, new_destination
;;

let move_regexp = Str.regexp {|move \([0-9]+\) from \([0-9]+\) to \([0-9]+\)|}

let apply_move ~transfer (qs : char list list) move =
  let () = assert (Str.string_match move_regexp move 0) in
  let how_many = Str.matched_group 1 move |> int_of_string in
  let source_num = Str.matched_group 2 move |> int_of_string in
  let destination_num = Str.matched_group 3 move |> int_of_string in
  let source_index = source_num - 1 in
  let destination_index = destination_num - 1 in
  let source = List.nth qs source_index in
  let destination = List.nth qs destination_index in
  let new_source, new_destination = transfer how_many source destination in
  qs
  |> Utils.list_replace source_index new_source
  |> Utils.list_replace destination_index new_destination
;;

let solve ~transfer lines =
  let setup, moves =
    match Utils.split_list "" lines with
    | [ header; body ] -> header, body
    | _ -> raise (Invalid_argument "")
  in
  let qs = parse_setup setup in
  let qs = List.fold_left (apply_move ~transfer) qs moves in
  let result = List.map List.hd qs |> List.to_seq |> String.of_seq in
  print_endline result
;;

let main () =
  let lines = Utils.load_input_lines "day05" in
  (* Part 1 *)
  solve ~transfer:transfer_part1 example_lines;
  solve ~transfer:transfer_part1 lines;
  (* Part 2 *)
  solve ~transfer:transfer_part2 example_lines;
  solve ~transfer:transfer_part2 lines
;;

let () = main ()
