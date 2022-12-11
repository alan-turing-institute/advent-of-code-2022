#lang racket/base

(require racket/match)


;; ---------------------------------------------------------------------------------------------------
;; Quick imperative queues

(provide (struct-out queue)
         queue-empty?  
         empty-queue
         push!
         pop!
         list->queue   ; Initialise a queue from a list
         queue->list)

;; Items are pushed on the tail and popped off the head
(struct queue (head tail) #:mutable #:transparent)

(define (empty-queue)
  (let ([eq (queue #f '())])
    (set-queue-head! eq (queue-tail eq))
    eq))

(define (queue-empty? q)
  (null? (queue-head q)))

;; Push v on the tail of q
(define (push! q v)
  (match-let ([(struct queue (head tail)) q])
    (if (null? tail)
        (begin
          (set-queue-tail! q (mcons v '()))
          (set-queue-head! q (queue-tail q)))
        (begin
          (set-mcdr! tail (mcons v null))
          (set-queue-tail! q (mcdr tail))))))

;; pop : queue? -> values any/c queue?
;; Pop a value from the head
(define (pop! q)
  (match-let ([(struct queue (head tail)) q]) 
    (let ([v (mcar head)]
          [r (mcdr head)])
      (set-queue-head! q r)
      (when (null? r)
          (set-queue-tail! q r))
      v)))

(define (list->queue xs)
  (let ([q (empty-queue)])
    (for ([x (in-list xs)])
      (push! q x))
    q))

(define (queue->list q)
  (for/list ([x (queue-head q)])
    x))




