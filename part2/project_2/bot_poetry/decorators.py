from functools import wraps


def input_error(func):
    @wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError as index_ex_message:
            return index_ex_message
        except ValueError as val_ex_message:
            return val_ex_message
        except KeyError as key_ex_message:
            return key_ex_message
        except TypeError as type_ex_message:
            return type_ex_message
        except AttributeError as atr_ex_message:
            return atr_ex_message
        except ZeroDivisionError as zero_div_ex_message:
            return zero_div_ex_message
        except FileNotFoundError as file_not_found_ex_message:
            return file_not_found_ex_message
        except PermissionError as permission_ex_message:
            return permission_ex_message

    return wrapper
