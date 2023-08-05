#!/usr/bin/env python
# crpn - a minimalist command-line calculator
#
# Copyright © 2020, Eron Hennessey
#
# This code is provided under the terms of the MIT open source license. See the LICENSE file
# included with this repository for # details.

import sys, os
import math, random
import json
from pathlib import Path
import decimal

SAVEFILE = '.crpn-state.json'

ID_TEXT = """
==================================================
crpn v0.2.0 - a minimalist command-line calculator
==================================================
"""

HELP_TEXT = """
Enter values on the stack, or the name of an operation or command.

Type 'quit' or 'exit' to quit.  Type 'help' for help.
"""

EXTRA_HELP = """
Also try:

    help <operation_name>

for operation-specific help. For a list of the available operations, type:

    help operations
"""

CONST_MAP = {
    "E": decimal.Decimal(math.e),
    "PI": decimal.Decimal(math.pi),
    "TAU": decimal.Decimal(math.tau),
}

OP_METHOD_MAP = {
    "!": "fact",
    "": "dup",
    "%": "mod",
    "*": "mult",
    "+": "add",
    "-": "subt",
    "/": "div",
    "^": "pow",
    "abs": "abs",
    "acos": "acos",
    "add": "add",
    "asin": "asin",
    "atan": "atan",
    "cbrt": "cbrt",
    "ceil": "ceil",
    "clear": "clear",
    "cos": "cos",
    "cosh": "cosh",
    "deg": "deg",
    "del": "delete",
    "div": "div",
    "dup": "dup",
    "e": "e",
    "en1": "en1",
    "eng": "eng",
    "exit": "quit",
    "exp": "exp",
    "expn1": "expn1",
    "fact": "fact",
    "fix": "fix",
    "floor": "floor",
    "help": "help",
    "hyp": "hyp",
    "inv": "inv",
    "ln": "ln",
    "log": "log",
    "max": "max",
    "min": "min",
    "mult": "mult",
    "neg": "neg",
    "pow": "pow",
    "q": "quit",
    "quit": "quit",
    "rad": "rad",
    "rand": "rand",
    "root": "root",
    "rot": "rot",
    "sci": "sci",
    "sin": "sin",
    "sinh": "sinh",
    "sqrt": "sqrt",
    "std": "std",
    "subt": "subt",
    "sum": "sum",
    "swap": "swap",
    "tan": "tan",
    "tanh": "tanh",
}

