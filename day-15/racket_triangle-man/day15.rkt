#lang racket

(require data/integer-set) 

(module+ main
  (require threading)

;;   (define *input* #<<END
;; Sensor at x=2, y=18: closest beacon is at x=-2, y=15
;; Sensor at x=9, y=16: closest beacon is at x=10, y=16
;; Sensor at x=13, y=2: closest beacon is at x=15, y=3
;; Sensor at x=12, y=14: closest beacon is at x=10, y=16
;; Sensor at x=10, y=20: closest beacon is at x=10, y=16
;; Sensor at x=14, y=17: closest beacon is at x=10, y=16
;; Sensor at x=8, y=7: closest beacon is at x=2, y=10
;; Sensor at x=2, y=0: closest beacon is at x=2, y=10
;; Sensor at x=0, y=11: closest beacon is at x=2, y=10
;; Sensor at x=20, y=14: closest beacon is at x=25, y=17
;; Sensor at x=17, y=20: closest beacon is at x=21, y=22
;; Sensor at x=16, y=7: closest beacon is at x=15, y=3
;; Sensor at x=14, y=3: closest beacon is at x=15, y=3
;; Sensor at x=20, y=1: closest beacon is at x=15, y=3
;; END
;;     )

;; (define *the-y* 10)

  (define *input*
    (with-input-from-file "input.txt" port->string))
  (define *the-y* 2000000)

  (define *reports*
    (~>> *input*
         (string-split _ "\n")
         (map
          (λ~>>
           (regexp-match #rx"Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)")
           cdr
           (map string->number)))
         ))

  (define *sensors* (map (λ (r) (cons (car r) (cadr r))) *reports*))
  (define *beacons* (map (λ (r) (cons (caddr r) (cadddr r))) *reports*))
  (define *zones* (map report->zone *reports*))

  ;; Part 1
  
  (count
   (subtract
    (subtract
     (union* (filter-map (λ (z) (zone-scan-x z *the-y*)) *zones*))
     (positions-scan-x *sensors* *the-y*))
    (positions-scan-x *beacons* *the-y*)))

  ;; Part 2
  
  (for/or ([y* 4000001])
    (let ([xs (complement
               (union* (filter-map (λ (z) (zone-scan-x z y*)) *zones*))
               0 4000000)])
      (when (zero? (modulo y* 100000)) (display "."))
      (let ([x (get-integer xs)])
        (and x (cons x y*)))))

  
  )


;; input is a list (x y m n) where (x y) is the position of the sensor and (m n) the position of the
;; nearest beacon.
;; Returns a zone (x y r) where (x and y is the sensor and r the radius) In the zone
;; means manhattan-dist <= r

(define (report->zone in)
  (let ([x (car in)]
        [y (cadr in)]
        [m (caddr in)]
        [n (cadddr in)])
    (let ([r (manhattan-dist
              `(,x . ,y) `(,m . ,n))])
      (list x y r))))

(define (manhattan-dist p1 p2)
  (+ (abs (- (car p1) (car p2)))
     (abs (- (cdr p1) (cdr p2)))))

;; Compute the intersection of zone z with horizontal line at y*
;; Returns a pair of (inclusive) x-values, or #f
(define (zone-scan-x z y*)
  (match z
    [(list x y r) 
     (let ([δ (- r (abs (- y y*)))])
       (and (>= δ 0)
            (make-integer-set `((,(- x δ) . ,(+ x δ))))))]))

;; Which points in ps lie on y = y*?
(define (positions-scan-x ps y*)
  (union*
   (filter-map (λ (p)
                 (and (= (cdr p) y*)
                      (make-range (car p))))
               ps)))

;; Union of a list of integer-set?
(define (union* is)
  (foldl union
         (make-range)
         is))
