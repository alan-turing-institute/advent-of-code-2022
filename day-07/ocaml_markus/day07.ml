open Aoc22_ocaml

let example_lines =
  [ "$ cd /"
  ; "$ ls"
  ; "dir a"
  ; "14848514 b.txt"
  ; "8504156 c.dat"
  ; "dir d"
  ; "$ cd a"
  ; "$ ls"
  ; "dir e"
  ; "29116 f"
  ; "2557 g"
  ; "62596 h.lst"
  ; "$ cd e"
  ; "$ ls"
  ; "584 i"
  ; "$ cd .."
  ; "$ cd .."
  ; "$ cd d"
  ; "$ ls"
  ; "4060174 j"
  ; "8033020 d.log"
  ; "5626152 d.ext"
  ; "7214296 k"
  ]
;;

type line =
  | Cd of string
  | Ls
  | Dir of string
  | File of int * string

let regexps =
  [ (Str.regexp {|\$ cd \([A-Za-z/.]+\)|}, fun s -> Cd (Str.matched_group 1 s))
  ; (Str.regexp {|\$ ls|}, fun _ -> Ls)
  ; (Str.regexp {|dir \([A-Za-z/]+\)|}, fun s -> Dir (Str.matched_group 1 s))
  ; ( Str.regexp {|\([0-9]+\) \([A-Za-z/.]+\)|}
    , fun s -> File (Str.matched_group 1 s |> int_of_string, Str.matched_group 2 s) )
  ]
;;

let parse_line line =
  let result =
    List.find_map
      (fun (regexp, f_parse) ->
        if Str.string_match regexp line 0 then Some (f_parse line) else None)
      regexps
  in
  match result with
  | Some x -> x
  | None -> raise (Invalid_argument line)
;;

let get_path cwd new_name =
  let parent_path =
    match List.hd cwd with
    | Dir path -> path
    | _ -> raise (Invalid_argument "")
  in
  parent_path ^ "/" ^ new_name
;;

let set_cwd cwd new_cd =
  match new_cd with
  | Cd "/" -> [ Dir "/" ]
  | Cd ".." -> List.tl cwd
  | Cd "." -> cwd
  | Cd name -> Dir (get_path cwd name) :: cwd
  | _ -> raise (Invalid_argument "")
;;

let collect_nodes cmds =
  let folder (cwd, parent_pairs) cmd =
    match cmd with
    | Ls -> cwd, parent_pairs
    | Cd name -> set_cwd cwd (Cd name), parent_pairs
    | Dir name -> cwd, (List.hd cwd, Dir (get_path cwd name)) :: parent_pairs
    | File (size, name) ->
      cwd, (List.hd cwd, File (size, get_path cwd name)) :: parent_pairs
  in
  List.fold_left folder ([ Dir "/" ], []) cmds
;;

module StringMap = Map.Make (String)

let collect_children nodes =
  let folder child_map (parent, child) =
    match parent with
    | Dir name ->
      StringMap.update
        name
        (function
         | Some x -> Some (child :: x)
         | None -> Some [ child ])
        child_map
    | _ -> raise (Invalid_argument "")
  in
  List.fold_left folder StringMap.empty nodes
;;

let rec get_size child_map dir_map file =
  match file with
  | File (size, _) -> size, dir_map
  | Dir name ->
    (match StringMap.find_opt name dir_map with
     | Some size -> size, dir_map
     | None ->
       let new_size, new_dir_map =
         let folder (current_size, dm) x =
           let this_node_size, new_dm = get_size child_map dm x in
           current_size + this_node_size, new_dm
         in
         StringMap.find name child_map |> List.fold_left folder (0, dir_map)
       in
       new_size, StringMap.add name new_size new_dir_map)
  | _ -> raise (Invalid_argument "")
;;

let folder_sizes lines =
  List.map parse_line lines
  |> collect_nodes
  |> snd
  |> (fun nodes ->
       let files = List.map fst nodes in
       let child_map = collect_children nodes in
       let folder (acc, dm) file =
         let this_node_size, new_dm = get_size child_map dm file in
         acc + this_node_size, new_dm
       in
       List.fold_left folder (0, StringMap.empty) files)
  |> snd
;;

let solve_part1 lines =
  let result =
    folder_sizes lines
    |> StringMap.bindings
    |> List.map snd
    |> List.filter (fun x -> x <= 100000)
    |> List.fold_left ( + ) 0
  in
  print_endline @@ Int.to_string result
;;

let solve_part2 lines =
  let fs = folder_sizes lines in
  let total_size = 70000000 in
  let space_needed = 30000000 in
  let space_used = StringMap.find "/" fs in
  let space_free = total_size - space_used in
  let release_needed = space_needed - space_free in
  let result =
    StringMap.fold
      (fun _ this_size leading_candidate ->
        let room_to_spare = this_size - release_needed in
        if room_to_spare >= 0 && this_size < leading_candidate
        then this_size
        else leading_candidate)
      fs
      Int.max_int
  in
  print_endline @@ Int.to_string result
;;

let main () =
  let lines = Utils.load_input_lines "day07" in
  (* Part 1 *)
  solve_part1 example_lines;
  solve_part1 lines;
  (* Part 2 *)
  solve_part2 example_lines;
  solve_part2 lines
;;

let () = main ()
