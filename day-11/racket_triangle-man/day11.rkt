#lang racket

(require "queue.rkt")

(module+ main
  (define *monkeys*
    (vector
     ;; 0
     (monkey (q 75 63)
             (λ (w) (* w 3))
             11
             7
             2)
     ;; 1
     (monkey (q 65 79 98 77 56 54 83 94)
             (λ (w) (+ w 3))
             2
             2
             0)
     ;; 2
     (monkey (q 66)
             (λ (w) (+ w 5))
             5
             7
             5)
     ;; 3
     (monkey (q 51 89 90)
             (λ (w) (* w 19))
             7
             6
             4)
     ;; 4
     (monkey (q 75 94 66 90 77 82 61)
             (λ (w) (+ w 1))
             17
             6
             1)
     ;; 5
     (monkey (q 53 76 59 92 95)
             (λ (w) (+ w 2))
             19
             4
             3)
     ;; 6
     (monkey (q 81 61 75 89 70 92)
             (λ (w) (* w w))
             3
             0
             1)
     ;; 7
     (monkey (q 81 86 62 87)
             (λ (w) (+ w 8))
             13
             3
             5)))
  
  ;; Part 1
  
  ;; (for ([i 20]) (round! *monkeys*))

  ;; (apply *
  ;;        (take
  ;;         (sort (vector->list (vector-map monkey-counter *monkeys*)) >)
  ;;         2))

;; Part 2
  
  (define *mod* (apply * (vector->list (vector-map monkey-divisor *monkeys*))))
  
  (for ([i 10000]) (round! *monkeys* *mod*))

  (apply *
         (take
          (sort (vector->list (vector-map monkey-counter *monkeys*)) >)
          2))

  )



;; ---------------------------------------------------------------------------------------------------

(struct monkey (items      ; queue?   
                op         ; number? -> number?
                divisor
                iftrue
                iffalse
                [counter #:auto #:mutable])
  #:auto-value 0
  #:transparent)


(define (q . items)
  (list->queue items))

(define (monkey-catch! mnky v)
  (push! (monkey-items mnky) v))

(define (monkey-add1! mnky)
  (set-monkey-counter! mnky (+ 1 (monkey-counter mnky))))

;; Run a round for monkey number m
(define (turn! monkeys m mod)
  (let ([mnky (vector-ref monkeys m)])
    (match-let ([(monkey items op divisor iftrue iffalse counter) mnky])
      (let loop ()
        (unless (queue-empty? items)
          (monkey-add1! mnky)
          (let* ([worry (pop! items)]
                 [new-worry (modulo (op worry) mod)]
                 ;; [new-worry (quotient (op worry) 3)]
                 )
            (if (zero? (modulo new-worry divisor))
                (monkey-catch! (vector-ref monkeys iftrue) new-worry)
                (monkey-catch! (vector-ref monkeys iffalse) new-worry))
            (loop)))))))

(define (round! monkeys mod)
  (for ([m (vector-length monkeys)])
    (turn! monkeys m mod)))

(module+ test

  (define *monkeys*
    (vector
     (monkey (q 79 98)
             (λ (w) (* w 19))
             23
             2
             3)
     (monkey (q 54 65 75 74)
             (λ (w) (+ w 6))
             19
             2
             0)
     (monkey (q 79 60 97)
             (λ (w) (* w w))
             13
             1
             3)
     (monkey (q 74)
             (λ (w) (+ w 3))
             17
             0
             1)))

  ;; Part 2

  (define *mod* (apply * (vector->list (vector-map monkey-divisor *monkeys*))))
  
  (for ([i 10000]) (round! *monkeys* *mod*))

  (apply *
         (take
          (sort (vector->list (vector-map monkey-counter *monkeys*)) >)
          2))

  )


