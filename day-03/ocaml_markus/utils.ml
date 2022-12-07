exception Unreacheable

let inputs_folder = "./inputs"

let rec read_lines ?(acc : string list = []) (ic : in_channel) =
  try
    let line = input_line ic in
    read_lines ~acc:(acc @ [ line ]) ic
  with
  | End_of_file -> acc
;;

let load_input_lines file_name =
  let path = inputs_folder ^ "/" ^ file_name in
  let ic = open_in path in
  let lines = read_lines ic in
  close_in ic;
  lines
;;

let rec split_list
  ?(sublists : 'a list list = [])
  ?(current_sublist : 'a list = [])
  (splitter : 'a)
  (l : 'a list)
  =
  match l with
  | [] -> sublists @ [ current_sublist ]
  | head :: rest ->
    let split_here = head = splitter in
    let new_sublists = if split_here then sublists @ [ current_sublist ] else sublists in
    let new_current_sublist = if split_here then [] else current_sublist @ [ head ] in
    split_list ~sublists:new_sublists ~current_sublist:new_current_sublist splitter rest
;;

let rec sublists_of_size_n ?(acc : 'a list list = []) (n : int) (s : 'a Seq.t) =
  if Seq.is_empty s
  then acc
  else (
    let hd = Seq.take n s |> List.of_seq in
    let new_acc = hd :: acc in
    let tl = Seq.drop n s in
    sublists_of_size_n ~acc:new_acc n tl)
;;

let rec find_top_n ?(acc : 'a list = []) (n : int) (l : 'a list) =
  (* Assume acc is sorted at all times, with smallest value first. *)
  let () = assert (n > 0) in
  match l with
  | [] -> acc
  | head :: rest ->
    if List.length acc < n
    then find_top_n ~acc:(List.sort compare (head :: acc)) n rest
    else (
      match acc with
      | smallest :: largers ->
        if smallest < head
        then find_top_n ~acc:(List.sort compare (head :: largers)) n rest
        else find_top_n ~acc n rest
      | _ -> raise Unreacheable)
;;
