#lang racket

(module+ main

  (define *input*
    (with-input-from-file "input.txt" port->lines))
  
  (define *instructions*
    (map read-line *input*))

;; Part 1
  
  (define-values (c X *signal*)
    (for/fold ([cycle 1]        ; the cycle at the beginning of this operation 
               [X     1]        ; X register
               [signal/20 '()]) ; the signal every 20 cycles
              ([ins (in-list *instructions*)])
      (let-values ([(new-cycle new-X)
                    (match ins
                      ['(noop)    (values (+ cycle 1) X)]
                      [`(addx ,v) (values (+ cycle 2) (+ X v))])])
        (let ([output? (< (modulo
                           (- 40 (modulo (- cycle 20) 40))
                           40)
                          (- new-cycle cycle))])
          (values new-cycle
                  new-X
                  (if output?
                      (cons (* X (+ 20 (* 40 (quotient cycle 40)))) signal/20)
                      signal/20))))))

  (apply + *signal*)

  ;; Part 2

  (define *pixels* 
    (for/list ([X     (scanl/-1 + 1 (make-Δs *input*))]
               [cycle (in-naturals)])
      (<= (abs (- X (modulo cycle 40))) 1)))
  
  (for-each displayln (map list->string (crt *pixels*)))
  
  )

;; ---------------------------------------------------------------------------------------------------

;; Only used in Part 1
(define (read-line str)
  (match (string-split str)
    ['("noop") '(noop)]
    [(list "addx" v) `(addx ,(string->number v))]))

;; For Part 2, do a simpler thing
;; Convert input instructions to a list of changes to X,
;; one per cycle, padding with a 0 for addx
(define (make-Δs lines)
  (define (make-Δs-helper lines Δs)
    (if (null? lines)
        Δs
        (match (string-split (car lines))
          ['("noop")
           (make-Δs-helper (cdr lines) (cons 0 Δs))]
          [(list "addx" v)
           (make-Δs-helper (cdr lines) (list* (string->number v) 0 Δs))])))
  (reverse (make-Δs-helper lines '())))

;; Like scanl, but drop the last one 
(define (scanl/-1 proc init lst)
  (define (scan-proc v acc)    ; acc = (accn accn-1 ...)
    (let ([next (proc v (car acc))])
      (cons next acc)))
  (reverse (cdr (foldl scan-proc (list init) lst))))

(define (take-by n xs)
  (define (taker xs acc)
    (if (null? xs)
        acc
        (taker (drop xs n) (cons (take xs n) acc))))
  (reverse (taker xs '())))

(define (crt pixels)
  (take-by 40
           (map (λ (p) (if p #\# #\.)) pixels)))


;; ---------------------------------------------------------------------------------------------------

(module+ test
  (require threading)

  (define *input* #<<END
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
END
    )

  (define *instructions*
    (map read-line
         (with-input-from-string *input* port->lines)))

  (define-values (c X *signal*)
    (for/fold ([cycle 1]        ; the cycle at the beginning of this operation 
               [X     1]        ; X register
               [signal/20 '()]) ; the signal every 20 cycles
              ([ins (in-list *instructions*)])
      (let-values ([(new-cycle new-X)
                    (match ins
                      ['(noop)    (values (+ cycle 1) X)]
                      [`(addx ,v) (values (+ cycle 2) (+ X v))])])
        (let ([output? (< (modulo
                           (- 40 (modulo (- cycle 20) 40))
                           40)
                          (- new-cycle cycle))])
          (values new-cycle
                  new-X
                  (if output?
                      (cons (* X (+ 20 (* 40 (quotient cycle 40)))) signal/20)
                      signal/20))))))


  (apply + *signal*)

  ;; Part 2

  (define *pixels* 
    (for/list ([X     (scanl/-1 + 1 (make-Δs (string-split *input* "\n")))]
               [cycle (in-naturals)])
      (<= (abs (- X (modulo cycle 40))) 1)))
  
  
  
  )
