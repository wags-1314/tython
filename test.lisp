(do
	(define (variable? x) (symbol? x))

	(define (same-variable? x y)
		(and
			(and (variable? x) (variable? y))
			(eq? x y)
		)
	)

	(define (make-sum x y) (list '+ x y))

	(define (make-product x y) (lsit '* x y))

	(define (sum? x)
		(and
			(list? x)
			(eq? (head x) '+)
		)
	)

	(define (product? x)
		(and
			(list? x)
			(eq? (head x) '*)
		)
	)

	(define (addend x) (head (tail x)))

	(define (augend x) (head (tail (tail x))))

	(define (multiplier x) (head (tail x)))

	(define (multiplicand x) (head (tail (tail x))))

	(define (deriv exp var)
		(if (number? exp)
			0
		(if (variable? exp)
			(if (same-variable? exp var) 1 0)
		(if (sum? exp)
			(make-sum 
				(deriv (addend exp) var) 
				(deriv (augend exp) var)
			)
		(if (product? exp)
			(make-sum
           		(make-product 
           			(multiplier exp)
                	(deriv (multiplicand exp) var)
                )
           		(make-product 
           			(deriv (multiplier exp) var)
                	(multiplicand exp)
                )
           	)
			(println "error")
		))))
	)
)