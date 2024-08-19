// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/7/StackArithmetic/SimpleAdd/SimpleAdd.vm

// Pushes and adds two constants.

// this is how translated asm file should look like
// initializes the value of RAM[0] = 256
// @256
// D=A
// @SP
// M=D

push constant 7
// @7
// D=A

// @SP
// A=M
// M=D

// @SP
// M=M+1

push constant 8
// @8
// D=A

// @SP
// A=M
// M=D

// @SP
// M=M+1

add
// @SP
// M=M-1

// @SP
// A=M
// D=M // D=8

// @SP
// M=M-1

// @SP
// A=M
// // M=7
// M=D+M

// @SP
// M=M+1

// (END)
//   @END
//   0;JMP
