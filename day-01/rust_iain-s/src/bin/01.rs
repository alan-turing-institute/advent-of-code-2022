pub fn part_one(input: &str) -> Option<u32> {
    let mut max_calories: u32= u32::MIN;
    let mut calories = u32::MIN;
    for line in input.split("\n") {
        if line.len() == usize::MIN {
             // next elf
            if calories > max_calories {
                max_calories = calories;
            }
            calories = u32::MIN;
        } else {
            calories += line.parse::<u32>().unwrap();
        }
    }
    return Some(max_calories);
}

pub fn get_top_three(input: &str) -> Option<Vec<u32>> {
    let mut my_vec = Vec::new();
    let mut calories = u32::MIN;
    for line in input.split("\n") {
        if line.len() == usize::MIN {
            // next elf
            my_vec.push(calories);
            calories = u32::MIN;
        } else {
            calories += line.parse::<u32>().unwrap();
        }
    }

    my_vec.sort_unstable();
    return Some(my_vec[my_vec.len()-3..].to_vec());
}

pub fn part_two(input: &str) -> Option<u32> {
    let top_three = get_top_three(input).unwrap();
    return Some(top_three.iter().sum());
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
    fn test_part_one_one() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_one(&input).unwrap(), u32::MIN);
    }

    #[test]
    fn test_part_one_two() {
        let input = "1\n\n2\n\n3\n";
        assert_eq!(part_one(&input).unwrap(), 3u32);
    }

    #[test]
    fn test_part_two() {
        let input = "1\n\n2\n\n3\n";
        assert_eq!(part_two(&input).unwrap(), 6u32);
    }

    #[test]
    fn test_get_vec_one() {
        let input = "1\n\n2\n\n3\n";
        assert_eq!(get_top_three(&input).unwrap(), vec![1, 2, 3]);
    }

    #[test]
    fn test_get_vec_two() {
        let input = "1\n1\n\n1\n\n5\n\n3\n";
        assert_eq!(get_top_three(&input).unwrap(), vec![2, 3, 5]);
    }
}
