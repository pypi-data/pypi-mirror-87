class KastenException(Exception):
    """Generic exception"""
    pass

class InvalidKastenTypeLength(KastenException):
    """Occurs when Kasten packed bytes have invalid data type"""
    pass

class InvalidEncryptionMode(KastenException):
    """Occurs when Kasten packed bytes have invalid encryption mode"""
    pass

class InvalidID(KastenException):
    """Occurs when a Kasten generator fails validation, which means data does not match KastenChecksum"""
    pass

