; SIMPLE MEMORY EXAMPLE
simple_mem::
    mov 1, $r4
    mov 10, $r3 ; Test first 10 words

    mov 0, $r1
store_loop:
    out $r1, 1
    store $r1, $r1, 0   ; Store $r1 into mem[$r1]
    add $r1, $r4, $r1
    slt $r1, $r3, $r2
    br $r2, store_loop  ; If $r1 < $r3, keep going

    mov 0, $r1
load_loop:
    load $r1, 0, $r5    ; Load $r5 from mem[$r1]
    out $r5, 1
    add $r1, $r4, $r1
    slt $r1, $r3, $r2
    br $r2, load_loop  ; If $r1 < $r3, keep going
    out $r0, 0
