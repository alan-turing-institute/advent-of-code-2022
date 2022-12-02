#lang racket

(require threading)

;; Coding scheme for rock-paper-scissors:
;; 0 : Rock
;; 1 : Paper
;; 2 : Scissors

;; A game is a pair (them . you) where `them` is opponent's play; and `you` is your play

;; string? -> game?
(define (parse-game str)
  (match-define (list them _ you) (string->list str))
  (cons
   (match them
     [#\A 0]
     [#\B 1]
     [#\C 2])
   (match you
     [#\X 0]
     [#\Y 1]
     [#\Z 2])))

;; For part 2. Here "you" is your desired end state
;; game? -> game?
(define/match (play-game game)
  [((cons them you))
   (cons them (modulo (+ them (- you 1)) 3))])

(define/match (score-game game)
  [((cons them you))
   (+ (match (modulo (- you them) 3)
        [0 3] ; Draw
        [1 6] ; Win
        [2 0] ; Loss
        )
      (+ you 1))])

;; Example

(define *eg*
  (with-input-from-string #<<END
A Y
B X
C Z
END
port->lines))

(define *games* (with-input-from-file "input.txt" port->lines))

;; Part 1

(apply +
       (map (compose score-game parse-game) *games*))

;; Part 2

(apply +
       (map (compose score-game play-game parse-game) *games*))

