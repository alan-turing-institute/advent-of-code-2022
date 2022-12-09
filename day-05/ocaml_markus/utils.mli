val load_input_lines : string -> string list

val split_list
  :  ?sublists:'a list list
  -> ?current_sublist:'a list
  -> 'a
  -> 'a list
  -> 'a list list

val find_top_n : ?acc:'a list -> int -> 'a list -> 'a list
val sublists_of_size_n : ?acc:'a list list -> int -> 'a Seq.t -> 'a list list
val substrings_of_size_n : int -> string -> string list
val list_replace : int -> 'a -> 'a list -> 'a list
