use advent_of_code::helpers::{Line, Point};
use itertools::Itertools;
use regex::Regex;

// Part 1: Testing, Solving
const TEST_ROW: i64 = 10;
const SOLVE_ROW: i64 = 2000000;

// Part 2: Testing, Solving
const MAX_ROW_TEST: i64 = 20;
const MAX_ROW_SOLVE: i64 = 4000000;

fn read_input(input: &str) -> Vec<(Point<i64>, Point<i64>)> {
    let pattern = r"Sensor at x=(\-*\d+), y=(\-*\d+): closest beacon is at x=(\-*\d+), y=(\-*\d+)";
    let re: Regex = Regex::new(pattern).unwrap();
    let mut points = Vec::<(Point<i64>, Point<i64>)>::new();
    for cap in re.captures_iter(input) {
        points.push((
            Point::<i64>::new(
                cap[1].parse::<i64>().unwrap(),
                cap[2].parse::<i64>().unwrap(),
            ),
            Point::<i64>::new(
                cap[3].parse::<i64>().unwrap(),
                cap[4].parse::<i64>().unwrap(),
            ),
        ));
    }
    points
}

fn union_x_many(lines: &mut [Line<i64>]) -> Vec<Line<i64>> {
    lines.sort();
    let mut v = Vec::<Line<i64>>::new();
    v.push(*lines.first().unwrap());
    lines.iter().skip(1).fold(v, |mut v, next_line| {
        if let Some(line_union) = v.last().unwrap().union_x(next_line) {
            v.pop();
            v.push(line_union);
        } else {
            v.push(*next_line);
        }
        v
    })
}

pub fn part_one(input: &str, row_idx: i64) -> Option<i64> {
    let pairs = read_input(input);
    let mut row: Vec<Line<i64>> = Vec::new();
    for (sensor, beacon) in pairs {
        let distance = sensor.manhattan(&beacon);
        let row_diff = (sensor.y - row_idx).abs();
        let x_range = distance - row_diff;
        let line_of_points = Line::<i64>::new(
            &Point::<i64>::new(sensor.x - x_range, row_idx),
            &Point::<i64>::new(sensor.x + x_range, row_idx),
        );

        if x_range >= 0 {
            row.push(line_of_points);
        }
    }
    Some(
        union_x_many(&mut row)
            .iter()
            .map(|line| line.length())
            .sum::<i64>(),
    )
}

pub fn part_one_test(input: &str) -> Option<i64> {
    part_one(input, TEST_ROW)
}

pub fn part_one_solve(input: &str) -> Option<i64> {
    part_one(input, SOLVE_ROW)
}

pub fn part_two(input: &str, min_row: i64, max_row: i64) -> Option<i64> {
    let pairs = read_input(input);
    let mut rows: Vec<Vec<Line<i64>>> = vec![Vec::new(); (max_row - min_row) as usize];
    for (sensor, beacon) in pairs {
        let distance = sensor.manhattan(&beacon);
        for row_diff in -distance..distance {
            let row_idx = sensor.y + row_diff;
            if !(min_row..max_row).contains(&row_idx) {
                continue;
            }
            let x_range = distance - row_diff.abs();
            let line_of_points = Line::<i64>::new(
                &Point::<i64>::new(sensor.x - x_range, row_idx),
                &Point::<i64>::new(sensor.x + x_range, row_idx),
            );
            rows[row_idx as usize].push(line_of_points);
        }
    }

    let mut location_to_find: Option<Point<i64>> = None;
    for row in rows.iter_mut() {
        for (left, right) in union_x_many(row).iter().tuple_windows() {
            if left.end.x >= min_row && left.end.x < max_row && right.start.x > left.end.x + 1 {
                location_to_find = Some(Point::<i64>::new(left.end.x + 1, left.end.y));
                break;
            }
        }
        if location_to_find.is_some() {
            break;
        }
    }
    location_to_find.map(|location_to_find| location_to_find.x * 4000000 + location_to_find.y)
}

pub fn part_two_test(input: &str) -> Option<i64> {
    part_two(input, 0, MAX_ROW_TEST)
}

pub fn part_two_solve(input: &str) -> Option<i64> {
    part_two(input, 0, MAX_ROW_SOLVE)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 15);
    advent_of_code::solve!(1, part_one_solve, input);
    advent_of_code::solve!(2, part_two_solve, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 15);
        assert_eq!(part_one_test(&input), Some(26));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 15);
        assert_eq!(part_two_test(&input), Some(56000011));
    }
}