OP_HELP = {
    "abs": {
        "desc": "Compute the absolute value of row 0.",
        "min_stack": 1
    },
    "acos": {
        "desc":  "Compute the arccosine of row 0.",
        "min_stack": 1
    },
    "add": {
        "desc": "Add rows 0 and 1 together.",
        "min_stack": 1
    },
    "asin": {
        "desc":  "Compute the arcsine of row 0.",
        "min_stack": 1
    },
    "atan": {
        "desc":  "Compute the arctangent of row 0.",
        "min_stack": 1
    },
    "cbrt": {
        "desc":  "Compute the cube root of row 0.",
        "min_stack": 1
    },
    "ceil": {
        "desc":  "Compute the ceiling (next higher whole number) for row 0.",
        "min_stack": 1
    },
    "clear": {
        "desc":  "Clear the stack.",
        "min_stack": 0
    },
    "cos": {
        "desc":  "Compute the cosine of row 0.",
        "min_stack": 1
    },
    "cosh": {
        "desc":  "Compute the hyperbolic cosine of row 0.",
        "min_stack": 1
    },
    "deg": {
        "desc":  "Converts the radian value on row 0 to degrees",
        "min_stack": 1
    },
    "del": {
        "desc":  "Delete row 0, or the row specified by the optional argument.",
        "min_stack": 1,
        "opt_args": "1: the stack row to delete."
    },
    "div": {
        "desc":  "Divide row 1 by row 0.",
        "min_stack": 2
    },
    "dup": {
        "desc":  "Duplicate row 0 and add it to the stack.",
        "min_stack": 1
    },
    "e":  {
        "desc": "Raise the constant 'e' to the power of the value on row 0.",
        "min_stack": 1
    },
    "en1":  {
        "desc": "Raise the constant 'e' to the power of 1/value on row 0.",
        "min_stack": 1
    },
    "eng":  {
        "desc": "Display results in engineering notation.",
        "min_stack": 0
    },
    "exp": {
        "desc": "Raise 10 to the power of the value on row 0.",
        "min_stack": 1
    },
    "expn1": {
        "desc": "Raise 10 to the power of 1/value on row 0.",
        "min_stack": 1
    },
    "fact": {
        "desc": "Compute the factorial of row 0.",
        "min_stack": 1,
        "req_type": "integer"
    },
    "fix": {
        "desc": "Display results in fixed-point notation.",
        "min_stack": 0
    },
    "floor": {
        "desc": "Compute the floor (next lower whole number) for row 0.",
        "min_stack": 1
    },
    "help": {
        "desc": "Print general help, or for a given operation.",
        "min_stack": 0,
        "opt_args": "1: the operation to get help for."
    },
    "hyp": {
        "desc": "Computes the hypoteneuse (sqrt(x2 + y2)) of rows 0 and 1.",
        "min_stack": 1
    },
    "inv": {
        "desc": "Computes the inverse (1/x) of row 0.",
        "min_stack": 1
    },
    "ln": {
        "desc": "Computes the natural (e-based) log of row 0.",
        "min_stack": 1
    },
    "log": {
        "desc": "Computes the 10-based log of row 0.",
        "min_stack": 1
    },
    "max": {
        "desc": "Computes the max between row 0 and 1, or between the number of rows specified in the optional argument.",
        "min_stack": 2,
        "opt_args": "1: The number of rows to compute the max value of"
    },
    "min": {
        "desc": "Computes the min between row 0 and 1, or between the number of rows specified in the optional argument.",
        "min_stack": 2,
        "opt_args": "1: The number of rows to compute the min value of"
    },
    "mult": {
        "desc": "Multiply rows 0 and 1.",
        "min_stack": 2
    },
    "neg": {
        "desc": "Negate row 0.",
        "min_stack": 1
    },
    "pow": {
        "desc": "Raise row 1 to the power of row 2.",
        "min_stack": 1
    },
    "quit": {
        "desc": "Save the current state and quit.",
        "min_stack": 1
    },
    "rad": {
        "desc": "Convert the value of row 0 (in degrees) to radians.",
        "min_stack": 1
    },
    "rand": {
        "desc": "Add a random fractional value to the stack.",
        "min_stack": 1
    },
    "root": {
        "desc": "Computes the x root of y for rows 0 and 1.",
        "min_stack": 1
    },
    "rot": {
        "desc": "Rotates rows 0-2, or the number of rows specified in the optional argument.",
        "min_stack": 3,
        "opt_args": "1: The number of rows to rotate"
    },
    "sci": {
        "desc": "Display results in scientific notation.",
        "min_stack": 0
    },
    "sin": {
        "desc": "Compute the sine of row 0.",
        "min_stack": 1
    },
    "sinh": {
        "desc": "Compute the hyperbolic sine of row 0.",
        "min_stack": 1
    },
    "sqrt": {
        "desc": "Compute the square root of row 0.",
        "min_stack": 1
    },
    "std": {
        "desc": "Display results in standard notation.",
        "min_stack": 0
    },
    "subt": {
        "desc": "Subtract row 0 from row 1.",
        "min_stack": 2
    },
    "sum": {
        "desc": "Sum all rows, or a given number of them, together.",
        "min_stack": 1,
        "opt_args": "1: the number of rows to sum."
    },
    "swap": {
        "desc": "Swap rows 0 and 1, or row 0 with the one provided in the optional parameter.",
        "min_stack": 1,
        "opt_args": "1: the row to swap with row 0."
    },
    "tan": {
        "desc": "Compute the tangent of row 0.",
        "min_stack": 1
    },
    "tanh": {
        "desc": "Compute the hyperbolic tangent of row 0.",
        "min_stack": 1
    }
}

DISPLAY_MODES = ("std", "fix", "sci", "eng")
BASE_MODES = ("bin", "oct", "dec", "hex")
ANGLE_MODES = ("rad", "deg")

