#lang racket

(require threading)

(define empty-string? (λ (x) (= (string-length x) 0)))

(define *elves*
  (for/fold ([elf   0]
             [elves '()]
             #:result elves)
            ([line (with-input-from-file "input.txt" port->lines)])
    (if (empty-string? line)
        (values 0 (cons elf elves))
        (values (+ elf (string->number line)) elves))))


;; Part 1

(apply max *elves*)

;; Part 2

(~>
 (sort *elves* >)
 (take _ 3)
 (apply + _))
