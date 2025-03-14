from sympy.tensor.array.expressions import from_array_to_matrix
from sympy.tensor.array.expressions.conv_array_to_indexed import _conv_to_from_decorator

convert_array_to_matrix = _conv_to_from_decorator(from_array_to_matrix.convert_array_to_matrix)
_array2matrix = _conv_to_from_decorator(from_array_to_matrix._array2matrix)
_remove_trivial_dims = _conv_to_from_decorator(from_array_to_matrix._remove_trivial_dims)
