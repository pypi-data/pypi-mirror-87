This is boolean calculator with operate from left to right.

Developby PAO,RAM and YN

Example

import boolcalc

inp = "T ^ T <--> ( T --> F v ( T ^ T ) )".split(" ")
print(boolcalc.calculate(inp))

inp = "( ( ( T --> F --> T v F ) <--> T ) ^ T )".split(" ")
print(boolcalc.calculate(inp))

inp = "( ( ( T --> F --> T v F ) <--> T ) ^ T() ".split(" ")
print(boolcalc.calculate(inp))

inp = ["(","T","<-->","F","^","F",")"]
print(boolcalc.calculate(inp))