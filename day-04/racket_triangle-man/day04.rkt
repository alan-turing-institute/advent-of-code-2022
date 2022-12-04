#lang racket

(require (only-in data/integer-set
                  make-integer-set
                  subset?
                  intersect
                  get-integer))

(module+ main
  (require threading)

  (define *input*
    (~>>
     "input.txt"
     (with-input-from-file _ port->lines)
     (map read-line)))

  ;; Part 1
  (count (curry apply within?) *input*)

  ;; Part 2
  (count (curry apply overlap?) *input*)
  
  )


;; ---------------------------------------------------------------------------------------------------

;; read-line : string? -> [Pair-of integer-set?]
;; Read strings of the form "MM-NN,OO-PP", where MM... are numbers
(define (read-line str)
  (let ([in (map string->number
                 (cdr (regexp-match #rx"([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)" str)))])
    (list (make-integer-set `((,(car in) . ,(cadr in))))
          (make-integer-set `((,(caddr in) . ,(cadddr in)))))))

;; within? : integer-set? integer-set? -> boolean?
(define (within? S T)
  (or (subset? S T)
      (subset? T S)))

;; overlap? : integer-set? integer-set? -> (or/c boolean? number?)
(define (overlap? S T)
  (get-integer (intersect S T)))

;; ---------------------------------------------------------------------------------------------------

(module+ test
  (require threading)
  
  (define *eg*
    #<<END
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
END
    )

  (~>
   *eg*
   (with-input-from-string port->lines)
   (map read-line _)
   (count (curry apply within?) _)
   )
  
  )
