use itertools::Itertools;

pub fn part_one(input: &str) -> Option<String> {
    let mut cargo_stack = build_cargo_stack(input);
    let split: Vec<&str> = input.split("\n\n").collect();
    let instructions_block = split.iter().nth(1).unwrap();
    for line in instructions_block.lines() {
        let (nr_crates, from_stack, to_stack) = parse_instruction(line);
        println!("Instructions: {:?}", (nr_crates, from_stack, to_stack));
        for _n in 1..nr_crates + 1 {
            let item = cargo_stack[from_stack].pop().unwrap();
            cargo_stack[to_stack].push(item);
        }
    }
    let top_crates: String = cargo_stack.iter().map(|c| c.last().unwrap()).collect();
    return Some(top_crates);
}

pub fn part_two(input: &str) -> Option<String> {
    let mut cargo_stack = build_cargo_stack(input);
    let split: Vec<&str> = input.split("\n\n").collect();
    let instructions_block = split.iter().nth(1).unwrap();
    for line in instructions_block.lines() {
        let (nr_crates, from_stack, to_stack) = parse_instruction(line);
        let len = cargo_stack[from_stack].len();
        let mut items: Vec<char> = cargo_stack[from_stack].split_off(len - nr_crates);
        cargo_stack[to_stack].append(&mut items);
    }
    let top_crates: String = cargo_stack.iter().map(|c| c.last().unwrap()).collect();
    return Some(top_crates);
}

fn build_cargo_stack(input: &str) -> Vec<Vec<char>> {
    let split: Vec<&str> = input.split("\n\n").collect();
    let cargo_block = split.iter().next().unwrap();
    let mut cargo_iter = cargo_block.lines().rev();
    let labels = cargo_iter.next().unwrap().to_string();
    // initialise the cargo stacks (first element is int)
    let number_of_stacks = get_number_stacks(labels);
    let mut cargo_stack: Vec<Vec<char>> = initialise_stack(number_of_stacks);
    // build cargo stack
    let lines = split.iter().next().unwrap().lines().rev();
    for l in lines {
        let vec_line = l.chars().collect::<Vec<char>>();
        let mut index = 1;
        for i in 0..number_of_stacks {
            if vec_line[index].is_uppercase() {
                cargo_stack[i as usize].push(vec_line[index]);
            }
            // increment index
            index += 4;
        }
    }

    return cargo_stack;
}

fn get_number_stacks(labels: String) -> u32 {
    labels
        .chars()
        .filter_map(|a| a.to_digit(10))
        .collect_vec()
        .last()
        .unwrap()
        .to_owned()
}

fn initialise_stack(number_of_stacks: u32) -> Vec<Vec<char>> {
    let mut cargo_stack: Vec<Vec<char>> = Vec::new();
    for _i in 0..number_of_stacks {
        cargo_stack.push(Vec::new());
    }
    return cargo_stack;
}

fn parse_instruction(line: &str) -> (usize, usize, usize) {
    let vec = line.split_ascii_whitespace().collect_vec();
    return (
        vec[1].parse::<usize>().unwrap(),
        vec[3].parse::<usize>().unwrap() - 1,
        vec[5].parse::<usize>().unwrap() - 1,
    );
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 5);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_one(&input), Some("CMZ".to_string()));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_two(&input), Some("MCD".to_string()));
    }
}
