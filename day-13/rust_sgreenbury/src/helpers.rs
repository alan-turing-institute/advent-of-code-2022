/*
 * Use this file if you want to extract helpers from your solutions.
 * Example import from this file: `use advent_of_code::helpers::example_fn;`.
 */

use std::io;
pub fn wait() {
    let mut buffer = String::new();
    io::stdin()
        .read_line(&mut buffer)
        .map_err(|err| println!("{:?}", err))
        .ok();
}
