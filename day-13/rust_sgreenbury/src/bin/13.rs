use itertools::Itertools;
use std::cmp::Ordering;

#[derive(Debug, Clone, Copy)]
enum Token {
    Open,
    Close,
    Value(u32),
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum Packet {
    Int(u32),
    List(Vec<Packet>),
}

// Patterns to match: '[', ']', '0-9', '10', ','
fn string_to_tokens(line: &str) -> Vec<Token> {
    let mut it = line.chars().peekable();
    let mut tokens = Vec::<Token>::new();
    while let Some(c) = it.next() {
        match c {
            c if c == '[' => {
                tokens.push(Token::Open);
            }
            c if c == ']' => {
                tokens.push(Token::Close);
            }
            c if c == ',' => {
                continue;
            }
            c if c.is_numeric() => {
                if let Some(next_c) = it.peek() {
                    if next_c.is_numeric() {
                        it.next();
                        tokens.push(Token::Value(10));
                    } else {
                        tokens.push(Token::Value(c.to_digit(10).unwrap()))
                    }
                } else {
                    tokens.push(Token::Value(c.to_digit(10).unwrap()))
                }
            }
            _ => panic!("Can't process '{c}' char!"),
        }
    }
    tokens
}

fn tokens_to_packet_recursive(mut idx: usize, tokens: &[Token], packet: Packet) -> (usize, Packet) {
    match packet {
        Packet::List(mut packet_vec) => {
            while idx < tokens.len() {
                match tokens[idx] {
                    Token::Value(x) => {
                        packet_vec.push(Packet::Int(x));
                        idx += 1;
                    }
                    Token::Open => {
                        let (next_idx, nested_packet) =
                            tokens_to_packet_recursive(idx + 1, tokens, Packet::List(Vec::new()));
                        packet_vec.push(nested_packet);
                        idx = next_idx;
                    }
                    Token::Close => return (idx + 1, Packet::List(packet_vec)),
                }
            }
        }
        _ => panic!("Packet is not a vec!"),
    }
    panic!("Incorrectly terminated packet!")
}

fn string_to_packet(s: &str) -> Packet {
    tokens_to_packet_recursive(1, &string_to_tokens(s), Packet::List(Vec::new())).1
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        match (self, other) {
            (Packet::Int(left), Packet::Int(right)) => left.cmp(right),
            (Packet::Int(left), Packet::List(_)) => {
                let new_left = Packet::List(vec![Packet::Int(*left)]);
                new_left.cmp(other)
            }
            (Packet::List(_), Packet::Int(right)) => {
                let new_right = Packet::List(vec![Packet::Int(*right)]);
                self.cmp(&new_right)
            }
            (Packet::List(left), Packet::List(right)) => {
                let min_length = left.len().min(right.len());
                for idx in 0..min_length {
                    match left[idx].cmp(&right[idx]) {
                        Ordering::Less => return Ordering::Less,
                        Ordering::Equal => (),
                        Ordering::Greater => return Ordering::Greater,
                    }
                }
                left.len().cmp(&right.len())
            }
        }
    }
}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

pub fn part_one(input: &str) -> Option<usize> {
    let correct_idx = input
        .split("\n\n")
        .enumerate()
        .map(|(idx, lines)| {
            let mut it = lines.lines();
            let p1 = string_to_packet(it.next().unwrap());
            let p2 = string_to_packet(it.next().unwrap());
            (idx + 1) * ((p1 < p2) as usize)
        })
        .collect_vec();
    Some(correct_idx.iter().sum::<usize>())
}

pub fn part_two(input: &str) -> Option<usize> {
    let mut packets = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(string_to_packet)
        .collect_vec();
    let signal1 = Packet::List(vec![Packet::Int(2)]);
    let signal2 = Packet::List(vec![Packet::Int(6)]);
    packets.push(signal1.clone());
    packets.push(signal2.clone());
    packets.sort();
    Some(
        packets
            .iter()
            .enumerate()
            .fold(1, |mut acc, (idx, packet)| {
                match packet {
                    _ if packet == &signal1 || packet == &signal2 => {
                        acc *= idx + 1;
                    }
                    _ => (),
                };
                acc
            }),
    )
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 13);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_string_to_packet() {
        let input = "[1,[2,[3,[4,[5,6,7]]]],8,9]";
        println!("{:?}", string_to_packet(input));
    }

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 13);
        assert_eq!(part_one(&input), Some(13));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 13);
        assert_eq!(part_two(&input), Some(140));
    }
}
