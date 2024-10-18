; Simple program to test different conditions
INIT [0x08] = 0b00000110   ; Initialize memory at address 0x08 with binary 6
INIT [0x10] = 0b00000100   ; Initialize memory at address 0x10 with binary 4

LOAD R1, [0x08]            ; Load value from address 0x08 into register R1 (6)
LOAD R2, [0x10]            ; Load value from address 0x10 into register R2 (4)

; Test IF R1 > R2 THEN ADD R1, R2 to R3
IF R1 > R2 THEN ADD R1, R2, R3    ; If R1 > R2, R3 = R1 + R2
OUT R3                     ; Output the result in R3

; Test IF R1 < R2 THEN ADD R2, R1, R4
IF R1 < R2 THEN ADD R2, R1, R4    ; If R1 < R2, R4 = R2 + R1
OUT R4                     ; Output the result in R4

; Test IF R1 >= R2 THEN ADD R1, R1, R5
IF R1 >= R2 THEN ADD R1, R1, R5   ; If R1 >= R2, R5 = R1 + R1
OUT R5                     ; Output the result in R5

; Test IF R1 <= R2 THEN ADD R2, R2, R6
IF R1 <= R2 THEN ADD R2, R2, R6   ; If R1 <= R2, R6 = R2 + R2
OUT R6                     ; Output the result in R6

HALT                       ; Stop execution
