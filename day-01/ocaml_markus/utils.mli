val load_input_lines : string -> string list

val split_list
  :  ?sublists:'a list list
  -> ?current_sublist:'a list
  -> 'a
  -> 'a list
  -> 'a list list

val find_top_n : ?acc:'a list -> int -> 'a list -> 'a list
