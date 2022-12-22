#lang racket
;; Tetris

(require racket/generator)


(module+ main

  (define *input* (car (with-input-from-file "input.txt" port->lines)))
  
  ;; (define *input* ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
   
  ;; pieces are list of rows (starting from the bottom); rows are lists of coordinates
  (define *pieces*
    '(((0 1 2 3))
      ((1) (0 1 2) (1))
      ((0 1 2) (2) (2))
      ((0) (0) (0) (0))
      ((0 1) (0 1))))

  ;; Part 1
  
  ;; chamber is a list of row
  
  (define *‹pieces›*
    (sequence->repeated-generator *pieces*))
   
  (define *‹gusts›* (sequence->repeated-generator *input*))

  (define-values (*end* *N*)
    (for/fold ([chamber '()]
               [gusts 0])
              ([p 2022])
      (let-values ([(gust-counter new-chamber)
                    (drop-piece (*‹pieces›*) *‹gusts›* chamber)])
        (values new-chamber (+ gusts gust-counter)))))

  (printf "Length *end*: ~a. Number of gusts: ~a\n" (length *end*) *N*)

  ;; Part 1 real answer: 3048
  ;; Part 1 example answer 3068
  
  ;; Part 2
  ;; 1,000,000,000,000

  ;; Repeatedly drop all the pieces until:
  ;; - we are back at the beginning of the gust sequence; and
  ;; - a (short) pattern of rows repeats  

  (define *‹pieces2›*
     (sequence->repeated-generator *pieces*))
  (define *N-pieces* (length *pieces*))
  
  (define *‹gusts2›* (sequence->repeated-generator *input*))
  (define *N-gusts* (string-length *input*))

  (define *pattern-length* 13) ;; Maybe?
  
  ;; Repeatedly drop all the pieces
  ;; when there have been a multiple of *N-gusts* gusts
  ;; *and* we are back at the beginning of the pieces
  ;; *and* the pattern matches
  ;; report the number of pieces

  (define *seen-patterns* (make-hash))


  (call/ec (λ (k)
             (for/fold ([chamber       '()]
                        [gusts         0])
                       ([n (in-range 1000)])
               (when (zero? (modulo n 1))
                 (printf "Group ~a, gust ~a. Gust modulo ~a is ~a. Height is ~a.\n"
                         n
                         gusts
                         *N-gusts*
                         (modulo gusts *N-gusts*)
                         (length chamber)))
               (let-values ([(new-chamber new-gusts)
                             (for/fold ([chmbr chamber]
                                        [gusts gusts])
                                       ([_ *N-pieces*])
                               (let-values ([(gust-counter new-chamber)
                                             (drop-piece (*‹pieces2›*) *‹gusts2›* chmbr)])
                                 (values new-chamber (+ gusts gust-counter))))])
                 (let ([new-pattern (and (> n 1) (take new-chamber *pattern-length*))]
                       [gust-position (modulo gusts *N-gusts*)])
                   (when (hash-has-key? *seen-patterns* (cons gust-position new-pattern)) 
                     (printf "Found it at group ~a, height ~a !\n" n (length chamber))
                     (k (hash-ref *seen-patterns* (cons gust-position new-pattern))))
                   (hash-set! *seen-patterns* (cons gust-position new-pattern) (cons n (length chamber))))
                 (values new-chamber new-gusts)))))

  ;; The calculation for the test case
  (+ 25 (* (- 78 25) (/ (- 1000000000000 (* 3 5)) 5 7)))

  ;; The calculation for the real case
  (+ 349 ; height after 45 groups of 5
     (* (- 2921 349) ; increase of height in repeating pattern of (- 387 45) = 342 groups (coincidence??)
        (quotient
         (/ ; number of groups after first part
          (- 1000000000000 (* 45 5)) ; number of pieces after first part
          5)
         (- 387 45)) ;; number of groups in repeating pattern
        )
     (- 1637 349) ; height of another 173 groups (to group 173 + 45 = 218)
     )
  
  )


;; ---------------------------------------------------------------------------------------------------


(define (append-reverse this that)
  (if (null? this)
      that
      (append-reverse (cdr this) (cons (car this) that))))


;; ---------------------------------------------------------------------------------------------------

(define chamber-width 7)

;; a row is a vector of length *width*
(define (empty-row)
  (make-vector chamber-width #f))

(define (show-tile t)
  (if t #\# #\.))

(define (show-chamber rows)
  (for-each (λ (row)
              (displayln
               (list->string (map show-tile (vector->list row)))))
            rows))

(define (piece-row-position-okay? x piece-row row)
  (for/and ([offset piece-row])
    (let ([px (+ offset x)])
      (and (>= px 0)
           (< px chamber-width)
           (not (vector-ref row px))))))

;; Can `piece` be placed at x? 
(define (can-move-to? x piece rows)
  (let check-rows ([piece-rows piece]
                   [rows rows])
    (and (or (null? piece-rows)
             (null? rows)
             (and (piece-row-position-okay? x (car piece-rows) (car rows))
                  (check-rows (cdr piece-rows) (cdr rows))))
         x)))

(define (vector-of-piece-row piece-row x)
  (let ([v (empty-row)])
    (for ([offset (in-list piece-row)])
      (vector-set! v (+ offset x) #t))
    v))

(define (merge-row v1 v2)
  (vector-map (λ (b1 b2) (or b1 b2)) v1 v2))

(define (merge-piece-and-rows piece x rows rows-above)
  ;;
  ;; (displayln "\nmerge-piece-and-rows")
  ;; (printf "     piece: ~a\n" piece)
  ;; (printf "         x: ~a\n" x)
  ;; (printf "      rows: ~a\n" rows)
  ;; (printf "rows-above: ~a\n" rows-above)
  ;;
  (if (null? rows-above)
      (if (null? piece)
          rows
          (merge-piece-and-rows (cdr piece)
                                x
                                (cons (vector-of-piece-row (car piece) x) rows)
                                null))
      (if (null? piece)
          (merge-piece-and-rows null
                                x
                                (cons (car rows-above) rows)
                                (cdr rows-above))
          (merge-piece-and-rows (cdr piece)
                                x
                                (cons (merge-row (vector-of-piece-row (car piece) x)
                                                 (car rows-above))
                                      rows)
                                (cdr rows-above)))))

;; Drop any blank rows from the top
(define (drop-blank-rows rows)
  (dropf rows  (λ (row) (not (ormap values (vector->list row))))))

;; Return the new state of the chamber, represented as a list of rows
;; piece : a piece
;; ‹gusts› : a generator of char?
;; rows : a list of vector? with the highest row first 
;; width : the width of the chamber
(define (drop-piece piece ‹gusts› rows)
  (let step ([rows (list* (empty-row) (empty-row) (empty-row) rows)]
             [rows-above '()]
             [x 2]
             [gust-counter 1])
    ;; (printf "x: ~a\n" x)
    ;; (show-chamber rows)
    ;; (newline)
    (let* ([δ (if (char=? (‹gusts›) #\<) -1 1)]
           [x†
            (or (can-move-to? (+ x δ) piece rows-above)
                x)])
      ;; (printf "Gust δ: ~a, x†: ~a\n" δ x†)
      (if (or (null? rows)
              (not (can-move-to? x† piece (cons (car rows) rows-above))))
          (values gust-counter
                  (drop-blank-rows
                   (merge-piece-and-rows piece x† rows rows-above)))
          (step (cdr rows) (cons (car rows) rows-above) x† (+ gust-counter 1))))))
