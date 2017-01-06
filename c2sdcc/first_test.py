from __future__ import print_function
import sys

from pycparser import c_parser, c_generator
from var_generator import VarGenerator

text = r"""
void func(void)
{
  x = 1;
  int z = 2;
  int w, n;

  for (int i = 0; i != 3; i++) {
  }

  for (j = 0; i != 3; i++) {
  }
}
"""

parser = c_parser.CParser()
ast = parser.parse(text)
print("Before:")
ast.show(offset=2)


print("After changing vars")
var_gen = VarGenerator()
print(var_gen.visit(ast))

print("Generated:")
generator = c_generator.CGenerator()
print(generator.visit(ast))