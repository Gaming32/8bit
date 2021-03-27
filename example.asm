.offset $8000

init:
    lda #$80

loop:
    sti $01 #%01 ; set mode to print number
    sta $00      ; print the value of the X register
    sti $01 #%00 ; set mode to print ascii
    sti $00 '\n' ; print a newline
    sbi #$01
    ; jmp loop

finish:
    end

.truncate