class CRPN:
    """
    A class that contains an RPN calculator
    """
    def __init__(self):
        self.stack = []
        self.display_mode = 'std'
        self.base_mode = 'dec'
        self.angle_mode = 'rad'


    def process_input(self, user_input):
        # is more than one command being joined with '&&'?
        if '&&' in user_input:
            for x in user_input.split('&&'):
                self.process_input(x.strip())
            return

        # split any args from the input.
        cmd = args = None
        if ' ' in user_input:
            cmd_parts = user_input.split(' ')
            cmd = cmd_parts[0]
            if len(cmd_parts) > 1:
                args = cmd_parts[1:]
        else:
            cmd = user_input
            args = None

        if cmd in DISPLAY_MODES:
            self.display_mode = cmd
        elif cmd in BASE_MODES:
            self.base_mode = cmd
        elif cmd in ANGLE_MODES:
            self.angle_mode = cmd
        elif cmd in CONST_MAP:
            self.stack.append(CONST_MAP[cmd])
            return
        elif cmd in OP_METHOD_MAP:
            method = getattr(self, 'op_' + OP_METHOD_MAP[cmd])
            method(args)
            return
        else: # a value, perchance?
            try:
                self.stack.append(int(cmd))
            except ValueError:
                try:
                    self.stack.append(decimal.Decimal(cmd))
                except:
                    print("Unknown input: '%s'. Type 'help' for help." % cmd)
            return


    def require_stack(self, n):
        cur_stack_size = len(self.stack)
        if cur_stack_size < n:
            err_str = "ERROR: Operation requires " + str(n)
            if n == 1:
                err_str += " argument; "
            else:
                err_str +=  " arguments; "
            err_str += "there "
            if cur_stack_size == 0:
                err_str += "are 0"
            elif cur_stack_size == 1:
                err_str += "is only 1"
            else:
                err_str += "are only " + str(cur_stack_size)
            err_str += " on the stack!"
            raise ValueError(err_str)


    def get_stack(self):
        return self.stack


    def load_state(self):
        save_path = os.path.join(str(Path.home()), SAVEFILE)
        if os.path.exists(save_path):
            json_str = None
            with open(save_path, 'r') as savefile:
                json_str = savefile.read()
            save_data = json.loads(json_str)
            self.stack = []
            for item in save_data['stack']:
                value = None
                try:
                    self.stack.append(int(item))
                except ValueError:
                    self.stack.append(decimal.Decimal(item))
            if 'display_mode' in save_data:
                self.display_mode = save_data['display_mode']
            if 'base_mode' in save_data:
                self.base_mode = save_data['base_mode']
            if 'angle_mode' in save_data:
                self.angle_mode = save_data['angle_mode']
            return True
        return False


    def save_state(self):
        save_data = {
            'stack': [],
            'display_mode': self.display_mode,
            'base_mode': self.base_mode,
            'angle_mode': self.angle_mode
            }
        # convert all values to strings to preserve accuracy
        for item in self.stack:
            save_data['stack'].append(str(item))
        json_str = json.dumps(save_data)
        save_path = os.path.join(str(Path.home()), SAVEFILE)
        with open(save_path, 'w+') as savefile:
            savefile.write(json_str)

    #
    # Operations
    #

    def op_abs(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        if type(val1) is int:
            self.stack.append(abs(val1))
        else:
            self.stack.append(decimal.fabs(val1))

    def op_acos(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.acos(val1))

    def op_asin(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.asin(val1))


    def op_atan(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.atan(val1))


    def op_add(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 + val2)


    def op_clear(self, args):
        self.stack = []
        print('Stack cleared.')


    def op_cos(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.cos(val1))


    def op_cosh(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.cosh(val1))


    def op_div(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 / val2)


    def op_deg(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.degrees(val1))


    def op_delete(self, args):
        """
        Delete up to X (default 1) stack elements.
        """
        stack_level = 0
        if args != None:
            stack_level = int(args[0])
        self.require_stack(stack_level+1)
        if stack_level == None:
            self.stack.pop()
        else:
            self.stack.pop(-stack_level-1)


    def op_dup(self, args):
        """
        Duplicate the first element on the stack.
        """
        self.require_stack(1)
        self.stack.append(self.stack[-1])


    def op_fact(self, args):
        self.require_stack(1)
        if type(self.stack[-1]) is not int:
            raise ValueError("ERROR: The value in stack register 0 must be an integer!")
        val1 = self.stack.pop()
        self.stack.append(decimal.factorial(val1))


    def op_help(self, args):
        """
        Print general help or help for a specific command.
        """
        if args == None:
            print(HELP_TEXT + EXTRA_HELP)
        else:
            op = args[0]
            if op in OP_METHOD_MAP:
                op_method = OP_METHOD_MAP[op]
                op_synonyms = find_op_synonyms(op)
                if op_method in OP_HELP:
                    op_help = OP_HELP[op_method]
                    print("\n| " + op_help['desc'])
                    print("| Required stack size: " + str(op_help['min_stack']))
                    if len(op_synonyms) > 1:
                        print("| Synonyms: " + str(op_synonyms))
                    if 'opt_args' in op_help:
                        print("| Optional parameters: " + str(op_help['opt_args']))
                    print("")
                else:
                    print("Operation '%s' has no help!" % op_method)
            elif (op == "commands") or (op == "operations"):
                # list the available operations
                print("\nAvailable operations:")
                for op in OP_HELP:
                    print("* '%s' - %s" % (op, OP_HELP[op]['desc']))
                print("\nFor help about a specific operation, type 'help <op_name>'.\n")
            else:
                print("No operation named '%s'" % op)


    def op_max(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(max([val1, val2]))


    def op_min(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(min([val1, val2]))


    def op_mult(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 * val2)


    def op_neg(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(-val1)


    def op_pow(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        if (type(val1) is int) and (type(val2) is int):
            self.stack.append(val2 ** val1)
        else:
            self.stack.append(decimal.pow(val2, val1))


    def op_quit(self, args):
        self.save_state()
        print("State saved. See you later!")
        sys.exit(0)


    def op_rad(self, args):
        """
        Put a random fractional value (0-1) on the stack.
        """
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.radians(val1))


    def op_rand(self, args):
        self.stack.append(random.random())


    def op_rot(self, args):
        """
        Rotate items on the stack. By default, will rotate the top 3 items.
        """
        stack_level = 3
        if args != None:
            stack_level = int(args[0])
        if stack_level < 3:
            raise ValueError("ERROR: You can't rotate fewer than 3 items!")
        self.require_stack(stack_level)
        val = self.stack.pop(-stack_level)
        self.stack.append(val)


    def op_sin(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.sin(val1))


    def op_sinh(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.sinh(val1))


    def op_subt(self, args):
        self.require_stack(2)
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 - val2)


    def op_sum(self, args):
        """
        Add together all of the entries on the stack and push the result. Optionally, provide a
        number to restrict the number of stack entries summed.
        """
        sum = 0
        stack_levels = len(self.stack)
        if args != None:
            stack_levels = int(args[0])
        self.require_stack(stack_levels)
        for i in range(0, stack_levels):
            sum += self.stack.pop()
        self.stack.append(sum)


    def op_swap(self, args):
        """
        Swap the two bottom values on the stack, or optionally, the bottom value with the stack
        level passed in as an argument.
        """
        stack_level = 1
        if args != None:
            stack_level = int(args[0])
        self.require_stack(stack_level+1)
        val2 = self.stack[-stack_level-1]
        val1 = self.stack[-1]
        self.stack[-stack_level-1] = val1
        self.stack[-1] = val2


    def op_sqrt(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.sqrt(val1))

    def op_tan(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.tan(val1))

    def op_tanh(self, args):
        self.require_stack(1)
        val1 = self.stack.pop()
        self.stack.append(decimal.tanh(val1))


def main():
    app = CRPN()
    
    print(ID_TEXT + HELP_TEXT)

    if app.load_state():
        sys.stdout.write("Restored previously saved state. ")

    print("Current stack:")
    while(True):
        # print the current stack
        stack_values = app.get_stack()
        stack_size = len(stack_values)
        stack_heading = "modes: | %s | %s | %s |" % (app.display_mode, app.angle_mode, app.base_mode)
        print('-' * len(stack_heading))
        print(stack_heading)
        print('-' * len(stack_heading))
        for x in stack_values:
            stack_size -= 1
            print('%2s:   %s' % (stack_size, x))
        print('-' * len(stack_heading))
        sys.stdout.write('> ')
        user_input = input()
        try:
            app.process_input(user_input)
        except ValueError as e:
            print(e)


def find_op_synonyms(op):
    synonyms = []
    op_method = OP_METHOD_MAP[op]
    for op_name in OP_METHOD_MAP:
        if OP_METHOD_MAP[op_name] == op_method:
            synonyms.append(op_name)
    return synonyms

