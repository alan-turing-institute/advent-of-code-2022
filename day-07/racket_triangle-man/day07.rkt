#lang racket

(module+ main
  (require threading)

  (define root-dir
    (~> (with-input-from-file "input.txt" port->lines)
        (map tokenise _)
        parse-dir
        result-val
        car))

  ;; Part 1

  (define dir-sizes (fs-dir-sizes root-dir))
  
  (~>> dir-sizes
       flatten
       (filter (λ (v) (<= v 100000)))
       (apply +))

  ;; Part 2

  (define *unused* (- 70000000 (car dir-sizes)))
  (define *required* (- 30000000 *unused*))

  (~>> dir-sizes
       flatten
       (filter (λ (v) (>= v *required*)))
       (apply min))
  
  )

;; ---------------------------------------------------------------------------------------------------

;; Lexical analysis

(struct token () #:transparent)
(struct token-$up  token () #:transparent)      ; neaning "$ cd .."
(struct token-$cd  token (where) #:transparent) ; `where` is a string
(struct token-$ls  token () #:transparent)
(struct token-file token (name size) #:transparent)
(struct token-dir  token (name) #:transparent)

(define (tokenise line)
  (match line
    ["$ ls" (token-$ls)]
    ["$ cd .." (token-$up)]
    [(regexp #rx"\\$ cd (.+)" (list _ where))
     (token-$cd where)]
    [(regexp #rx"([0-9]+) (.+)" (list _ size name))
     (token-file name (string->number size))]
    [(regexp #rx"dir (.+)" (list _ name))
     (token-dir name)]))

;; Parsing

;; A filesystem is a directory or a file
(struct fs () #:transparent)
(struct fs-dir  fs (name contents) #:transparent) ; A directory
(struct fs-file fs (name size) #:transparent)     ; A file

;; A parse result is either a result or #f
;; A result is the resulting filesystem, together with the remaining tokens
(struct result (val toks) #:transparent)

;; A parser for things
;; is a function from strings
;; to lists of pairs
;; of things and strings
;; -- Fritz Ruehr

;; Although in this case the list is always of length 1.

(define ((parser/literal tok) toks)
  (match toks
    [(cons tok rest) (result #f rest)]
    [_ #f]))

(define (parse-success toks)
  (result #f toks))

(define (parse-done toks)
  (if (null? toks)
      (result #f toks)
      #f))

;; A result value is either #f or a list of things
(define (combine val1 val2)
  (if (not val1)
      val2
      (if (not val2)
          val1
          (append val1 val2))))

(define ((parser/seq p1 p2) toks)
  (let ([res1 (p1 toks)])
    (and res1
         (let ([res2 (p2 (result-toks res1))])
           (and res2
                (let ([val1 (result-val res1)]
                      [val2 (result-val res2)])
                  (result (combine val1 val2) (result-toks res2))))))))

(define ((parser/alt p1 p2) toks)
  (or (p1 toks)
      (p2 toks)))

(define (parser/* p)
  (parser/alt
   (parser/seq p (λ (toks) ((parser/* p) toks)))
   parse-success))


;; ---------------------------------------------------------------------------------------------------
;; Parse the filesystem traversal

(define (parse-dirname toks)
  (match toks
    [(cons (token-dir name) rest) (result #f rest)]
    [_ #f]))

(define (parse-file toks)
  (match toks
    ['() #f]
    [(cons (token-file name size) rest)
     (result (list (fs-file name size)) rest)]
    [_ #f]))

(define (parse-dir toks)
  (match toks
    [(list (token-$cd dirname) (token-$ls) rest ...)
     (let ([contents ((parser/seq
                       (parser/*
                        (parser/alt
                         (parser/alt parse-file parse-dir)
                         parse-dirname))
                       (parser/alt (parser/literal (token-$up))
                                   parse-done))
                      rest)])
       (result (list (fs-dir dirname (result-val contents))) (result-toks contents)))]
    [_ #f]))

;; ---------------------------------------------------------------------------------------------------

;; Walk the directory tree

;; fs-dir-sizes : fs-dir? -> ...
;; Return a pair, consisting of the size of this directory, and a list of the
;; pairs representing sub-directories 
(define (fs-dir-sizes dir)
  (for/fold ([total-size 0]
             [dirs       '()]
             #:result (cons total-size dirs))
            ([node (fs-dir-contents dir)])
    (match node
      [(fs-file _ size)
       (values (+ total-size size) dirs) ]
      [(fs-dir _ _)
       (let ([subdirs (fs-dir-sizes node)])
         (values (+ total-size (car subdirs)) (cons subdirs dirs)))])))

;; ---------------------------------------------------------------------------------------------------

(module+ test
  (require threading)
  
  (define *eg* #<<END
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
END
    )

  (define root-dir
    (~> (string-split *eg* "\n")
        (map tokenise _)
        parse-dir
        result-val
        car))
  
  (~>> (fs-dir-sizes root-dir)
       flatten
       (filter (λ (v) (<= v 100000)))
       (apply +))

  )


