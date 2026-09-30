# MSSV: 20227207
# Họ và tên: Phan Anh Tuấn


from employee import DEFAULT_DEPARTMENT, Employee
from validators import (format_money, require_in_range, require_non_negative,
                        require_positive)

MAX_COMMISSION_RATE = "0.3"


class SalesEmployee(Employee):
    """Nhân viên kinh doanh: lương cơ bản + hoa hồng theo doanh số."""

    def __init__(self, employee_id, full_name, department=DEFAULT_DEPARTMENT,
                 base_salary=0, sales_revenue=0, commission_rate=0):
        super().__init__(employee_id, full_name, department)
        self.base_salary = base_salary
        self.sales_revenue = sales_revenue
        self.commission_rate = commission_rate

    @classmethod
    def basic(cls, employee_id, full_name):
        return cls(employee_id, full_name)

    @property
    def base_salary(self):
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):
        self._base_salary = require_non_negative(value, "Lương cơ bản")

    @property
    def sales_revenue(self):
        return self._sales_revenue

    @sales_revenue.setter
    def sales_revenue(self, value):
        self._sales_revenue = require_non_negative(value, "Doanh số")

    @property
    def commission_rate(self):
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        self._commission_rate = require_in_range(
            value, "Tỷ lệ hoa hồng", 0, MAX_COMMISSION_RATE)

    # Cập nhật doanh số có kiểm soát (thay vì cho ghi trực tiếp tùy ý)
    def update_sales_revenue(self, new_revenue):
        self.sales_revenue = new_revenue

    def record_sale(self, amount):
        self._sales_revenue += require_positive(amount, "Giá trị đơn hàng")

    @property
    def commission(self):
        return self._sales_revenue * self._commission_rate

    def calculate_gross_pay(self):
        return self._base_salary + self.commission + self.monthly_bonus

    def get_employee_type(self):
        return "Sales"

    def display_payroll_info(self):
        return "\n".join([
            self._header(),
            f"  Lương cơ bản: {format_money(self._base_salary)}",
            f"  Doanh số: {format_money(self._sales_revenue)} x "
            f"{self._commission_rate * 100:.1f}% = {format_money(self.commission)}",
            self._bonus_line(),
            self._total_line(),
        ])
