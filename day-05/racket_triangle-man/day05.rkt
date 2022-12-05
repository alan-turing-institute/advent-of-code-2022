#lang racket

(module+ main
  (require threading)
  
  (define *eg* (with-input-from-file "input.txt" port->string))
  (match-define (list *stacks* *instructions*) (string-split *eg* "\n\n"))

  (define stacks
    (~>> *stacks*
         (string-split _ "\n")
         (map string->list)
         (map cdr)                ; Drop the first "["
         (map (every 4))          ; Pick out the letters by position
         transpose
         (map (λ (xs) (dropf xs (curry char=? #\space))))  ; Drop initial spaces
         (map (λ (xs) (drop-right xs 1)))                  ; Drop the final number
         (list->vector)))

  (define instructions
    (~>> *instructions*
         (string-split _ "\n")
         (map read-instruction)))

  ;; Part 1 or 2
  (execute-instructions! instructions stacks #:new-crane? #t)
  (list->string (map car (vector->list stacks)))
  
)

;; ---------------------------------------------------------------------------------------------------

;; read-instruction : string? -> list-of number?
;; Read, eg, "move 10 from 2 to 1" as '(10 1 0)
(define (read-instruction str)
  (let ([in (map string->number
                 (cdr (regexp-match #rx"move ([0-9]+) from ([0-9]+) to ([0-9]+)" str)))])
    (list (car in) (- (cadr in) 1) (- (caddr in) 1))))

;; execute-instruction! : instruction? [Vector-of list?]
;; Update the stacks after executing instruction
;; new-crane? if #t use crane 9001
(define (execute-instruction! ins stacks #:new-crane? (new-crane? #f))
  (define crane-op
    (if new-crane?
        values     ; identity function
        reverse))
  (match-define (list N from-idx to-idx) ins)
  (let ([from (vector-ref stacks from-idx)]
        [to   (vector-ref stacks to-idx)])
    (vector-set! stacks from-idx (drop from N))
    (vector-set! stacks to-idx (append (crane-op (take from N)) to))))

;; execute-instructions! : [list-of instruction?] [Vector-of list?]
;; Update the stacks after executing instructions
(define (execute-instructions! inss stacks #:new-crane? (new-crane? #f))
  (for ([ins inss])
    (execute-instruction! ins stacks #:new-crane? new-crane?)))

;; Utilities

;; every : number? -> (list? -> list?)
;; Take every nth entry in a list starting with the first
(define ((every n) xs)
  (for/list ([x xs]
             [m (in-naturals)]
             #:when (zero? (modulo m n)))
    x))

;; transpose : [List-of list?] -> [List-of list?]
;; eg, '((1 a) (2 b)) -> '((1 2) (a b))
(define (transpose xss)
  (apply map list xss))


;; ---------------------------------------------------------------------------------------------------

(module+ test
  (require threading)
  (define *eg*
    #<<END
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
END
    )

  (match-define (list *stacks* *instructions*) (string-split *eg* "\n\n"))

  (define stacks
    (~>> *stacks*
         (string-split _ "\n")
         (map string->list)
         (map cdr)                ; Drop the first "["
         (map (every 4))
         transpose
         (map (λ (xs) (dropf xs (curry char=? #\space))))  ; Drop initial spaces
         (map (λ (xs) (drop-right xs 1)))                  ; Drop the final number
         (list->vector)))

  ;; 
  (define instructions
    (~>> *instructions*
         (string-split _ "\n")
         (map read-instruction)))
  
  (execute-instructions! instructions stacks)

  (list->string (map car (vector->list stacks)))
  
  
  )
