"""Lớp cơ sở trừu tượng Employee."""
from abc import ABC, abstractmethod
from decimal import Decimal

from bonus import BonusRecord
from validators import (require_in_range, require_positive, require_text,
                        format_money)

DEFAULT_DEPARTMENT = "Unassigned"
DEFAULT_BONUS_REASON = "Thưởng cố định"
MAX_BONUS_RATE = Decimal("0.5")


class Employee(ABC):
    """Nhân sự chung. Là lớp trừu tượng vì không có công thức lương chung."""

    # ---- Constructor (nạp chồng bằng tham số mặc định) ----
    # Employee(employee_id, full_name)
    # Employee(employee_id, full_name, department)
    def __init__(self, employee_id, full_name, department=DEFAULT_DEPARTMENT):
        self._employee_id = require_text(employee_id, "Mã nhân sự")
        self._full_name = require_text(full_name, "Họ tên")
        self._department = require_text(department, "Phòng ban")
        self._bonus_history = []          # list[BonusRecord]; tổng thưởng được suy ra

    # ---- Thuộc tính (đóng gói) ----
    @property
    def employee_id(self):
        return self._employee_id          # chỉ đọc: mã không đổi sau khi tạo

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = require_text(value, "Họ tên")

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = require_text(value, "Phòng ban")

    @property
    def monthly_bonus(self):
        """Tổng thưởng tháng = tổng lịch sử thưởng (một nguồn sự thật duy nhất)."""
        return sum((r.amount for r in self._bonus_history), Decimal(0))

    @property
    def bonus_history(self):
        return tuple(self._bonus_history)  # bản sao bất biến

    # ---- Nạp chồng addBonus ----
    def add_bonus(self, *args):
        """Ba phiên bản (chọn theo số đối số lúc chạy):
        add_bonus(amount)
        add_bonus(amount, reason)
        add_bonus(rate, reference_amount, reason)
        """
        if len(args) == 1:
            return self.add_fixed_bonus(args[0])
        if len(args) == 2:
            return self.add_fixed_bonus(args[0], args[1])
        if len(args) == 3:
            return self.add_rate_bonus(args[0], args[1], args[2])
        raise TypeError("add_bonus nhận 1, 2 hoặc 3 đối số, "
                        f"nhận {len(args)}")

    def add_fixed_bonus(self, amount, reason=DEFAULT_BONUS_REASON):
        value = require_positive(amount, "Khoản thưởng")
        reason = require_text(reason, "Lý do thưởng")
        self._bonus_history.append(BonusRecord(value, reason, "FIXED"))
        return value

    def add_rate_bonus(self, rate, reference_amount, reason):
        rate = require_in_range(rate, "Tỷ lệ thưởng", 0, MAX_BONUS_RATE)
        if rate <= 0:
            raise ValueError("Tỷ lệ thưởng phải lớn hơn 0")
        reference = require_positive(reference_amount, "Giá trị tham chiếu")
        reason = require_text(reason, "Lý do thưởng")
        value = rate * reference
        self._bonus_history.append(
            BonusRecord(value, reason, "RATE", rate, reference))
        return value

    def reset_bonus(self):
        """Đặt lại thưởng khi bắt đầu kỳ lương mới."""
        self._bonus_history.clear()

    # ---- Hành vi đa hình (lớp dẫn xuất phải ghi đè) ----
    @abstractmethod
    def calculate_gross_pay(self):
        """Thu nhập trước khấu trừ."""

    @abstractmethod
    def get_employee_type(self):
        """Tên loại nhân sự."""

    @abstractmethod
    def display_payroll_info(self):
        """Trả về chuỗi hiển thị chi tiết thu nhập."""

    # ---- Hỗ trợ hiển thị cho lớp dẫn xuất ----
    def _header(self):
        return (f"[{self.get_employee_type()}] {self.employee_id} - "
                f"{self.full_name} | Phòng: {self.department}")

    def _bonus_line(self):
        return f"  Thưởng: {format_money(self.monthly_bonus)}"

    def _total_line(self):
        return f"  Tổng thu nhập: {format_money(self.calculate_gross_pay())}"

    def __repr__(self):
        return (f"{type(self).__name__}(id={self.employee_id!r}, "
                f"name={self.full_name!r}, dept={self.department!r})")
