from tython_types import List

def print_forms(expr):
	if type(expr) == List:
		return f"({' '.join(print_forms(e) for e in expr)})"
	if type(expr) == bool:
		if expr:
			return "#t"
		else:
			return '#f'
	else:
		return str(expr)