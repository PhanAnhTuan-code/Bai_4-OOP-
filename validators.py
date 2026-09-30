# MSSV: 20227207
# Họ và tên: Phan Anh Tuấn


"""Các hàm kiểm tra dữ liệu dùng chung (tránh lặp logic validate ở nhiều lớp)."""
from decimal import Decimal


def require_text(value, name):
    """Chuỗi không rỗng (sau khi strip). Trả về chuỗi đã strip."""
    if not isinstance(value, str):
        raise TypeError(f"{name} phải là chuỗi ký tự")
    text = value.strip()
    if not text:
        raise ValueError(f"{name} không được rỗng")
    return text


def to_decimal(value, name):
    """Chuyển int/float/Decimal sang Decimal; từ chối bool, chuỗi, NaN, vô cực."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise TypeError(f"{name} phải là số")
    number = value if isinstance(value, Decimal) else Decimal(str(value))
    if not number.is_finite():
        raise ValueError(f"{name} phải là số hữu hạn")
    return number


def require_non_negative(value, name):
    number = to_decimal(value, name)
    if number < 0:
        raise ValueError(f"{name} không được âm (nhận {number})")
    return number


def require_positive(value, name):
    number = to_decimal(value, name)
    if number <= 0:
        raise ValueError(f"{name} phải lớn hơn 0 (nhận {number})")
    return number


def require_in_range(value, name, low, high):
    """Kiểm tra low <= value <= high (đóng hai đầu)."""
    number = to_decimal(value, name)
    if not (Decimal(str(low)) <= number <= Decimal(str(high))):
        raise ValueError(f"{name} phải nằm trong [{low}, {high}] (nhận {number})")
    return number


def format_money(amount):
    """Định dạng tiền kiểu Việt Nam: 18.000.000 VND."""
    return f"{amount:,.0f}".replace(",", ".") + " VND"
