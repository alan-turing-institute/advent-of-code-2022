use hashbrown::HashMap;
use itertools::Itertools;
use std::{collections::VecDeque, fmt::Display};

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Instruction {
    Addx(i32),
    Noop,
}

impl Display for Instruction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Instruction::Addx(x) => {
                write!(f, "Addx {}", x)
            }
            Instruction::Noop => {
                write!(f, "Noop")
            }
        }
    }
}

fn read_instructions(input: &str) -> VecDeque<Instruction> {
    input
        .lines()
        .map(|line| {
            if line.starts_with('n') {
                Instruction::Noop
            } else {
                Instruction::Addx(line.split_once(' ').unwrap().1.parse::<i32>().unwrap())
            }
        })
        .collect()
}

const WIDTH: usize = 40;
const HEIGHT: usize = 6;

fn display_to_string(crt_display: &[[char; WIDTH]; HEIGHT]) -> String {
    crt_display
        .iter()
        .map(String::from_iter)
        .collect_vec()
        .iter()
        .join("\n")
}

pub fn part_one(input: &str) -> Option<i32> {
    let mut instructions: VecDeque<Instruction> = read_instructions(input);
    let mut queue: HashMap<usize, i32> = HashMap::new();
    let mut counter = 1i32;
    let mut cycle_points = vec![];
    let mut cycle_idx = 0;
    while !instructions.is_empty() || !queue.is_empty() {
        // Add to cycle points
        if (cycle_idx + 20) / 40 != cycle_points.len() {
            cycle_points.push(counter * (cycle_points.len() * 40 + 20) as i32);
        }

        // Remove from queue
        counter += if let Some((_, x)) = queue.remove_entry(&cycle_idx) {
            x
        } else {
            0
        };

        if let Some(instruction) = instructions.pop_front() {
            // Add to queue
            match instruction {
                Instruction::Noop => {
                    cycle_idx += 1;
                }
                Instruction::Addx(x) => {
                    queue.insert(cycle_idx + 2, x);
                    cycle_idx += 2;
                }
            }
        }
    }
    Some(cycle_points.into_iter().sum())
}

fn add_instruction_to_queue(
    mut queue: HashMap<usize, i32>,
    cycle_idx: usize,
    instruction: Instruction,
) -> HashMap<usize, i32> {
    // Add to queue
    match instruction {
        Instruction::Noop => {
            queue.insert(cycle_idx + 1, 0);
        }
        Instruction::Addx(x) => {
            queue.insert(cycle_idx + 2, x);
        }
    }
    queue
}

pub fn part_two(input: &str) -> Option<String> {
    let mut crt_display = [[' '; WIDTH]; HEIGHT];
    let mut instructions: VecDeque<Instruction> = read_instructions(input);
    let mut queue: HashMap<usize, i32> = HashMap::new();
    let mut counter = 1i32;
    let mut cycle_idx = 0;
    if let Some(instruction) = instructions.pop_front() {
        queue = add_instruction_to_queue(queue, cycle_idx, instruction);
    }
    while !instructions.is_empty() || !queue.is_empty() {
        // Remove from queue and add next instruction
        counter += if let Some((_, v)) = queue.remove_entry(&cycle_idx) {
            if let Some(instruction) = instructions.pop_front() {
                queue = add_instruction_to_queue(queue, cycle_idx, instruction)
            }
            v
        } else {
            0
        };
        // Handle write to crt
        let crt_col = cycle_idx % WIDTH;
        let crt_row = cycle_idx / WIDTH;
        if (cycle_idx % WIDTH) as i32 >= counter - 1 && (cycle_idx % WIDTH) as i32 <= counter + 1 {
            crt_display[crt_row][crt_col] = '#';
        } else {
            crt_display[crt_row][crt_col] = '.';
        }

        cycle_idx += 1;
        if cycle_idx == WIDTH * HEIGHT {
            break;
        }
    }

    Some(display_to_string(&crt_display))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 10);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    const PART_2_STR: &str = "\
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....";

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(part_one(&input), Some(13140));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(
            part_two(&input),
            Some(PART_2_STR.to_string().replace(' ', ""))
        );
    }
}
