original_print = print

def print_in_color(color):
        def print_in_color(*args, **kwargs):
            original_print(color + " ".join([str(arg) for arg in args]), **kwargs)
        return print_in_color