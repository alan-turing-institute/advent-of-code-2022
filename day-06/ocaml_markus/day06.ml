open Aoc22_ocaml

let example_inputs =
  [ "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
  ; "bvwbjplbgvbhsrlpgdmjqwftvncz"
  ; "nppdvjthqldpwncqszvftbrmjlhg"
  ; "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
  ; "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
  ]
;;

module CharSet = Set.Make (Char)

let solve n input =
  let index =
    Utils.rolling_substring n input
    |> Seq.zip (Seq.ints 0)
    |> Seq.find_map (fun (i, ss) ->
         let ss_set = String.to_seq ss |> CharSet.of_seq in
         if CharSet.cardinal ss_set = n then Some i else None)
  in
  match index with
  | None -> raise (Invalid_argument input)
  | Some i -> print_endline @@ Int.to_string i
;;

let main () =
  let input = Utils.load_input_lines "day06" |> List.hd in
  (* Part 1 *)
  List.iter (solve 4) example_inputs;
  solve 4 input;
  (* Part 2 *)
  List.iter (solve 14) example_inputs;
  solve 14 input
;;

let () = main ()
