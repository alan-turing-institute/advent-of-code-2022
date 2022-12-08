#lang racket

(module+ main
  (require threading)

  (define *input* (with-input-from-file "input.txt" port->lines))

  (define *trees*
    (~>> *input*
         (map string->list)
         (map (λ (s) (map string s)))
         (map (λ (s) (map string->number s)))))

  ;; Part 1
  (count (λ (a b c d) (or a b c d))
         (flatten (visible? *trees*))                             
         (flatten ((with-transform visible? flip) *trees*))
         (flatten ((with-transform visible? transpose) *trees*))
         (flatten ((with-transform visible? flip transpose) *trees*)))

  ;; Part 2
  (apply max
    (map *
     (flatten (view-distance *trees*))                                     ; from left
     (flatten ((with-transform view-distance flip) *trees*))               ; from right
     (flatten ((with-transform view-distance transpose) *trees*))          ; from top
     (flatten ((with-transform view-distance flip transpose) *trees*))))

  )


(module+ test
  (require threading)

  (define *eg* #<<END
30373
25512
65332
33549
35390
END
    )

  (define *trees*
    (~>> (with-input-from-string *eg* port->lines)
         (map string->list)
         (map (λ (s) (map string s)))
         (map (λ (s) (map string->number s)))))

  ;; Part 1
  (count (λ (a b c d) (or a b c d))
         (flatten (visible? *trees*))                                     ; from left
         (flatten ((with-transform visible? flip) *trees*))               ; from right
         (flatten ((with-transform visible? transpose) *trees*))          ; from top
         (flatten ((with-transform visible? flip transpose) *trees*)))    ; from bottom

  ;; Part 2
  (apply max
    (map *
     (flatten (view-distance *trees*))                                     ; from left
     (flatten ((with-transform view-distance flip) *trees*))               ; from right
     (flatten ((with-transform view-distance transpose) *trees*))          ; from top
     (flatten ((with-transform view-distance flip transpose) *trees*))))


  )




;;---------------------------------------------------------------------------------------------------

;; The first element of the result is init
(define (scan proc init xs)
  (for/fold ([acc init]
             [ls '()]
             #:result (reverse ls))
            ([x (in-list xs)])
    (let ([v (proc x acc)])
      (values v (cons acc ls )))))

(define (scan/max xs)
  (scan max -1 xs))


;; Counting visibility 

(define (with-transform proc . Ts)
  (apply compose (append (reverse Ts) (cons proc Ts))))

;; transpose : [List-of list?] -> [List-of list?]
;; eg, '((1 a) (2 b)) -> '((1 2) (a b))
(define (transpose xss)
  (apply map list xss))

(define flip (curry map reverse))

(define (in-tails xs)
  (if (null? xs)
      empty-stream
      (stream-cons xs (in-tails (cdr xs)))))


;; count-visible : [List-of [List-of number?]] -> number?
(define (visible? xss)
  (define (visible/row? xs)
    (map > xs (scan/max xs)))
  (map visible/row? xss))


;; Compute viewing distance to the right
(define (view-distance/row/from-first v xs)
  (if (null? xs)
      0 ; on the right-hand edge
      (for/sum ([x xs]
                #:final (>= x v))
        1)))

(define (view-distance/row xs)
  (for/list ([lst (in-tails xs)])
    (view-distance/row/from-first (car lst) (cdr lst))))

(define (view-distance xss)
  (map view-distance/row xss))
