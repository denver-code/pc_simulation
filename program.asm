; Example program
INIT [0x08] = 0b00000101   ; Initialize memory at address 0x08 with binary 5
INIT [0x10] = 0b00001010   ; Initialize memory at address 0x10 with binary 10
INIT [0x1F] = 0b00001010

LOAD R1, [0x08]            ; Load value from address 0x08 into register R1
LOAD R2, [0x10]            ; Load value from address 0x10 into register R2
ADD R1, R2, R3             ; Add R1 and R2, store result in R3

STORE R3, [0x20]           ; Store the result in memory address 0x20

OUT R3                     ; Display the register R3

CLEAR [0x20]               ; Clear the value in memory address 0x20
CLEAR [0x08]               ; Clear the value in memory address 0x08
CLEAR [0x10]               ; Clear the value in memory address 0x10

HALT                       ; Stop execution
