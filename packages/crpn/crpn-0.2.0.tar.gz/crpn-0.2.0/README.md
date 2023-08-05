# crpn - A simple command-line calculator

This is a simple [reverse polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
(RPN) calculator for use in a command-line terminal.

It's essentially a ground-up rewrite of my desktop calculator,
[NeRPN](https://github.com/Abstrys/NeRPN), which is still a neat example of a Swing Java application
and works well enough if you're looking for a graphical (but minimal) RPN calculator.

This version is written in pure Python and should run just about anywhere. It can be used over SSH
in a pure terminal environment, and of course, will use the colors and fonts you have set in your
terminal.

1. [Installing it](#installing-it)
1. [Using it](#using-it)
1. [Other things to try](#other-things-to-try)
1. [List of operations](#list-of-operations)
1. [License](#license)

## Installing it

As a user, the easiest way is to install is from pypi:

    pip install crpn

Alternatively, to install from the [downloaded repo](https://github.com/Abstrys/crpn/archive/main.zip),
use the included `Makefile`:

    make install


## Using it

1. Run it by typing **`crpn`** at the command-prompt. It will provide a few instructions and show
   you the stack, which will initially be empty:

        ===================================================
        crpn v.0.2.0 - a minimalist command-line calculator
        ===================================================
        
        Enter values on the stack, or the name of an operation or command.
        
        Type 'quit' or 'exit' to quit.  Type 'help' for help.
        
        Current stack:
        ------------------------
        ------------------------
        > 

1. Type values (either integer or floating-point) and press **Enter** to add them to the stack.

        > 10
        ------------------------
         0:   10
        ------------------------
        > 2
        ------------------------
         1:   10
         0:   2
        ------------------------

1. Type operations (`+`, `-`, `*`, `/`, `!`, `^`, `cos`, `abs`, etc.) to operate on stack members
   and see the results of the calculation.

        > ^
        ------------------------
         0:   100
        ------------------------

1. Type `quit` or `exit` to save the stack and quit.


## Other things to try

* Type `help commands` or `help operations` for a list of all current operations.

* Type `help` or `help <op_name>` to get general help or help for a specific operation at any time.

* Press **Enter** without entering a value to duplicate the final row on the stack.

* Type `del` or `del <n>` to delete stack row(s), or `clear` to clear the stack

* You can combine operations with `&&`. For example, to clear the stack and then quit, type:

        > clear && quit


## List of operations

(generated using `help operations`)

* 'abs' - Compute the absolute value of row 0.
* 'acos' - Compute the arccosine of row 0.
* 'add' - Add rows 0 and 1 together.
* 'asin' - Compute the arcsine of row 0.
* 'atan' - Compute the arctangent of row 0.
* 'cbrt' - Compute the cube root of row 0.
* 'ceil' - Compute the ceiling (next higher whole number) for row 0.
* 'clear' - Clear the stack.
* 'cos' - Compute the cosine of row 0.
* 'cosh' - Compute the hyperbolic cosine of row 0.
* 'deg' - Converts the radian value on row 0 to degrees
* 'del' - Delete row 0, or the row specified by the optional argument.
* 'div' - Divide row 1 by row 0.
* 'dup' - Duplicate row 0 and add it to the stack.
* 'e' - Raise the constant 'e' to the power of the value on row 0.
* 'en1' - Raise the constant 'e' to the power of 1/value on row 0.
* 'eng' - Display results in engineering notation.
* 'exp' - Raise 10 to the power of the value on row 0.
* 'expn1' - Raise 10 to the power of 1/value on row 0.
* 'fact' - Compute the factorial of row 0.
* 'fix' - Display results in fixed-point notation.
* 'floor' - Compute the floor (next lower whole number) for row 0.
* 'help' - Print general help, or for a given operation.
* 'hyp' - Computes the hypoteneuse (sqrt(x2 + y2)) of rows 0 and 1.
* 'inv' - Computes the inverse (1/x) of row 0.
* 'ln' - Computes the natural (e-based) log of row 0.
* 'log' - Computes the 10-based log of row 0.
* 'max' - Computes the max between row 0 and 1, or between the number of rows specified in the optional argument.
* 'min' - Computes the min between row 0 and 1, or between the number of rows specified in the optional argument.
* 'mult' - Multiply rows 0 and 1.
* 'neg' - Negate row 0.
* 'pow' - Raise row 1 to the power of row 2.
* 'quit' - Save the current state and quit.
* 'rad' - Convert the value of row 0 (in degrees) to radians.
* 'rand' - Add a random fractional value to the stack.
* 'root' - Computes the x root of y for rows 0 and 1.
* 'rot' - Rotates rows 0-2, or the number of rows specified in the optional argument.
* 'sci' - Display results in scientific notation.
* 'sin' - Compute the sine of row 0.
* 'sinh' - Compute the hyperbolic sine of row 0.
* 'sqrt' - Compute the square root of row 0.
* 'std' - Display results in standard notation.
* 'subt' - Subtract row 0 from row 1.
* 'sum' - Sum all rows, or a given number of them, together.
* 'swap' - Swap rows 0 and 1, or row 0 with the one provided in the optional parameter.
* 'tan' - Compute the tangent of row 0.
* 'tanh' - Compute the hyperbolic tangent of row 0.

To get built-in help for any of these operations, type `help <op_name>`.


## License

This code is provided under the MIT license. You are free to use it for any purpose, but I assume no
liability and offer no warranty. See the
[LICENSE](https://github.com/Abstrys/crpn/blob/main/LICENSE) file for full details.

