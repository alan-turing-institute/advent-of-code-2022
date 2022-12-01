use itertools::Itertools;

fn calories_per_elf(input: &str) -> Vec<u32> {
    input
        .split("\n\n")
        .map(|block| {
            block
                .lines()
                .map(|line| line.parse::<u32>().unwrap())
                .sum::<u32>()
        })
        .collect_vec()
}

pub fn part_one(input: &str) -> Option<u32> {
    calories_per_elf(input).into_iter().max()
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(
        calories_per_elf(input)
            .into_iter()
            .sorted()
            .rev()
            .take(3)
            .sum::<u32>(),
    )
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 1);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_one(&input), Some(24000));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_two(&input), Some(45000));
    }
}
