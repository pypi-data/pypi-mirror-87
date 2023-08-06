This is boolean calculator with operate from left to right.

#---------------------------#
Develop by PAO,RAM and YN
#---------------------------#

Example

import boolcalc

inp = "T ^ T <--> ( T --> F v ( T ^ T ) )".split(" ");
print(boolcalc.calculate(inp));

inp = "( ( ( T --> F --> T v F ) <--> T ) ^ T )".split(" ");
print(boolcalc.calculate(inp));

inp = "( ( ( T --> F --> T v F ) <--> T ) ^ T() ".split(" ");
print(boolcalc.calculate(inp));

inp = ["(","T","<-->","F","^","F",")"];
print(boolcalc.calculate(inp));

This library use expression tree data structure to operate the postfix of boolean term.

To convert infix to postfix, use the stack data stucture.

The mentioned datastructure we implement by ourselves.