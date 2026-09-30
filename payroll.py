import re
from decimal import Decimal

from employee import Employee
from validators import format_money, require_text


class Payroll:
    """Bảng lương một kỳ. Quan hệ kết tập (has-a) 1 -- 0..* với Employee,
    KHÔNG kế thừa Employee."""

    def __init__(self, period):
        period = require_text(period, "Kỳ lương")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", period):
            raise ValueError("Kỳ lương phải có dạng YYYY-MM, ví dụ 2026-09")
        self._period = period
        # dict giữ THAM CHIẾU tới đối tượng Employee (không sao chép/cắt lát)
        # => bảo toàn hành vi lớp dẫn xuất; đồng thời tra cứu mã trùng O(1).
        self._employees = {}

    @property
    def period(self):
        return self._period

    def __len__(self):
        return len(self._employees)

    def add_employee(self, employee):
        if not isinstance(employee, Employee):
            raise TypeError("Chỉ được thêm đối tượng kiểu Employee")
        if employee.employee_id in self._employees:
            raise ValueError(f"Mã nhân sự {employee.employee_id} đã tồn tại")
        self._employees[employee.employee_id] = employee

    def find_employee(self, employee_id):
        return self._employees.get(employee_id)   # None nếu không có

    def calculate_total_payroll(self):
        return sum((e.calculate_gross_pay() for e in self._employees.values()),
                   Decimal(0))

    def calculate_payroll_by_department(self, department):
        key = require_text(department, "Phòng ban").casefold()
        return sum((e.calculate_gross_pay() for e in self._employees.values()
                    if e.department.casefold() == key), Decimal(0))

    def find_highest_paid_employee(self):
        if not self._employees:
            return None
        return max(self._employees.values(), key=lambda e: e.calculate_gross_pay())

    def display_payroll(self):
        lines = [f"===== BẢNG LƯƠNG KỲ {self._period} ====="]
        if not self._employees:
            lines.append("(Bảng lương trống - chưa có nhân sự)")
        else:
            for e in self._employees.values():
                lines.append(e.display_payroll_info())    # gọi đa hình
            lines.append("-" * 50)
        lines.append(f"TỔNG BẢNG LƯƠNG: {format_money(self.calculate_total_payroll())}")
        return "\n".join(lines)
