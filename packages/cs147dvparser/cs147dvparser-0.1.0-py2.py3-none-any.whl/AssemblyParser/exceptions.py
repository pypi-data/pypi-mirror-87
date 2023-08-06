'''
a list of exceptions that are used by the CS147DV Assembly Parser
'''
class CS147DVError(Exception):
    pass

class MnemonicError(CS147DVError):
    pass

class RtypeError(CS147DVError):
    pass

class ItypeError(CS147DVError):
    pass

class JtypeError(CS147DVError):
    pass

class NumTypeError(CS147DVError):
    pass

class BaseError(CS147DVError):
    pass

class FieldLengthError(CS147DVError):
    pass

class RegisterError(CS147DVError):
    pass

class ShamtError(CS147DVError):
    pass

class ImmediateError(CS147DVError):
    pass

class AddressError(CS147DVError):
    pass
