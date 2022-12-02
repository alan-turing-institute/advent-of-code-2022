use std::str::Split;

pub fn part_one(input: &str) -> Option<u32> {
    // Returns the total calories of the top elf.
    let calories_per_elf = count_calories_per_elf(input).unwrap();
    let max_calories = calories_per_elf.iter().max().unwrap();
    return Some(*max_calories);
}

pub fn part_two(input: &str) -> Option<u32> {
    // Returns the total calories of the top three elves.
    let mut calories_per_elf = count_calories_per_elf(input).unwrap();
    calories_per_elf.sort();
    calories_per_elf.reverse();
    let calories_top_three_elves = calories_per_elf[0] + calories_per_elf[1] + calories_per_elf[2];
    return Some(calories_top_three_elves);
}

fn count_calories_per_elf(input: &str) -> Option<Vec<u32>> {
    // Returns a vector with the total calorie count for each elf.
    let mut calories_per_elf = Vec::new();
    let elves: Split<&str> = input.split("\n\n");
    for elf in elves {
        let food_items = elf.lines();
        let mut calorie_count = 0;
        for item in food_items {
            let calories = item.parse::<u32>().unwrap();
            calorie_count = calorie_count + calories;
        }
        calories_per_elf.push(calorie_count);
    }
    return Some(calories_per_elf);
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
        assert_eq!(part_one(&input), Some(2327));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_two(&input), Some(3215));
    }
}
