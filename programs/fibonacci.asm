; FIBONACCI EXAMPLE
fibonacci::
    mov 10000, $r3
    mov 0, $r1
    mov 1, $r2
start: out $r2, 1
    slt $r3, $r2, $r4
    br $r4, stop
    add $r1, $r2, $r5
    mov $r2, $r1
    mov $r5, $r2
    jmp start
stop: out $r0, 0
    jmp fibonacci
