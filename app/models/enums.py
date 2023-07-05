from enum import Enum


class DocumentTypeEnum(str, Enum):
    """
    Enum for document types
    Args:
        str (Enum): Enum for document types
    """
    CPF = "CPF"
    CNPJ = "CNPJ"
    RG = "RG"
    CNH = "CNH"
    PASSPORT = "PASSPORT"


class StatusEnum(str, Enum):
    """
    Enum for status
    Args:
        str (Enum): Enum for status
    """
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class AccountTypeEnum(str, Enum):
    """
    Enum for account types
    Args:
        str (Enum): Enum for account types
    """
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    SALARY = "SALARY"
