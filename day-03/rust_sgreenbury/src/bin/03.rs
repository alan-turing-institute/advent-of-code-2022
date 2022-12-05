use hashbrown::HashSet;
use itertools::Itertools;

fn char_to_int(c: char) -> u32 {
    if c.is_uppercase() {
        26 + c as u32 - 'A' as u32 + 1
    } else {
        c as u32 - 'a' as u32 + 1
    }
}

fn str_to_hashset(s: &str) -> HashSet<char> {
    s.chars().fold(HashSet::<char>::new(), |mut acc, c| {
        acc.insert(c);
        acc
    })
}

pub fn part_one(input: &str) -> Option<u32> {
    Some(
        input
            .lines()
            .map(|rucksack| {
                let (left_compartment, right_compartment) = rucksack.split_at(rucksack.len() / 2);
                str_to_hashset(left_compartment)
                    .intersection(&str_to_hashset(right_compartment))
                    .copied()
                    .map(char_to_int)
                    .next()
                    .unwrap()
            })
            .sum::<u32>(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(
        input
            .lines()
            .chunks(3)
            .into_iter()
            .map(|group| {
                group
                    .map(str_to_hashset)
                    .collect_tuple()
                    .map(|(elf1, elf2, elf3)| {
                        let elf1_elf2: HashSet<char> = elf1.intersection(&elf2).copied().collect();
                        *elf1_elf2.intersection(&elf3).next().unwrap()
                    })
                    .map(char_to_int)
                    .unwrap()
            })
            .sum::<u32>(),
    )
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
