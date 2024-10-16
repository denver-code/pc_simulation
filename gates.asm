; Example usage of logic gates

; Initialize registers with some values
INIT [0x00] = 0b11001100  ; Set RAM[0x00] to 11001100 (binary)
INIT [0x01] = 0b10101010  ; Set RAM[0x01] to 10101010 (binary)

; Load values from RAM into registers
LOAD R0, [0x00]           ; Load RAM[0x00] into R0
LOAD R1, [0x01]           ; Load RAM[0x01] into R1

; Perform AND operation
AND R0, R1, R2            ; R2 = R0 AND R1
OUT R2                    ; Output result of AND operation

; Perform OR operation
OR R0, R1, R3             ; R3 = R0 OR R1
OUT R3                    ; Output result of OR operation

; Perform NOT operation on R0
NOT R0, R4                ; R4 = NOT R0
OUT R4                    ; Output result of NOT operation

; Perform NAND operation
NAND R0, R1, R5           ; R5 = R0 NAND R1
OUT R5                    ; Output result of NAND operation

; Perform NOR operation
NOR R0, R1, R6            ; R6 = R0 NOR R1
OUT R6                    ; Output result of NOR operation

; Perform XOR operation
XOR R0, R1, R7            ; R7 = R0 XOR R1
OUT R7                    ; Output result of XOR operation
