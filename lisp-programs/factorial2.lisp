; Recursive factorial function
(defun factor1(n)
	(if (= n 1)
		1
		(* n (factor1 (- n 1)))
	)
)

; Factorial function using looping and a global list
(defun factor4(n)
	(setq rangelist (loop :for r :from 2 to n :collect r))
	(setq factorlist (list 1))
	(loop for x in rangelist
		do (setq factorlist 
			(append
				(list (* (car factorlist) x))
				factorlist
			)
		)
	)
	(car factorlist)
)

; Factorial using the multiplication operator on an entire list
; Does not work on n >= 10000
(defun factor5(n)
	(apply '* (loop :for r :from 2 to n :collect r))
)

; Find number of digits in a positive integer
(defun count-digit(n)
	(if (< n 1)
		0
		(+ 1 (count-digit (/ n 10)))
	)
)