#lang racket

(module+ main
  (require threading)

  ;; (define *input*
  ;;   (with-input-from-file "input.txt" port->string))
  
  (define *input* #<<END
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
END
    )

  (define *cubes*
    (~> *input*
        (string-split _ "\n")
        (map (λ (l)
               (map string->number (string-split l ","))) _)))

  ;; Part 1
  (printf "Part 1: ~a\n" (cubes-surface-area *cubes*))
  

  ;; Part 2
  ;; Plan:
  ;; 1. Start with a rectangular cuboid which just covers the droplet
  ;;    (to a depth of 1)
  ;; 2. Expand inwards repeatedly until no further expansion possible
  ;; 3. Compute the surface area of this shape
  ;; 4. Subtract the exterior surface area

  ;; The corners of the enclosing cuboid
  (define *bbox*
    (list
     (list (apply min (map car *cubes*))
           (apply min (map cadr *cubes*))
           (apply min (map caddr *cubes*)))
     (list (apply max (map car *cubes*))
           (apply max (map cadr *cubes*))
           (apply max (map caddr *cubes*)))))

  (printf "Bounding box is ~a\n" *bbox*)
  
  ;; Construct the (hollow) enclosing cuboid
  (define *boundary*
    (match-let
        ([(list (list minx miny minz) (list maxx maxy maxz))
          (list (map sub1 (car *bbox*)) (map add1 (cadr *bbox*)))])
      (set-union
       (for*/set ([y (range miny (+ maxy 1))]
                  [z (range minz (+ maxz 1))])
         (list minx y z)) 
       (for*/set ([y (range miny (+ maxy 1))]
                  [z (range minz (+ maxz 1))])
         (list maxx y z)) 
       (for*/set ([x (range minx (+ maxx 1))]
                  [z (range minz (+ maxz 1))])
         (list x miny z)) 
       (for*/set ([x (range minx (+ maxx 1))]
                  [z (range minz (+ maxz 1))])
         (list x maxy z))
       (for*/set ([x (range minx (+ maxx 1))]
                  [y (range miny (+ maxy 1))])
         (list x y minz))
       (for*/set ([x (range minx (+ maxx 1))]
                  [y (range miny (+ maxy 1))])
         (list x y maxz)))
      ))
  
  ;; Make a set from the list of cubes
  (define *droplet* (list->set *cubes*))
  
  ;; Expand the boundary
  (define *fill* 
    (let expand ([bdry *boundary*]
                 [filled *droplet*]
                 [n 1])
      (printf "Expanding ~a\n" n)
      (if (set-empty? bdry)
          filled
          (let ([new-bdry (set-subtract
                           (cubes-expand bdry *bbox*)
                           filled)])
            (expand new-bdry (set-union filled bdry) (+ n 1))))))

  (printf "Surface area for Part 2: ~a\n"
          (-
           (cubes-surface-area (set-subtract *fill* *droplet*))
           (bounding-cuboid-surface-area *bbox*)))

  ;; 


  

  
  )

;; Compute the exposed surface area of a set of cubes
(define (cubes-surface-area cubes)
  (set-count
   (for/fold ([faces (set)])
             ([ cube cubes])
     (foldl set-xor faces (cube->faces cube)))))

(define ((flip f) x y) (f y x))

;; Every cube produces six faces
;; Each face is identified by its normal (x, y, or z)
;; and the coordinate of the cube to its "right"

(define (cube->faces pos)
  (match-define (list x y z) pos)
  (list
   `(x ,x ,y ,z)
   `(x ,(+ x 1) ,y ,z)
   `(y ,x ,y ,z)
   `(y ,x ,(+ y 1) ,z)
   `(z ,x ,y ,z)
   `(z ,x ,y ,(+ z 1))))

(define (set-xor v st)
  (if (set-member? st v)
      (set-remove st v)
      (set-add st v)))

;; is this cube within a bounding volume?
(define ((in-bounds? bbox) pos)
  (match-define (list x y z) pos)
  (match-define (list (list minx miny minz) (list maxx maxy maxz)) bbox)
  (and (<= x maxx)
       (>= x minx)
       (<= y maxy)
       (>= y miny)
       (<= z maxz)
       (>= z minz)))

;; Return the 6 cubes surrounding this one
(define (cube-expand cube bbox)
  (match-define (list x y z) cube)
  (list->set
   (filter (in-bounds? bbox) 
           `((,(+ x 1) ,y ,z)
             (,(- x 1) ,y ,z)
             (,x ,(+ y 1) ,z)
             (,x ,(- y 1) ,z)
             (,x ,y ,(+ z 1))
             (,x ,y ,(- z 1))))))

;; Return all the cubes surrounding these
;; but excluding these
;; and not outside the bound
(define (cubes-expand cubes bbox)
  (let ([cubes† 
         (for/fold ([expanded (set)])
                   ([cube (in-set cubes)])
           (set-union expanded (cube-expand cube bbox)))])
    (set-subtract cubes† cubes)))


;; Compute the "exterior surface area" of a bounding cuboid
(define (bounding-cuboid-surface-area bbox)
  (match-define
    (list δx δy δz) (map (curry - 3) (apply map - bbox)))
  (* 2 (+ (* δx δy) (* δx δz) (* δy δz))))
