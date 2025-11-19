import re
from datetime import datetime

CPF_CNPJ_RE = re.compile(r"[^0-9]")
PHONE_RE = re.compile(r"[^0-9+]")


def sanitize_numeric(value: str) -> str:
    """Keep only digits and decimal separators (dot or comma)."""
    if value is None:
        return ""
    # Allow digits, dot, comma
    return re.sub(r"[^0-9\.,]", "", str(value))


def validate_integer(new_value: str) -> bool:
    """Return True if new_value is empty or a valid integer."""
    if new_value == "":
        return True
    return new_value.isdigit()


def validate_decimal(new_value: str) -> bool:
    """Allow digits, one dot or comma, optional leading digits."""
    if new_value == "":
        return True
    # Replace comma with dot for checking
    nv = new_value.replace(',', '.')
    # Allow only one dot
    if nv.count('.') > 1:
        return False
    # After replacing, check all chars are digits or dot
    for ch in nv:
        if not (ch.isdigit() or ch == '.'):
            return False
    return True


def mask_cpf_cnpj(value: str) -> str:
    """Format CPF or CNPJ for display. If length 11 -> CPF, if 14 -> CNPJ."""
    digits = re.sub(r"\D", "", str(value))
    if len(digits) <= 11:
        # CPF: 000.000.000-00
        digits = digits.ljust(11, '0')[:11]
        return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"
    else:
        # CNPJ: 00.000.000/0000-00
        digits = digits.ljust(14, '0')[:14]
        return f"{digits[0:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"


def mask_phone(value: str) -> str:
    digits = re.sub(r"\D", "", str(value))
    if len(digits) <= 10:
        # (00) 0000-0000
        digits = digits.ljust(10, '0')[:10]
        return f"({digits[0:2]}) {digits[2:6]}-{digits[6:10]}"
    else:
        # (00) 00000-0000
        digits = digits.ljust(11, '0')[:11]
        return f"({digits[0:2]}) {digits[2:7]}-{digits[7:11]}"


def validate_date_yyyy_mm_dd(value: str) -> bool:
    if value == "":
        return True
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except Exception:
        return False
