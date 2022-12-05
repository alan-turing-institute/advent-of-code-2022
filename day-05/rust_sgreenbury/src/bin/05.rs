use regex::Regex;

// Type for the state of system as a vec of stacks (vecs)
#[derive(Debug)]
struct State {
    stacks: Vec<Vec<char>>,
}

impl From<&str> for State {
    fn from(input: &str) -> Self {
        let n_stacks = (input.lines().next().unwrap().len() + 1) / 4;
        let mut stacks = vec![Vec::<char>::new(); n_stacks];
        for line in input.lines() {
            if line.chars().nth(1).unwrap().is_numeric() {
                break;
            }
            for (idx, stack) in stacks.iter_mut().enumerate() {
                if let Some(c) = line.chars().nth(idx * 4 + 1) {
                    if !c.is_whitespace() {
                        stack.insert(0, c);
                    }
                }
            }
        }
        Self { stacks }
    }
}

impl State {
    fn pop_crates(&mut self, inst: &Instruction) -> Vec<char> {
        let n = self.stacks[inst.source].len();
        self.stacks[inst.source].split_off(n - inst.number)
    }
    fn push_crates(&mut self, inst: &Instruction, crates: Vec<char>, reversed: bool) {
        if reversed {
            self.stacks[inst.target].extend(crates.iter().rev());
        } else {
            self.stacks[inst.target].extend(crates.iter());
        };
    }
    fn get_string(&self) -> String {
        self.stacks.iter().fold(String::new(), |mut s, stack| {
            if let Some(c) = stack.last() {
                s.push(*c);
            }
            s
        })
    }
}

// Type for an instruction moving the crates
#[derive(Debug)]
struct Instruction {
    number: usize,
    source: usize,
    target: usize,
}

impl From<(&str, &str, &str)> for Instruction {
    fn from(caps: (&str, &str, &str)) -> Self {
        Instruction {
            number: caps.0.parse().unwrap(),
            source: caps.1.parse::<usize>().unwrap() - 1,
            target: caps.2.parse::<usize>().unwrap() - 1,
        }
    }
}

fn read_instructions(text: &str) -> Vec<Instruction> {
    let re: Regex = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    let mut insts: Vec<Instruction> = Vec::new();
    for cap in re.captures_iter(text) {
        insts.push(Instruction::from((&cap[1], &cap[2], &cap[3])));
    }
    insts
}

fn run(input: &str, reversed: bool) -> Option<String> {
    // Get instructions
    let insts = read_instructions(input);

    // Fold instructions over initial state
    let state = insts.iter().fold(State::from(input), |mut state, inst| {
        let crates_to_move = state.pop_crates(inst);
        state.push_crates(inst, crates_to_move, reversed);
        state
    });

    // Get string representation of state
    Some(state.get_string())
}

pub fn part_one(input: &str) -> Option<String> {
    run(input, true)
}

pub fn part_two(input: &str) -> Option<String> {
    run(input, false)
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
