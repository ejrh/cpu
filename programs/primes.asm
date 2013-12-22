; PRIMES EXAMPLE
primes::
    mov 1, $r1                    ; Increment value
    mov 100, $r3                  ; Maximum number to search up to
    mov 0, $r4                    ; Start of primes array
    mov 0, $r5                    ; End of primes array (exclusive)
    mov 2, $r2                    ; First prime

found_prime: out $r2, 1           ; Print
    store $r2, $r5, 0             ; Append to array
    add $r1, $r5, $r5
    
next_candidate: add $r1, $r2, $r2 ; New candidate to check
    
    slt $r3, $r2, $r6             ; Check if reached maximum number
    br $r6, stop
    
    mov $r4, $r7                  ; Start at start of primes array
check_prime: load $r7, 0, $r8     ; Load the prime
    mov 0, $r9
    
next_multiple: add $r8, $r9, $r9
    slt $r2, $r9, $r6             ; Check if past candidate
    br $r6, next_prime            ; If so, move on to the next prime divisor
    sub $r2, $r9, $r6             ; Check if multiple is equal to candidate
    br $r6, next_multiple         ; If not, move on to the next multiple
    jmp next_candidate            ; Otherwise, move on to the next candidate
    
next_prime: add $r1, $r7, $r7     ; Next prime
    slt $r7, $r5, $r6
    br $r6, check_prime
    
    jmp found_prime               ; No divisors found

stop: out $r0, 0
    jmp primes
