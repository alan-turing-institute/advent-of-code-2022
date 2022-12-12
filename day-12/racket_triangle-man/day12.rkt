#lang racket

(require "grid.rkt")


(module+ main
  (require threading)

;;   (define *input* #<<END
;; Sabqponm
;; abcryxxl
;; accszExk
;; acctuvwj
;; abdefghi
;; END
;; )

  (define *input* (with-input-from-file "input.txt" port->string))
  
  ;; Parsing
  
  (define *terrain*
    (~> *input*
        (with-input-from-string _ port->lines)
        (map string->list _)
        lists->grid))

  ;; Find start and end
  (define *start*
    (grid-member #\S *terrain*))

  (define *end*
    (grid-member #\E *terrain*))

  ;; And fix the grid
  (grid-set! *terrain* *start* #\a)
  (grid-set! *terrain* *end*   #\z)

  (define *heights*
    (struct-copy grid *terrain*
                 [vec (vector-map char->integer (grid-vec *terrain*))]))
  

  ;; Part 1

  (define *shortest-distances*
    (time (min-path *heights* *end*)))  ; For bragging points

  (grid-ref *shortest-distances* *start*)

  ;; Part 2 turns out to be solved already
  
  (apply min
         (filter-map (λ (p) (grid-ref *shortest-distances* p))
                     (grid-indexes-of *terrain* #\a)))
  
)  


;; ---------------------------------------------------------------------------------------------------  

;; is pos within the grid?
(define ((in-bounds? g) pos)
  (and
   (let ([row (car pos)])
     (and (>= row 0)
          (<  row (grid-nrows g))))
   (let ([col (cdr pos)])
     (and (>= col 0)
          (< col (grid-ncols g))))))

;; is `there` no more than one up from `here`? 
(define ((walkable? heights there) here)
  (<= (grid-ref heights there) (+ 1 (grid-ref heights here))))

;; Up to four grid locations from which one can reach pos
(define (whence heights pos)
  (let ([x (car pos)]
        [y (cdr pos)])
    (let ([nn (list (cons (+ x 1) y)
                    (cons (- x 1) y)
                    (cons x       (+ y 1))
                    (cons x       (- y 1)))])
      (filter (and/c (in-bounds? heights)
                     (walkable? heights pos))
              nn))))

;; Find the length of the minimum path from anywhere to `to`
(define (min-path heights to)
  (define distances (make-grid (grid-ncols heights) (grid-nrows heights) #f))
  (grid-set! distances to 0)
  ;; Expand boundary from search-nodes, returning new boundary
  (define (expand-known! search-nodes)
    ;; Debugging
    ;; (displayln "-----------------")
    ;; (for-each displayln (grid->lists distances))
    ;;
    (if (null? search-nodes)
        null?
        (let ([new-search-nodes
               (for/fold ([new-search-nodes '()])
                         ([node (in-list search-nodes)])
                 (let ([new-nodes (filter-not
                                   (λ (nd) (grid-ref distances nd))
                                   (whence heights node))])
                   (begin
                     (for-each
                      (λ (nd)
                        (grid-set! distances nd (+ (grid-ref distances node) 1)))
                      new-nodes)
                     (append new-nodes new-search-nodes))))])
          (expand-known! new-search-nodes))))
  (expand-known! (list to))
  distances)

