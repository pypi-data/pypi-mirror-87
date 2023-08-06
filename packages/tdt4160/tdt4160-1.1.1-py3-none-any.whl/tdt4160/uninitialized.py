class UninitializedError(Exception):
    pass


class Uninitialized(int):
    """
    Helper class to use to represent uninitialized values in the registry. This is often needed, and they're usually
    overwritten, which is fine. Using this with overloaded operators throws exceptions for indeterminate results instead
    of swallowing the errors quietly by just using 0 for these values.
    """

    def logic_error(self):
        raise UninitializedError("You can not use an uninitialized value in a logical expression")

    def arithmetic_error(self):
        raise UninitializedError("You can not use an uninitialized value to perform arithmetic")

    def __add__(self, other):
        self.arithmetic_error()

    def __and__(self, other):
        self.logic_error()

    def __eq__(self, other):
        self.logic_error()

    def __float__(self):
        self.arithmetic_error()

    def __format__(self, format_spec):
        return "UNINITIALIZED"  # Ignore format here, this is probably more correct

    def __ge__(self, other):
        self.logic_error()

    def __gt__(self, other):
        self.logic_error()

    def __le__(self, other):
        self.logic_error()

    def __lt__(self, other):
        self.logic_error()

    def __mod__(self, other):
        self.arithmetic_error()

    def __mul__(self, other):
        self.arithmetic_error()

    def __ne__(self, other):
        self.logic_error()

    def __neg__(self):
        self.arithmetic_error()

    def __or__(self, other):
        self.logic_error()

    def __pos__(self):
        self.arithmetic_error()

    def __pow__(self, power, modulo=None):
        self.arithmetic_error()

    def __radd__(self, other):
        self.arithmetic_error()

    def __rand__(self, other):
        self.logic_error()

    def __rdivmod__(self, other):
        self.arithmetic_error()

    def __repr__(self):
        return "UNINITIALIZED"

    def __rfloordiv__(self, other):
        self.arithmetic_error()

    def __rlshift__(self, other):
        self.arithmetic_error()

    def __rmod__(self, other):
        self.arithmetic_error()

    def __rmul__(self, other):
        self.arithmetic_error()

    def __ror__(self, other):
        self.logic_error()

    def __round__(self, n=None):
        self.arithmetic_error()

    def __rpow__(self, other, mod=None):
        self.arithmetic_error()

    def __rrshift__(self, other):
        self.arithmetic_error()

    def __rshift__(self, other):
        self.arithmetic_error()

    def __rsub__(self, other):
        self.arithmetic_error()

    def __rtruediv__(self, other):
        self.arithmetic_error()

    def __rxor__(self, other):
        self.logic_error()

    def __str__(self):
        return "UNINITIALIZED"

    def __sub__(self, other):
        self.arithmetic_error()

    def __truediv__(self, other):
        self.arithmetic_error()

    def __trunc__(self):
        self.arithmetic_error()

    def __xor__(self, other):
        self.logic_error()
