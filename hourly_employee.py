from decimal import Decimal

from employee import DEFAULT_DEPARTMENT, Employee
from validators import format_money, require_in_range, require_non_negative

STANDARD_HOURS = Decimal(160)
OVERTIME_MULTIPLIER = Decimal("1.5")
MAX_HOURS = 250


class HourlyEmployee(Employee):
    """Nhân viên theo giờ (giờ vượt 160 được nhân 1,5)."""

    def __init__(self, employee_id, full_name, department=DEFAULT_DEPARTMENT,
                 hourly_rate=0, worked_hours=0):
        super().__init__(employee_id, full_name, department)
        self.hourly_rate = hourly_rate
        self.worked_hours = worked_hours

    @classmethod
    def basic(cls, employee_id, full_name):
        return cls(employee_id, full_name)

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        self._hourly_rate = require_non_negative(value, "Đơn giá giờ")

    @property
    def worked_hours(self):
        return self._worked_hours

    @worked_hours.setter
    def worked_hours(self, value):
        self._worked_hours = require_in_range(value, "Số giờ làm", 0, MAX_HOURS)

    # Các đại lượng được TÍNH từ trạng thái hiện có, không lưu riêng
    @property
    def regular_hours(self):
        return min(self._worked_hours, STANDARD_HOURS)

    @property
    def overtime_hours(self):
        return max(self._worked_hours - STANDARD_HOURS, Decimal(0))

    @property
    def base_pay(self):
        return (self.regular_hours * self._hourly_rate
                + self.overtime_hours * self._hourly_rate * OVERTIME_MULTIPLIER)

    def calculate_gross_pay(self):
        return self.base_pay + self.monthly_bonus

    def get_employee_type(self):
        return "Hourly"

    def display_payroll_info(self):
        return "\n".join([
            self._header(),
            f"  Đơn giá giờ: {format_money(self._hourly_rate)}",
            f"  Giờ thường: {self.regular_hours} | Giờ vượt ngưỡng: {self.overtime_hours}",
            f"  Lương giờ (basePay): {format_money(self.base_pay)}",
            self._bonus_line(),
            self._total_line(),
        ])
