#lang racket

(module+ main

  (define *moves*
    (expand-moves
     (map read-line
          (with-input-from-file "input.txt" port->lines))))

  ;; Part 1
  
  (define *breadcrumbs* 
    (for/fold ([hd '(0 . 0)]
               [tl '(0 . 0)]
               [breadcrumbs (list '(0 . 0))]
               #:result breadcrumbs)
              ([mv (in-stream *moves*)])
      (let* ([new-hd (move mv hd)]
             [new-tl (follow-the-leader new-hd tl)])
        (values new-hd
                new-tl
                (cons new-tl breadcrumbs)))))
  
  (length (remove-duplicates *breadcrumbs*))

  ;; Part 2
  
  (define *breadcrumbs2*
    (for/fold ([knots (make-list 10 '(0 . 0))]
               [breadcrumbs (list '(0 . 0))]
               #:result breadcrumbs)
              ([mv (in-stream *moves*)])
      (let-values ([(new-knots new-tl) (move-rope mv knots)])
        (values new-knots (cons new-tl breadcrumbs))))
    )
  
  (length (remove-duplicates *breadcrumbs2*))

  
  )

;; ---------------------------------------------------------------------------------------------------

;; A direction? is a pair (dir . val) where
;; dir is 'up, 'down, 'left, or 'right; and val is an integer
(define (read-line str)
  (match-let ([(list dir dist) (string-split str)])
    (let ([val (string->number dist)])
      (match dir
        ["U" (cons 'up    val)]
        ["D" (cons 'down  val)]
        ["L" (cons 'left  val)]
        ["R" (cons 'right val)]))))

;; Produce a stream of single instructions,
;; eg. '((up . 2) (down . 1)) becomes '(up up down)
(define (expand-moves mvs)
  (if (null? mvs)
      empty-stream
      (let ([next-move (car mvs)]
            [remainder (cdr mvs)])
        (stream-append
         (make-list (cdr next-move) (car next-move))
         (expand-moves remainder)))))

;; Move pos according to mv
(define (move mv pos)
  (match-let ([(cons x y) pos])
    (match mv
      ['up    (cons x (+ y 1))]
      ['down  (cons x (- y 1))]
      ['left  (cons (- x 1) y)]
      ['right (cons (+ x 1) y)])))

;; Update tail to follow head
;; head and tail are pairs (x . y)
(define (follow-the-leader head tail)
  (match-let ([(cons hx hy) head]
              [(cons tx ty) tail])
    (let ([Δx (- hx tx)]
          [Δy (- hy ty)])
      (if (or (> (abs Δx) 1)
              (> (abs Δy) 1))
          (cons (+ tx (sgn Δx))
                (+ ty (sgn Δy)))
          tail))))

;; Move an entire rope
;; Returns (values new-knots new-tail)
(define (move-rope mv knots)
  (let ([hd  (car knots)]
        [tls (cdr knots)])
    (for/fold ([last-knot (move mv hd)]
               [new-knots '()]
               #:result (values (reverse (cons last-knot new-knots)) last-knot))
              ([knot tls])
      (let ([new-knot (follow-the-leader last-knot knot)])
        (values new-knot (cons last-knot new-knots))))))


;; ---------------------------------------------------------------------------------------------------
;; TESTING

(module+ test

  (define *input* #<<END
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
END
    )
  (define *moves*
    (expand-moves
     (map read-line
          (with-input-from-string *input* port->lines))))

  ;; Part 1
  
  (define *breadcrumbs* 
    (for/fold ([hd '(0 . 0)]
               [tl '(0 . 0)]
               [breadcrumbs (list '(0 . 0))]
               #:result breadcrumbs)
              ([mv (in-stream *moves*)])
      (let* ([new-hd (move mv hd)]
             [new-tl (follow-the-leader new-hd tl)])
        (values new-hd
                new-tl
                (cons new-tl breadcrumbs)))))

  (length (remove-duplicates *breadcrumbs*))

  ;; Part 2

  (define *input2* #<<END
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
END
    )

  (define *moves2*
    (expand-moves
     (map read-line
          (with-input-from-string *input2* port->lines))))
  
  (define *breadcrumbs2*
    (for/fold ([knots (make-list 10 '(0 . 0))]
               [breadcrumbs (list '(0 . 0))]
               #:result breadcrumbs)
              ([mv (in-stream *moves2*)])
      (let-values ([(new-knots new-tl) (move-rope mv knots)])
        (values new-knots (cons new-tl breadcrumbs))))
    )
  
  (length (remove-duplicates *breadcrumbs2*))
  
  )
