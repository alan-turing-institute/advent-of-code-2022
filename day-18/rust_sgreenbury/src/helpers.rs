/*
 * Use this file if you want to extract helpers from your solutions.
 * Example import from this file: `use advent_of_code::helpers::example_fn;`.
 */

use num::Integer;
use std::convert::TryFrom;
use std::{
    cmp::Ordering,
    fmt::Debug,
    io,
    ops::{Add, Sub},
};
pub fn wait() {
    let mut buffer = String::new();
    io::stdin()
        .read_line(&mut buffer)
        .map_err(|err| println!("{:?}", err))
        .ok();
}

#[derive(Copy, Clone, Hash, PartialEq, PartialOrd, Eq, Ord, Debug)]
pub struct Point<T: Integer> {
    pub x: T,
    pub y: T,
}
impl<T> Point<T>
where
    T: Integer + TryFrom<usize> + Copy,
    <T as std::convert::TryFrom<usize>>::Error: Debug,
{
    pub fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
    pub fn offet(&self, offset: &Point<T>) -> Point<T> {
        *self - *offset
    }
    pub fn manhattan(&self, other: &Point<T>) -> T {
        let d1 = if self.x > other.x {
            self.x - other.x
        } else {
            other.x - self.x
        };
        let d2 = if self.y > other.y {
            self.y - other.y
        } else {
            other.y - self.y
        };
        assert!(d1 + d2 >= T::try_from(0).unwrap());
        d1 + d2
    }
}

impl<T: Integer> Add for Point<T> {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl<T: Integer> Sub for Point<T> {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Direction {
    Right,
    Left,
    Down,
    Up,
    None,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Line<T: Integer> {
    pub start: Point<T>,
    current: Option<Point<T>>,
    pub end: Point<T>,
    direction: Direction,
    length: T,
}

impl<T: Integer> Ord for Line<T> {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.start.x.cmp(&other.start.x)
    }
}
impl<T: Integer> PartialOrd for Line<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<T> Line<T>
where
    T: Integer + TryFrom<usize> + Copy,
    <T as std::convert::TryFrom<usize>>::Error: Debug,
{
    pub fn new(start: &Point<T>, end: &Point<T>) -> Self {
        let (direction, length) = if start.x == end.x && start.y < end.y {
            (Direction::Down, end.y - start.y)
        } else if start.x == end.x && start.y > end.y {
            (Direction::Up, start.y - end.y)
        } else if start.x < end.x && start.y == end.y {
            (Direction::Right, end.x - start.x)
        } else if start.x > end.x && start.y == end.y {
            (Direction::Left, start.x - end.x)
        } else if start == end {
            (Direction::None, T::try_from(0).unwrap())
        } else {
            panic!("Diagonal!")
        };
        Self {
            start: *start,
            current: Some(*start),
            end: *end,
            direction,
            length,
        }
    }
    pub fn length(&self) -> T {
        self.length
    }
    pub fn union_x(&self, other: &Line<T>) -> Option<Line<T>> {
        assert!(self.start.y == self.end.y && other.start.y == other.end.y);
        if self.start.x >= other.start.x && self.end.x <= other.end.x {
            Some(*other)
        } else if other.start.x >= self.start.x && other.end.x <= self.end.x {
            Some(*self)
        } else if self.end.x >= other.start.x && self.start.x <= other.start.x {
            Some(Line::new(
                &Point::new(self.start.x, self.start.y),
                &Point::new(other.end.x, other.end.y),
            ))
        } else if other.end.x >= self.start.x && other.start.x <= self.start.x {
            Some(Line::new(
                &Point::new(other.start.x, other.start.y),
                &Point::new(self.end.x, self.end.y),
            ))
        } else {
            None
        }
    }
}

impl<T> Iterator for Line<T>
where
    T: Integer + TryFrom<usize> + Copy,
    <T as std::convert::TryFrom<usize>>::Error: Debug,
{
    type Item = Point<T>;
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.current;
        if let Some(ref point) = self.current {
            let one: T = T::try_from(1).unwrap();
            self.current = match self.direction {
                Direction::Right if point.x < self.end.x => {
                    Some(Point::new(point.x + one, point.y))
                }
                Direction::Right => None,
                Direction::Left if point.x > self.end.x => Some(Point::new(point.x - one, point.y)),
                Direction::Left => None,
                Direction::Down if point.y < self.end.y => Some(Point::new(point.x, point.y + one)),
                Direction::Down => None,
                Direction::Up if point.y > self.end.y => Some(Point::new(point.x, point.y - one)),
                Direction::Up => None,
                Direction::None => None,
            };
            current
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_xunion() {
        let a = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        let b = Line::<i32>::new(&Point::<i32>::new(-3, 2), &Point::<i32>::new(10, 2));
        let expected = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(10, 2));
        assert_eq!(expected, a.union_x(&b).unwrap());

        let b = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        let a = Line::<i32>::new(&Point::<i32>::new(-3, 2), &Point::<i32>::new(10, 2));
        let expected = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(10, 2));
        assert_eq!(expected, a.union_x(&b).unwrap());

        let a = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        let b = Line::<i32>::new(&Point::<i32>::new(5, 2), &Point::<i32>::new(10, 2));
        let _expected = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(10, 2));
        assert!(a.union_x(&b).is_none());

        let a = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        let b = Line::<i32>::new(&Point::<i32>::new(-2, 2), &Point::<i32>::new(2, 2));
        let expected = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        assert_eq!(expected, a.union_x(&b).unwrap());

        let b = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        let a = Line::<i32>::new(&Point::<i32>::new(-2, 2), &Point::<i32>::new(2, 2));
        let expected = Line::<i32>::new(&Point::<i32>::new(-4, 2), &Point::<i32>::new(4, 2));
        assert_eq!(expected, a.union_x(&b).unwrap());
    }
}
