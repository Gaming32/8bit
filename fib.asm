.offset $8000

FIRST_VALUE = #0  ; First Fibonacci number
SECOND_VALUE = #1 ; Second Fibonacci number

init:
    ldx FIRST_VALUE
    ldy SECOND_VALUE

print:
    sti $01 #%01 ; set mode to print number
    stx $00      ; print the value of the X register
    sti $01 #%00 ; set mode to print ascii
    sti $00 '\n' ; print a newline

calculate:
    stx $02
    sty $03
    ldx $03
    lda $02
    add $03
    sta $02
    ldy $02

loop:
    jmp print

.truncate
