use std::char::from_digit;
use std::str::Split;
use std::{iter, vec};

use itertools::Itertools;

pub fn part_one(input: &str) -> Option<u32> {
    Some(input.lines().map(|l| has_duplicate(l) as u32).sum::<u32>())
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(input.lines().map(|l| has_overlap(l) as u32).sum::<u32>())
}

fn get_range(elf: &str) -> (u32, u32) {
    let range: Vec<u32> = elf.split('-').map(|c| c.parse::<u32>().unwrap()).collect();
    let (min, max) = (*range.first().unwrap(), *range.last().unwrap());
    return (min, max);
}

fn has_duplicate(line: &str) -> bool {
    let pair: Vec<(u32, u32)> = line.split(',').map(|c| get_range(c)).collect();
    let elf1 = pair[0];
    let elf2 = pair[1];

    match elf1.1 - elf1.0 < elf2.1 - elf2.0 {
        true => elf2.0 <= elf1.0 && elf2.1 >= elf1.1,
        false => elf1.0 <= elf2.0 && elf1.1 >= elf2.1,
    }
}

fn has_overlap(line: &str) -> bool {
    let pair: Vec<(u32, u32)> = line.split(',').map(|c| get_range(c)).collect();
    let mut elf1 = pair[0];
    let mut elf2 = pair[1];
    if pair[0].0 > pair[1].0 {
        elf1 = pair[1];
        elf2 = pair[0];
    }

    elf1.0 <= elf2.1 && elf2.0 <= elf1.1
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 4);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_one(&input), Some(2));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_two(&input), Some(4));
    }
}
