#lang racket

(require graph)

(module+ main
  (require threading)

  (define *input*
    (with-input-from-file "input.txt"  port->string))
  
;;   (define *input* #<<END
;; Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
;; Valve BB has flow rate=13; tunnels lead to valves CC, AA
;; Valve CC has flow rate=2; tunnels lead to valves DD, BB
;; Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
;; Valve EE has flow rate=3; tunnels lead to valves FF, DD
;; Valve FF has flow rate=0; tunnels lead to valves EE, GG
;; Valve GG has flow rate=0; tunnels lead to valves FF, HH
;; Valve HH has flow rate=22; tunnel leads to valve GG
;; Valve II has flow rate=0; tunnels lead to valves AA, JJ
;; Valve JJ has flow rate=21; tunnel leads to valve II
;; END
;;     )

  (define-values (*flows* *valves*)
    (read-graph (string-split *input* "\n")))

  (define *simplified-valves*
    (condense-graph *valves* *flows* "AA"))

  ;; Part 1

  (displayln "Part 1")

  (time
   (maximum-output *simplified-valves*
                   *flows*
                   "AA"
                   31  ;; Because we waste a minute opening "AA"
                   (remove "AA" (get-vertices *simplified-valves*))))
  
  ;; Part 2

  (displayln "Part 2")

  ;; Give some valves to me and the remainder to Nelly
  (define *splits*
    (partitions (remove "AA" (get-vertices *simplified-valves*))))
  
  (define *counter* (box 0))
  (apply max
         (map (λ (split) (maximum-output/elephant *simplified-valves*
                                                  *flows*
                                                  "AA"
                                                  27
                                                  split
                                                  *counter*))
              *splits*))

  
  )


;; ---------------------------------------------------------------------------------------------------

(define (read-node str)
  (match str
    [(regexp #rx"Valve ([A-Z][A-Z]) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z][A-Z])((, [A-Z][A-Z])*)"
                   (list _ node flow out outs _))
     (list node
           flow
           (cons out (string-split outs ", ")))]))

;; (a b) -> (b a)
(define (swap pr)
  (list (cadr pr) (car pr)))

;; [List-of? string?] -> (values hash? graph?)
(define (read-graph strs)
  (let ([nodes (map read-node strs)])
    (let ([flows
           (make-hash (map (λ (n) (cons (car n) (string->number (cadr n)))) nodes))]
          [graph
           (undirected-graph
            (remove-duplicates 
             (apply append
                    (map (λ (n) (map (curry list (car n)) (caddr n))) nodes))
             (λ (n1 n2) (or (equal? n1 n2) (equal? (swap n1) n2)))))])
      (values flows graph))))
  

;; Remove unnecessary nodes. Return a new graph where:
;; - the nodes are only those nodes in graph with non-zero flows (except keep start)
;; - the edge weights are the shortest distances
(define (condense-graph graph node-weights start)
  ;;
  (define (remove-dups assc)
    (remove-duplicates assc
                       (λ (w1 w2)
                         (or (equal? (car w1) (car w2))
                             (equal? (swap (car w1)) (car w2))))))
  ;;
  (define (remove-ids assc)
    (filter (λ (w) (not (eq? (caar w) (cadar w)))) assc))
  ;
  (define (remove-zeros! node-weights start g)
    (for ([n (in-vertices g)])
      (when (and (zero? (hash-ref node-weights n))
                 (not (equal? n start)))
        (printf "Removing ~a\n" n)
        (remove-vertex! g n))))
  ;;
  (let ([fw (hash->list (floyd-warshall graph))])
    (let ([distances (remove-dups (remove-ids fw))])
      (let ([g (weighted-graph/undirected
                (map (λ (e) (list (cdr e) (caar e) (cadar e))) distances))])
        (remove-zeros! node-weights start g)
        g))))




;; Compute the maximum output available from this node, in the time remaining
;; (not including anything opened already)
;; maximum-output : graph flows node time opened
;; valves : the (weighted!) graph
;; flows : the available flows at each valve
;; here : where I am now
;; time : turns remaining
;; closed : list of valves still closed
(define (maximum-output valves flows here turns closed)
  (if (or (< turns 2)
          (null? closed))
      0
      (let ([to-try (remove here closed)])
        (+ (* (hash-ref flows here) (- turns 1))
           (apply max
                  (for/list ([next closed])
                    (maximum-output valves
                                    flows
                                    next
                                    (- turns 1 (edge-weight valves here next))
                                    to-try)))))))


(define (partitions xs)
  ;; pss is a list of pairs of lists
  (define (add-part x pss)
    (append
     (map (λ (pr) `(,(cons x (car pr)) . ,(cdr pr))) pss)
     (map (λ (pr) `(,(car pr) . ,(cons x (cdr pr)))) pss)))
  (for/fold ([parts '((() . ()))])
            ([x xs])
    (add-part x parts)))

;; Split is a pair of lists of valves
(define (maximum-output/elephant valves flows here turns split counter)
  (let ([count (unbox counter)])
    (when (zero? (modulo count 300)) (display ".") (flush-output))
    (when (zero? (modulo count 3000)) (display "|"))
    (set-box! counter (+ count 1)))
  (+ (maximum-output valves flows here turns (car split))
     (maximum-output valves flows here turns (cdr split))))
