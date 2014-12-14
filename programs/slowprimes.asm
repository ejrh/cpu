; SLOW PRIMES EXAMPLE
primes::
    mov 1, $r1                    ; Increment value
    mov 10000, $r3                ; Maximum number to search up to
    mov 1, $r2                    ; Number just before first candidate to check
    mov 16, $r10                  ; Offset of IO ports

new_candidate: add $r1, $r2, $r2             
    slt $r3, $r2, $r6  ; Check if reached maximum number
    br $r6, stop
    
    mov 2, $r8                    ; Start at first divisor, 2
check_divisor: mov 0, $r9
    
    ;out $r8, 3
next_multiple: add $r8, $r9, $r9
    ;out $r9, 4
    slt $r2, $r9, $r6             ; Check if past candidate
    br $r6, next_divisor          ; If so, move on to the next prime divisor
    sub $r2, $r9, $r6             ; Check if multiple is equal to candidate
    br $r6, next_multiple         ; If not, move on to the next multiple
    ;out $r2, 2
    jmp new_candidate             ; Otherwise, move on to the next candidate
    
next_divisor: add $r1, $r8, $r8   ; Next divisor
    slt $r8, $r2, $r6
    br $r6, check_divisor
    
    out $r2, $r10, 2              ; Print
    jmp new_candidate             ; No divisors found

stop: out $r0, 0
    jmp primes
