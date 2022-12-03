#lang racket

;; A rucksack is a pair (compartment1 . compartment2)
;; where each compartment is a list of char?
;; and the lists have the same length

(module+ main
  (require threading)

  ;; Part 1
  
  (~>>
   (read-rucksacks (with-input-from-file "input.txt" port->lines))
   (map (compose priority common-item))
   (apply +))

  ;; Part 2

   (~>>
    (read-rucksacks (with-input-from-file "input.txt" port->lines))
    (group 3)
    (map (compose priority find-badge))
    (apply +))
  
  )


;; ---------------------------------------------------------------------------------------------------

;; read-rucksacks : list-of string -> list-of rucksack?
(define (read-rucksacks strs)
  (map (λ (rucksack)
         (let ([size     (/ (string-length rucksack) 2)]
               [contents (string->list rucksack)])
           (cons (take contents size) (drop contents size))))
       strs))

;; common-item : rucksack? -> char?
;; Identify the item common to both compartments
(define (common-item r)
  (let ([left (car r)]
        [right (cdr r)])
    (for/first ([l left]
                #:when (member l right))
      l)))

;; priority : char? -> number?
;; Return the priority of a character. Assumes a..z have consecutive codepoints, and likewise A..Z,
;; but does not assume an ordering between these two.
(define (priority c)
  (if (char-lower-case? c)
      (+ 1 (- (char->integer c) (char->integer #\a)))
      (+ 27 (- (char->integer c) (char->integer #\A)))))


;; Functions for Part 2

;; group : number? list? -> list-of list?
;; Group a list into groups of a particular size
(define (group n xs)
  (define (group-helper lists xs n)
    (if (null? xs)
        lists
        (group-helper (cons (take xs n) lists) (drop xs n) n)))
  (group-helper '() xs n))

;; find-badge : list-of rucksack? -> char?
;; Find the common element in a list of rucksacks
(define (find-badge rucksacks)
  (car ; there can be only one!
   (apply set-intersect
          (map (λ (r) (set-union (car r) (cdr r))) rucksacks))))

;; ---------------------------------------------------------------------------------------------------

(module+ test
  (require threading)
  (define *eg* #<<END
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
END
    )

  (~>>
   (read-rucksacks (with-input-from-string *eg* port->lines))
   (map (compose priority common-item))
   (apply +))

  (~>>
   (read-rucksacks (with-input-from-string *eg* port->lines))
   (group 3)
   (map find-badge)
   ))



