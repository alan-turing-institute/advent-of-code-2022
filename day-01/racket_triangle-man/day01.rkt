#lang racket

(require racket/function ; for curry
         threading)

;; Given a list of strings, some of which are empty, split the list at the empty strings to produce a
;; list of lists
(define (split-lines-on-blank xs)
  (let ([empty-string? (λ (x) (not (= (string-length x) 0)))])
    (if (null? xs)
        null
        (let-values
            ([(elf elves) (splitf-at xs empty-string?)])
          (if (null? elves)
              (list elf)
              (cons elf (split-lines-on-blank (cdr elves))))))))

(define *input*
  (let ([elves (~>
                (with-input-from-file "input.txt" port->lines)
                split-lines-on-blank)])
    (map (curry map string->number) elves)))

;; Part 1

;; *elves*: Total calories for each elf
(define *elves* (map (curry apply +) *input*))

(apply max *elves*)

;; Part 2

(~>
 (sort *elves* >)
 (take _ 3)
 (apply + _))
