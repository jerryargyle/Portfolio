#lang s-exp "minischeme.rkt"

(define-syntax let
  (syntax-rules ()
    [(_ ([v e] ...) body ...)
     ((lambda (v ...) body ...) e ...)]))

(define-syntax let*
  (syntax-rules ()
    [(_ ([v1 e1] [v e] ...) body ...)
     (let ([v1 e1])
       (let* ([v e] ...) body ...))]
    [(let* () body ...)
     (let () body ...)]))

(define-syntax begin
  (syntax-rules ()
    [(_ e)
     e]
    [(_ e1 e* ...)
     (let ([t e1])
       (begin e* ...))]))

; And

; Implement short-circuiting `and` in terms of if.
; 1pt extra credit for supporting arbitrarily many arguments!

(define-syntax and
  (syntax-rules ()
    [(_ a b)
     (if a
         b
         #f)]))

; While loops and letrec

; implement `while` and `letrec`.
(define-syntax while
  (syntax-rules ()
    [(_ c
        body ...)
     (letrec ([v (lambda ()
                   (if c
                       (begin
                         body ...
                         (v) )
                       (void) )
                   )])
       (v) )]))
  
(define-syntax letrec
  (syntax-rules ()
    [(_([v e] ...)
     body)
     (let ([v #%undefined] ...)
       (begin
         (set! v e ) ...
         body)
       )]
    ))


; I would like to write this while loop:
#;(let ([x 5])
    (while (> x 0)
           (displayln x)
           (set! x (- x 1))))

; Which would expand to this use of letrec:
#;(let ([x 5])
    (letrec ([f (lambda ()
                  (if (> x 0)
                      (begin
                        (displayln x)
                        (set! x (- x 1))
                        (f))
                      (void)))])
      (f) ))

; Which finally expands to:
#;(let ([x 5])
  (let ([f #%undefined])
    (begin
      (set! f (lambda ()
                (if (> x 0)
                    (begin
                      (displayln x)
                      (set! x (- x 1))
                      (f))
                    (void))))
      (f))))


; Here's another use of letrec that your macro should support:
#;(letrec ([even?
           (lambda (n)
             (if (equal? 0 n)
               #t
               (odd? (- n 1))))]
         [odd?
           (lambda (n)
             (if (equal? 0 n)
               #f
               (even? (- n 1))))])
  (even? 10))


; Cond

; implement a macro for `cond`

; When I have multiple conditions, it would be nicer to not have to
; write deeply nested `if`s. Scheme provides `cond` for this purpose:

(define x 5)

; I would like to write:

(cond
  [(< x 5) 'a]
  [(> x 5) 'b]
  [else 'c])

; Which should expand to:
#;(if (< x 5) 'a
  (if (> x 5) 'b
    x))

; If no `else` clause is provided and none of the conditions match, the
; cond expression should return (void)


(define-syntax else
  (syntax-rules ()))

(define-syntax cond
  (syntax-rules (else)
  [(_ [else body])
   body]
   [(_ [c1 v1] [c v] ...)
    (if c1
        v1
        (cond [c v] ... ))]
    [(_ )
     (void)]
    ))

   ;else case
   ;general case of 1 or more
   ;void case

; Classes

; implement `class` and `send`
(define-syntax class
  (syntax-rules ()
    [(_ (val ...) (method (name arg ...) body) ... )
     (lambda (val ...)
       (lambda (msg)
         (let ([msgname (car msg)])
           (cond
             [(equal? msgname 'name)
              (helperMacro (cdr msg) body (arg ...))
              ] ...
              [else (error 'class "no such method")]
             )
         )))]
    ))

(define-syntax helperMacro
  (syntax-rules ()
    [(_ cmsg body ())
     body]
    [(_ cmsg body (arg args ...))
     (let ([arg (car cmsg)])
       (helperMacro (cdr cmsg) body (args ...))
       )]
    ))

(define-syntax send
  (syntax-rules ()
    [(_ name (method args ...))
     (name (list 'method args ...))]
    ))

; I would like to write:
(define counter%
  (class (val)
    (method (inc)
      (set! val (+ 1 val)))
    (method (get)
      val)))

(define c (counter% 5))
(send c (get))
(send c (inc))
(send c (get))

; And have it desugar to this:
#;(define counter%
  (lambda (val)
    (lambda (msg)
      (let ([msgname (car msg)])
        (cond
          [(equal? msgname 'inc)
           (set! val (+ 1 val))]
          [(equal? msgname 'get)
           val]
          [else (error 'class "no such method")])))))

;(define o (counter% 5))
;(o '(get))
;(o '(inc))
;(o '(get))

; I would like to write:
(define point%
  (class (x y)
    (method (getx) x)
    (method (gety) y)
    (method (distance other)
      (sqrt
       (+ (expt (- (send other (getx)) x) 2)
          (expt (- (send other (gety)) y) 2))))))

(send (point% 1 2) (distance (point% 2 3)))

; And have it desugar to this:(define point%
#;(lambda (x y)
   (lambda (msg)
      (let ([msgname (car msg)])
        (cond
          [(equal? msgname 'getx)
           x]
          [(equal? msgname 'gety)
           y]
          [(equal? msgname 'distance)
           (let ([other (car (cdr msg))])
             (sqrt
              (+ (expt (- (other (list 'getx)) x) 2)
                 (expt (- (other (list 'gety)) y) 2))))]))))

;((point% 1 2) (list 'distance (point% 2 3)))

