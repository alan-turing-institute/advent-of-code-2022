#lang racket

(module+ main
  (require threading)

 ;;  (define *input* #<<END
;; [1,1,3,1,1]
;; [1,1,5,1,1]

;; [[1],[2,3,4]]
;; [[1],4]

;; [9]
;; [[8,7,6]]

;; [[4,4],4,4]
;; [[4,4],4,4,4]

;; [7,7,7,7]
;; [7,7,7]

;; []
;; [3]

;; [[[]]]
;; [[]]

;; [1,[2,[3,[4,[5,6,7]]]],8,9]
;; [1,[2,[3,[4,[5,6,0]]]],8,9]
;; END
;; )

  (define *input* (with-input-from-file "input.txt" port->string))
  
  (define *packets*
    (~> *input*
        (string-replace "," " ")
        (string-replace "\n\n" "\n")
        (string-split "\n")
        (map (λ (s) (with-input-from-string s read)) _)))

  ;; Part 1
  
  (for/sum
      ([ps (cons-by-two *packets*)]
       [idx (in-naturals 1)]
       #:when (= 1 (packet-compare (car ps) (cdr ps))))
    idx)

  ;; Part 2

  (for/product
      ([p (sort (list* '((2)) '((6)) *packets*)
                 (λ (p1 p2) (equal? (packet-compare p1 p2) 1)))]
       [idx (in-naturals 1)]
       #:when (or (equal? p '((2))) (equal? p '((6)))))
    idx)
  
  )

;; ---------------------------------------------------------------------------------------------------

(define (cons-by-two xs)
  (reverse
   (let loop ([xs xs]
              [acc '()])
     (if (null? xs)
         acc
         (loop (cddr xs)
               (cons (cons (car xs) (cadr xs)) acc))))))


;; Returns:
;; -1 if p1 > p2
;; 0  if p1 = p2
;; 1. if p1 < p2
(define (packet-compare p1 p2)
  ;; (printf "Comparing ~a and ~a\n" p1 p2)
  (match `(,p1 . ,p2)
    [(cons (? number? n1) (? number? n2))
     (cond
       [(< n1 n2) 1]
       [(= n1 n2) 0]
       [else     -1])]
    [(cons '() '())  0]
    [(cons '()   _)  1]
    [(cons   _ '()) -1]
    [(cons xs (? number? n)) (packet-compare xs (list n))]
    [(cons (? number? n) xs) (packet-compare (list n) xs)]
    [(cons (cons q1 q1s) (cons q2 q2s))
     (let ([c (packet-compare q1 q2)])
       (if (zero? c)
           (packet-compare q1s q2s)
           c))]))
