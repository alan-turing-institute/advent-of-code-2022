#lang racket

(require "grid.rkt")

(module+ main

  (require threading)

  (define *input*
    (with-input-from-file "input.txt" port->string))
  
;;   (define *input* #<<END
;; 498,4 -> 498,6 -> 496,6
;; 503,4 -> 502,4 -> 502,9 -> 494,9
;; END
;;     )

  ;; read-line : string? -> [List-of position?]
  (define (read-line str)
    (define (snoc x y) (cons y x))
    (define (read-pos str)
      (apply snoc
             (map string->number (string-split str ","))))
    (map read-pos
         (string-split str " -> ")))
  
  (define *coords* 
    (~> *input*
        (string-split "\n")
        (map read-line _)))
  
  ;; Our grid columns will go from *min-x* to *max-x*
  ;; and rows from 0 to *max-y* 
  (define-values (*max-x* *min-x* *max-y* *min-y*)
    (let ([deepmap
           (λ (proc lol) (flatten (map (λ (ls) (map proc ls)) lol)))])
      (let ([xs (deepmap cdr *coords*)]
            [ys (deepmap car *coords*)])
        (values
         (+ (apply max xs) 1) ; allow a column of air on the right
         (- (apply min xs) 1) ; ... and on the left
         (apply max ys)
         (apply min ys)))))

  ;; Part 1

  (define *cave*
    (make-cave *coords* *max-x* *min-x* *max-y*))
  
  (make-sandpile! *cave* `(0 . ,(- 500 *min-x*)))

  (count (λ (p) (eq? p 'sand))
         (flatten (grid->lists *cave*)))

  ;; Part 2

  (define *max-x*† (max (+ 502 *max-y*) *max-x*))
  (define *min-x*† (min (- 498 *max-y*) *min-x*))
  
  (define *cave*†
    (make-cave *coords* *max-x*† *min-x*† (+ *max-y* 1)))
  
  (make-sandpile!† *cave*† `(0 . ,(- 500 *min-x*†)))

  ;; Answer is one more than this
  (count (λ (p) (eq? p 'sand))
         (flatten (grid->lists *cave*†)))

  
  )


;; --------------------------------------------------------------------------------------------------- 

;; show-tile
(define (show-tile tile)
  (match tile
    ['air #\.]
    ['rock #\#]
    ['sand #\o]))

;; show-cave
(define (show-cave cave)
  (for-each
   (λ (tiles) (displayln (list->string (map show-tile tiles))))
   (grid->lists cave)))


;; make-cave
(define (make-cave rocklines max-x min-x max-y)
  (define cave
    (make-grid (+ (- max-x min-x) 1) (+ max-y 1) 'air))
  (for ([rockline (in-list rocklines)])
    (for ([rock (rocks-along rockline)])
      (grid-set! cave (translate rock (cons 0 (- min-x)) 1) 'rock)))
  cave)

;; Given a list of corners, return a stream of rock positions
(define (rocks-along rockline)
  (rocks-along/from-start (car rockline) (cdr rockline)))

(define (rocks-along/from-start start-rock rockline)
  (if (null? rockline)
      (stream-cons start-rock empty-stream)
      (let ([next-rock (car rockline)])
        (let ([Δ (direction-from start-rock next-rock)])
          (stream-append
           (for/list ([n (manhattan-dist start-rock next-rock)])
             (translate start-rock Δ n))
           (rocks-along/from-start next-rock (cdr rockline)))))))

;; Moving sand

;; For part 1

;; Drop a piece of sand
;; Returns either:
;; - 'abyss (the sand fell for ever), or
;; - a position? (the final resting place)
(define (drop-sand cave pos)
  (define last-row (- (grid-nrows cave) 1))
  (let step ([pos pos])
    (if (= (car pos) last-row)
        'abyss
        (let ([down (translate pos '(1 . 0) 1)])
          (if (eq? (grid-ref cave down) 'air)
              (step down)
              (let ([down-left (translate pos '(1 . -1) 1)])
                (if (eq? (grid-ref cave down-left) 'air)
                    (step down-left)
                    (let ([down-right (translate pos '(1 . 1) 1)])
                      (if (eq? (grid-ref cave down-right) 'air)
                          (step down-right)
                          pos)))))))))

;; Repeatedly add sand until overflow
(define (make-sandpile! cave start)
  (let loop ()
    (let ([resting-place (drop-sand cave start)])
      (unless (eq? resting-place 'abyss)
        (begin
          (grid-set! cave resting-place 'sand)
          (loop))))))

;; For part 2

;; Drop a piece of sand
;; Returns a position? (the final resting place)
;; Assumes there is a floor at last-row + 1
(define (drop-sand† cave pos)
  (define last-row (- (grid-nrows cave) 1))
  (let step ([pos pos])
    (if (= (car pos) last-row)
        pos
        (let ([down (translate pos '(1 . 0) 1)])
          (if (eq? (grid-ref cave down) 'air)
              (step down)
              (let ([down-left (translate pos '(1 . -1) 1)])
                (if (eq? (grid-ref cave down-left) 'air)
                    (step down-left)
                    (let ([down-right (translate pos '(1 . 1) 1)])
                      (if (eq? (grid-ref cave down-right) 'air)
                          (step down-right)
                          pos)))))))))

;; Repeatedly add sand until overflow
(define (make-sandpile!† cave start)
  (let loop ()
    (let ([resting-place (drop-sand† cave start)])
      (unless (equal? resting-place start)
        (begin
          (grid-set! cave resting-place 'sand)
          (loop))))))


;; ---------------------------------------------------------------------------------------------------

;; Utilities for positions.
;; Really should move to the grid module)

(define (manhattan-dist p1 p2)
  (+ (abs (- (car p1) (car p2)))
     (abs (- (cdr p1) (cdr p2)))))

(define (direction-from p1 p2)
  (cons
   (sgn (- (car p2) (car p1)))
   (sgn (- (cdr p2) (cdr p1)))))

;; Translate p1 by m * d
(define (translate p1 d m)
  (cons (+ (car p1) (* m (car d)))
        (+ (cdr p1) (* m (cdr d)))))
