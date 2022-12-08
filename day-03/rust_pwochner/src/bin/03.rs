use std::collections::{HashMap, HashSet};

use itertools::Itertools;

pub fn part_one(input: &str) -> Option<u32> {
    let map_priorities = get_map();
    Some(
        input
            .lines()
            .map(|line| wrong_item(line))
            .map(|c| map_priorities.get(&c).unwrap())
            .sum::<u32>(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    let map_priorities = get_map();
    let lines = input.lines();
    let mut sum = 0;
    for (elf_1, elf_2, elf_3) in lines.tuples() {
        let badge = get_badge(elf_1, elf_2, elf_3);
        let priority = map_priorities.get(&badge).unwrap();
        sum += *priority;
    }
    return Some(sum);
}

fn get_map() -> HashMap<char, u32> {
    let alphabet = (b'a'..=b'z')
        .chain(b'A'..=b'Z')
        .filter_map(|c| {
            let c = c as char;
            if c.is_alphabetic() {
                Some(c)
            } else {
                None
            } // filter only alphabetic chars
        })
        .collect::<Vec<_>>();
    let map_priorities: HashMap<char, u32> = alphabet
        .into_iter()
        .enumerate()
        .map(|c| (c.1, c.0 as u32 + 1))
        .collect();
    return map_priorities;
}

fn wrong_item(rucksack: &str) -> char {
    let nr_items = rucksack.len();
    let compartment_1 = &rucksack[..nr_items / 2];
    let compartment_2 = &rucksack[nr_items / 2..];
    return get_duplicate(compartment_1, compartment_2);
}
fn get_duplicate(compartment_1: &str, compartment_2: &str) -> char {
    let set_1 = unique_chars(compartment_1);
    let set_2 = unique_chars(compartment_2);
    let vec_duplicates: Vec<&char> = set_1.intersection(&set_2).collect_vec();
    let duplicate = vec_duplicates.first().unwrap();
    return *duplicate.to_owned();
}

fn get_badge(elf_1: &str, elf_2: &str, elf_3: &str) -> char {
    let set_1 = unique_chars(elf_1);
    let set_2 = unique_chars(elf_2);
    let set_3 = unique_chars(elf_3);
    let candidates = set_1.intersection(&set_2).collect_vec();
    for c in candidates {
        if set_3.contains(c) {
            return *c;
        }
    }
    // let intersec_1: HashSet<&char> = HashSet::from_iter(intersection_vec.iter().cloned());
    // let badge = intersec_1.intersection(&set_3).collect_vec();

    return 'a';
}

fn unique_chars(line: &str) -> HashSet<char> {
    let set: HashSet<char> = line.chars().collect();
    return set;
}
fn main() {
    let input = &advent_of_code::read_file("inputs", 3);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_one(&input), Some(157));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_two(&input), Some(70));
    }
}
