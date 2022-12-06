#lang racket

;; ---------------------------------------------------------------------------------------------------
;; Quick functional queues

(module queue racket

  (provide queue
           queue-empty?  
           empty-queue
           enqueue
           dequeue
           list->queue   ; Initialise a queue from a list
           queue->unordered-list)
  
  ;; Items are pushed on the head and popped off the tail.
  ;; When the tail is empty, the head is reversed, and the head and tail swapped
  
  (struct queue (head tail) #:transparent)

  (define empty-queue (queue '() '()))
  (define (queue-empty? q)
    (and (null? (queue-tail q))
         (null? (queue-head q))))

  ;; Push v on q
  (define (enqueue v q)
    (struct-copy queue q
                 [head (cons v (queue-head q))]))

  ;; dequeue : queue? -> values any/c queue?
  ;; Get a value from the tail
  (define/match (dequeue q)
    [((struct queue (head tail))) 
     (if (null? tail)
         (let ([tl (reverse head)])
           (values (car tl) (queue '() (cdr tl))))
         (values (car tail) (queue head (cdr tail))))])

  (define (list->queue xs)
    (queue '() xs))

  (define (queue->unordered-list q)
    (for/fold ([xs (queue-tail q)])
              ([x (queue-head q)])
      (cons x xs)))
  
  )

;; ---------------------------------------------------------------------------------------------------

(require 'queue)

(module+ test
  (define *eg* "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
  
  ;; Part 1 example
  (first-when-unique (string->list *eg*) 4)

  )

(module+ main
  (define *input* (with-input-from-file "input.txt" port->string))
  
  ;; Part 1
  (first-when-unique (string->list *input*) 4)

  ;; Part 2
  (first-when-unique (string->list *input*) 14)

  )

;; Find the index of the first N unique values in xs
(define (first-when-unique xs N)
  (for/fold ([q (list->queue (take xs N))]
             [idx N]
             #:result idx)
            ([x (drop xs N)])
    #:break (not (check-duplicates (queue->unordered-list q)))
    (let-values ([(vv qq) (dequeue (enqueue x q))])
      (values qq (add1 idx)))))



