use std::{collections::VecDeque, fmt::Display};

struct Monkey {
    idx: usize,
    items: VecDeque<u64>,
    transform: Box<dyn Fn(u64) -> u64>,
    divisor: u64,
    true_monkey: usize,
    false_monkey: usize,
    total_inspected: usize,
}

fn add(a: u64) -> impl Fn(u64) -> u64 {
    move |x| x + a
}

fn mul(a: u64) -> impl Fn(u64) -> u64 {
    move |x| x * a
}

fn square() -> impl Fn(u64) -> u64 {
    |x| x * x
}

impl Display for Monkey {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(
            f,
            "idx: {}, items: {:?}, div: {}, true: {}, false: {}",
            self.idx, self.items, self.divisor, self.true_monkey, self.false_monkey
        )?;
        writeln!(
            f,
            "Monkey {}: {:?}; Inspected: {}",
            self.idx, self.items, self.total_inspected
        )?;
        Ok(())
    }
}

impl Monkey {
    fn read_from_string(input: &str) -> Self {
        let mut lines = input.lines();
        let idx = lines
            .next()
            .unwrap()
            .strip_suffix(':')
            .unwrap()
            .split(' ')
            .last()
            .unwrap()
            .parse::<usize>()
            .unwrap();
        let items = lines
            .next()
            .unwrap()
            .rsplit_once("items: ")
            .unwrap()
            .1
            .split(", ")
            .map(|x| x.parse::<u64>().unwrap())
            .collect::<VecDeque<_>>();
        let op = lines
            .next()
            .unwrap()
            .rsplit_once("old ")
            .unwrap()
            .1
            .split_once(' ')
            .unwrap();
        let transform: Box<dyn Fn(u64) -> u64> = if op.0 == "+" && op.1 != "old" {
            Box::new(add(op.1.parse::<u64>().unwrap()))
        } else if op.0 == "*" && op.1 != "old" {
            Box::new(mul(op.1.parse::<u64>().unwrap()))
        } else {
            Box::new(square())
        };
        let divisor = lines
            .next()
            .unwrap()
            .rsplit_once(' ')
            .unwrap()
            .1
            .parse::<u64>()
            .unwrap();
        let true_monkey = lines
            .next()
            .unwrap()
            .rsplit_once(' ')
            .unwrap()
            .1
            .parse::<usize>()
            .unwrap();
        let false_monkey = lines
            .next()
            .unwrap()
            .rsplit_once(' ')
            .unwrap()
            .1
            .parse::<usize>()
            .unwrap();
        let total_inspected = 0;
        Self {
            idx,
            items,
            transform,
            divisor,
            true_monkey,
            false_monkey,
            total_inspected,
        }
    }

    fn process_items_part1(&mut self) -> Vec<(usize, u64)> {
        let mut processed: Vec<(usize, u64)> = Vec::new();
        self.total_inspected += self.items.len();
        while let Some(item) = self.items.pop_front() {
            let new_worry = (self.transform)(item) / 3;
            if new_worry % self.divisor == 0 {
                processed.push((self.true_monkey, new_worry));
            } else {
                processed.push((self.false_monkey, new_worry))
            }
        }
        processed
    }
    fn process_items_part2(&mut self, common_divisor: u64) -> Vec<(usize, u64)> {
        let mut processed: Vec<(usize, u64)> = Vec::new();
        self.total_inspected += self.items.len();
        while let Some(item) = self.items.pop_front() {
            let new_worry = (self.transform)(item);
            if new_worry % self.divisor == 0 {
                processed.push((self.true_monkey, new_worry % common_divisor));
            } else {
                processed.push((self.false_monkey, new_worry % common_divisor));
            }
        }
        processed
    }
}

fn top_n_inspected(n: usize, monkeys: &mut [Monkey]) -> usize {
    monkeys.sort_by(|a, b| a.total_inspected.cmp(&b.total_inspected));
    monkeys
        .iter()
        .rev()
        .take(n)
        .map(|m| m.total_inspected)
        .product::<usize>()
}

pub fn part_one(input: &str) -> Option<usize> {
    let mut monkeys = input
        .split("\n\n")
        .map(Monkey::read_from_string)
        .collect::<Vec<Monkey>>();

    for _round in 0..20 {
        for monkey_idx in 0..monkeys.len() {
            let v: Vec<(usize, u64)> = monkeys[monkey_idx].process_items_part1();
            for item in v {
                monkeys[item.0].items.push_back(item.1);
            }
        }
    }
    Some(top_n_inspected(2, &mut monkeys))
}

pub fn part_two(input: &str) -> Option<usize> {
    let mut monkeys = input
        .split("\n\n")
        .map(Monkey::read_from_string)
        .collect::<Vec<Monkey>>();
    let common_divisor = monkeys.iter().map(|m| m.divisor).product::<u64>();
    for _round in 0..10000 {
        for monkey_idx in 0..monkeys.len() {
            let v: Vec<(usize, u64)> = monkeys[monkey_idx].process_items_part2(common_divisor);
            for item in v {
                monkeys[item.0].items.push_back(item.1);
            }
        }
    }
    Some(top_n_inspected(2, &mut monkeys))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 11);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_one(&input), Some(10605));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_two(&input), Some(2713310158));
    }
}
