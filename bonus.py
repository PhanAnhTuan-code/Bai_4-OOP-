# MSSV: 20227207
# Họ và tên: Phan Anh Tuấn

"""Bản ghi thưởng bất biến - dùng để lưu lịch sử thưởng (không dùng mảng song song)."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class BonusRecord:
    amount: Decimal
    reason: str
    kind: str                                   # "FIXED" hoặc "RATE"
    rate: Optional[Decimal] = None              # chỉ có với thưởng theo tỷ lệ
    reference_amount: Optional[Decimal] = None  # chỉ có với thưởng theo tỷ lệ
