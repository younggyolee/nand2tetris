// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(LOOP)
  // declare variable i
  @i
  M=0
  // checks keyboard input
  // if any, paint black
  // else, paint white
  @KBD
  D=M
  @BLACK
  D;JGT
  @WHITE
  D;JEQ

  (BLACK)
    // break if i == 8192
    @i
    D=M
    @8192
    D=D-A
    @LOOP
    D;JEQ

    // draw into a cell
    @i
    D=M
    @SCREEN
    A=A+D
    M=-1

    // i = i + 1
    @i
    M=M+1

    @BLACK
    0;JMP

  (WHITE)
    // break if i == 8192
    @i
    D=M
    @8192
    D=D-A
    @LOOP
    D;JEQ

    // draw into a cell
    @i
    D=M
    @SCREEN
    A=A+D
    M=0

    // i = i + 1
    @i
    M=M+1

    @WHITE
    0;JMP
