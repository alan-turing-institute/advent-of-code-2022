#lang racket/base

(require racket/vector)

;; Mutable 2d vectors

(provide (struct-out grid)
         make-grid
         grid-ref
         grid-set!
         grid-fill!
         grid-ncols
         grid-nrows
         grid->lists
         lists->grid
         grid-member
         grid-indexes-of
         )

(struct grid (vec cols) #:transparent)

;; Make an m (cols) x n (rows) grid
(define (make-grid m n v)
  (grid (make-vector (* m n) v) m))

;; A position is a pair, (row . col)
;; Note that col changes fasted when accessing vec in order
(define (grid-ref g pos)
  (vector-ref (grid-vec g) (+ (cdr pos) (* (car pos) (grid-cols g)))))

(define (grid-set! g pos v)
  (vector-set! (grid-vec g) (+ (cdr pos) (* (car pos) (grid-cols g))) v))

(define (grid-fill! g v)
  (vector-fill! (grid-vec g) v))

(define (grid-ncols g)
  (grid-cols g))

(define (grid-nrows g)
  (/ (vector-length (grid-vec g)) (grid-cols g)))

(define (grid-member v g)
  (let ([vpos (vector-member v (grid-vec g))])
    (call-with-values (λ () (quotient/remainder vpos (grid-cols g))) cons)))

(define (grid->lists g)
  (for/list ([r (grid-nrows g)])
    (for/list ([c (grid-ncols g)])
      (grid-ref g `(,r . ,c)))))

;; xss is a non-empty list of non-empty lists
(define (lists->grid xss)
  (let ([vec (apply vector-append (map list->vector xss))])
    (grid vec (length (car xss)))))

;; Return a list of positions where v occurs
(define (grid-indexes-of g v)
  (for*/list ([r (grid-nrows g)]
              [c (grid-ncols g)]
              #:when (equal? (grid-ref g `(,r . ,c)) v)
              )
    (cons r c)))
             
