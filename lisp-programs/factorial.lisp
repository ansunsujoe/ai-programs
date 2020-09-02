; Factorial with simple recursion
(defun factor1 (n)
    (if (= n 0)
        1
        (* n (factor1 (- n 1)))
    )
)

; Test the factorial function
(defun testFactorial()
    (loop for i from 0 to 16
        do (format t "~D! = ~D~%" i (factorial1 i))
    )
)

; Factorial with tail recursion
(defun factor2 (n)
    (factorial-helper n 1)
)

; Helper function for tail recursion
; Variable a is the accumulator
(defun factorial-helper (n a)
    (if (= n 1)
        a
        (factorial-helper (- n 1) (* n a))
    )
)

; Factorial with looping
(defun factor3 (n)
    (loop for i from 1 to n
        for answer = 1 then (* answer i)
        finally (return answer)
    )
)