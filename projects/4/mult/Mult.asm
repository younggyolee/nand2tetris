// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

// R0 = RAM[0]
@0
D=M
@R0
M=D

// R1 = RAM[1]
@1
D=M
@R1
M=D

// multiplication

// i=0
@0
D=A
@i
M=D

// R2 = 0
@0
D=A
@R2
M=D

// while i < R1 - 1, R2 = R2 + R0
(LOOP)
  // if i == R1, goto END
  @i
  D=M
  @R1
  D=D-M
  @END
  D;JEQ

  // R2 = R2 + R0
  @0
  D=M
  @2
  M=M+D

  // i = i + 1
  @i
  M=M+1

  // goto LOOP
  @LOOP
  0;JMP

(END)
  @END
  0;JMP
