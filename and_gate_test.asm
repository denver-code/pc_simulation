; Example program demonstrating the AND logic gate

; Initialize RAM with two binary values
INIT [0x00] = 0b11001100  ; Set RAM[0x00] to 11001100
INIT [0x01] = 0b10101010  ; Set RAM[0x01] to 10101010

; Load values from RAM into registers
LOAD R0, [0x00]           ; Load RAM[0x00] into R0
LOAD R1, [0x01]           ; Load RAM[0x01] into R1

; Perform AND operation
AND R0, R1, R2            ; R2 = R0 AND R1
OUT R2                    ; Output result of AND operation

; Cleanup: Clear RAM values used
CLEAR [0x00]              ; Clear RAM at address 0x00
CLEAR [0x01]              ; Clear RAM at address 0x01

HALT                       ; Stop execution
