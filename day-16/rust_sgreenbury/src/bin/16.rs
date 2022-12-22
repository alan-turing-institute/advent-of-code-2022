use hashbrown::{HashMap, HashSet};
use itertools::Itertools;
use pathfinding::prelude::dijkstra;
use std::collections::VecDeque;

fn read_input(input: &str) -> HashMap<String, Room> {
    let mut rooms = HashMap::<String, Room>::new();
    input.lines().for_each(|line| {
        let (left, right) = line.split_once(';').unwrap();
        let label = left
            .split_once("Valve ")
            .unwrap()
            .1
            .split_once(" has flow")
            .unwrap()
            .0;
        let rate = left.rsplit_once('=').unwrap().1.parse::<u32>().unwrap();
        let neighbours = if let Some(pair) = right.rsplit_once("to valves ") {
            pair.1
        } else {
            right.rsplit_once("to valve ").unwrap().1
        };
        let neighbours = neighbours
            .split(", ")
            .map(|neigh| (neigh.to_string(), 1))
            .collect::<HashMap<String, usize>>();

        let room = Room {
            label: label.to_string(),
            rate,
            neighbours,
        };
        rooms.insert(label.to_string(), room);
    });

    reduce_rooms(&rooms)
}

fn reduce_rooms(rooms_in: &HashMap<String, Room>) -> HashMap<String, Room> {
    let mut rooms = rooms_in.clone();
    let rooms_to_remove: Vec<String> = rooms
        .iter()
        .filter(|(label, room)| (room.rate == 0 && *label != "AA"))
        .map(|(l, _)| l.clone())
        .collect_vec();

    for label in &rooms_to_remove {
        let neighbours = rooms.get(label).unwrap().get_neighbours().clone();
        for (room_label, room) in &mut rooms {
            if let Some(cost) = room.get_neighbours().clone().get(label) {
                for (zero_neighbour_label, zero_neighbour_cost) in &neighbours {
                    if zero_neighbour_label != room_label {
                        room.get_mut_neighbours()
                            .entry(zero_neighbour_label.to_string())
                            .or_insert(cost + zero_neighbour_cost);
                    }
                }
            }
            room.get_mut_neighbours().remove(label);
        }
        rooms.remove(label);
    }
    rooms
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Room {
    label: String,
    rate: u32,
    neighbours: HashMap<String, usize>,
}

impl Room {
    fn get_neighbours(&self) -> &HashMap<String, usize> {
        &self.neighbours
    }
    fn get_mut_neighbours(&mut self) -> &mut HashMap<String, usize> {
        &mut self.neighbours
    }
    fn get_neighbours_for_path(&self) -> Vec<(String, usize)> {
        self.neighbours
            .iter()
            .map(|(label, cost)| (label.clone(), *cost))
            .collect_vec()
    }
}

fn get_distance_map(rooms: &HashMap<String, Room>) -> HashMap<(&str, &str), usize> {
    let mut dists_map = HashMap::<(&str, &str), usize>::new();
    for (source, _) in rooms.iter() {
        for (target, _) in rooms.iter() {
            let path = dijkstra(
                source,
                |label| rooms.get(label).unwrap().get_neighbours_for_path(),
                |label| *label == *target,
            );
            dists_map.insert((source, target), path.unwrap().1);
        }
    }
    dists_map
}

pub fn get_path(
    dists_map: &HashMap<(&str, &str), usize>,
    rooms: &HashMap<String, Room>,
) -> (Vec<String>, usize, u32) {
    // Set-up
    let visited: Vec<&str> = vec!["AA"];
    let remaining: HashSet<&str> = HashSet::from_iter(
        rooms
            .iter()
            .filter(|(k, _)| *k != "AA")
            .map(|(k, _)| k.as_str()),
    );
    let mut completed_paths: Vec<(Vec<&str>, usize, u32)> = Vec::new();

    let mut queue = VecDeque::new();
    queue.push_front((visited, remaining, 30, 0));

    // Begin BFS
    while let Some((visited, remaining, current_time, mut current_release)) = queue.pop_front() {
        let current = *visited.last().unwrap();
        let rate = rooms.get(current).unwrap().rate;
        current_release += rate * current_time as u32;

        if remaining.is_empty() {
            completed_paths.push((visited.clone(), current_time, current_release));
            continue;
        }
        for &next in remaining.iter() {
            let dist = dists_map.get(&(current, next)).unwrap();
            // If next time is after the time has run out, abort
            if current_time < dist + 1 {
                completed_paths.push((visited.clone(), current_time, current_release));
                continue;
            }
            let next_time = current_time - 1 - dist;

            let mut next_remaining = remaining.clone();
            next_remaining.remove(next);

            let mut next_visited = visited.clone();
            next_visited.push(next);
            queue.push_back((next_visited, next_remaining, next_time, current_release));
        }
    }
    completed_paths.sort_by(|a, b| b.2.cmp(&a.2));
    let best_path = completed_paths.first().unwrap();
    (
        best_path.0.iter().map(|x| x.to_string()).collect_vec(),
        best_path.1,
        best_path.2,
    )
}

type PairPath<'a> = (Vec<&'a str>, Vec<&'a str>, usize, usize, u32);
type PairPathString = (Vec<String>, Vec<String>, usize, usize, u32);

pub fn get_path_paired_search(
    dists_map: &HashMap<(&str, &str), usize>,
    rooms: &HashMap<String, Room>,
) -> PairPathString {
    let visited_you: Vec<&str> = vec!["AA"];
    let visited_elephant: Vec<&str> = vec!["AA"];
    let remaining: HashSet<&str> = HashSet::from_iter(
        rooms
            .iter()
            .filter(|(k, _)| *k != "AA")
            .map(|(k, _)| k.as_str()),
    );
    let mut completed_paths: Vec<PairPath> = Vec::new();
    let mut queue = VecDeque::new();
    queue.push_front((visited_you, visited_elephant, remaining, 26, 26, 0));

    let mut current_best: PairPath = (Vec::new(), Vec::new(), 0, 0, 0);

    // Begin DFS
    while let Some((
        visited_you,
        visited_elephant,
        remaining,
        current_you_time,
        current_elephant_time,
        current_release,
    )) = queue.pop_front()
    {
        let current_you = *visited_you.last().unwrap();
        let current_elephant = *visited_elephant.last().unwrap();
        if !completed_paths.is_empty() {
            let current_best = completed_paths[0].4;
            let max_time = current_you_time.max(current_elephant_time);
            // If all opened in next step, would it be worse than current best? If so, stop exploring this path
            if current_release
                + remaining
                    .iter()
                    .map(|x| rooms.get(*x).unwrap().rate * max_time as u32)
                    .sum::<u32>()
                <= current_best
            {
                continue;
            }
        }

        // If remaining is empty or both clocks are 0
        if remaining.is_empty() || (current_you_time == 0 && current_elephant_time == 0) {
            completed_paths.push((
                visited_you.clone(),
                visited_elephant.clone(),
                current_you_time,
                current_elephant_time,
                current_release,
            ));
            completed_paths.sort_by(|a, b| b.4.cmp(&a.4));
            let new_best = completed_paths.first().unwrap();
            if current_best.4 < new_best.4 {
                current_best = new_best.clone();
                println!("Current best: {:?}", current_best);
            }
            continue;
        }

        // Move you
        if current_you_time >= current_elephant_time {
            for &next_you in remaining.iter() {
                let dist_you = dists_map.get(&(current_you, next_you)).unwrap();
                // Next time
                let next_you_time = if current_you_time > *dist_you {
                    current_you_time - dist_you - 1
                } else {
                    0
                };
                // Update remaining
                let mut new_remaining = remaining.clone();
                new_remaining.remove(next_you);

                // Update release
                let rate_you = rooms.get(next_you).unwrap().rate;
                let new_release = current_release + rate_you * next_you_time as u32;

                // Update visited
                let mut next_visited = visited_you.clone();
                next_visited.push(next_you);
                queue.push_front((
                    next_visited,
                    visited_elephant.clone(),
                    new_remaining,
                    next_you_time,
                    current_elephant_time,
                    new_release,
                ));
            }
        }
        // Move elephant
        else {
            // Loop over remaining
            for &next_elephant in remaining.iter() {
                let dist_elephant = dists_map.get(&(current_elephant, next_elephant)).unwrap();
                // Next time
                let next_elephant_time = if current_elephant_time > *dist_elephant {
                    current_elephant_time - dist_elephant - 1
                } else {
                    0
                };
                // Update remaining
                let mut new_remaining = remaining.clone();
                new_remaining.remove(next_elephant);

                // Update release
                let rate_elephant = rooms.get(next_elephant).unwrap().rate;
                let new_release = current_release + rate_elephant * next_elephant_time as u32;

                // Update visited
                let mut next_visited = visited_elephant.clone();
                next_visited.push(next_elephant);
                queue.push_front((
                    visited_you.clone(),
                    next_visited,
                    new_remaining,
                    current_you_time,
                    next_elephant_time,
                    new_release,
                ));
            }
        }
    }

    completed_paths.sort_by(|a, b| b.4.cmp(&a.4));
    let best_path = completed_paths.first().unwrap();
    (
        best_path.0.iter().map(|x| x.to_string()).collect_vec(),
        best_path.1.iter().map(|x| x.to_string()).collect_vec(),
        best_path.2,
        best_path.3,
        best_path.4,
    )
}

pub fn part_one(input: &str) -> Option<u32> {
    // Read initial graph
    let rooms = read_input(input);

    // Valve room to room distance map
    let dists_map = get_distance_map(&rooms);

    // Get best path
    let path = get_path(&dists_map, &rooms);

    println!("{:?}", path);
    Some(path.2)
}

pub fn part_two(input: &str) -> Option<u32> {
    // Read initial graph
    let rooms = read_input(input);

    // Valve room to room distance map
    let dists_map = get_distance_map(&rooms);

    // Get best path
    let path = get_path_paired_search(&dists_map, &rooms);

    println!("{:?}", path);
    Some(path.4)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 16);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 16);
        assert_eq!(part_one(&input), Some(1651));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 16);
        assert_eq!(part_two(&input), Some(1707));
    }
}
