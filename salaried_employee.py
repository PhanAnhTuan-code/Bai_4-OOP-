from employee import DEFAULT_DEPARTMENT, Employee
from validators import format_money, require_non_negative


class SalariedEmployee(Employee):
    """Nhân viên lương cố định."""

    # Constructor đầy đủ (các tham số sau full_name có giá trị mặc định
    # nên cũng dùng được như constructor rút gọn).
    def __init__(self, employee_id, full_name, department=DEFAULT_DEPARTMENT,
                 monthly_salary=0, responsibility_allowance=0):
        super().__init__(employee_id, full_name, department)   # ủy quyền
        self.monthly_salary = monthly_salary
        self.responsibility_allowance = responsibility_allowance

    # Constructor rút gọn (factory): lương = 0, phụ cấp = 0, phòng ban mặc định
    @classmethod
    def basic(cls, employee_id, full_name):
        return cls(employee_id, full_name)

    @property
    def monthly_salary(self):
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value):
        self._monthly_salary = require_non_negative(value, "Lương tháng")

    @property
    def responsibility_allowance(self):
        return self._allowance

    @responsibility_allowance.setter
    def responsibility_allowance(self, value):
        self._allowance = require_non_negative(value, "Phụ cấp trách nhiệm")

    def calculate_gross_pay(self):
        return self._monthly_salary + self._allowance + self.monthly_bonus

    def get_employee_type(self):
        return "Salaried"

    def display_payroll_info(self):
        return "\n".join([
            self._header(),
            f"  Lương tháng: {format_money(self._monthly_salary)}",
            f"  Phụ cấp trách nhiệm: {format_money(self._allowance)}",
            self._bonus_line(),
            self._total_line(),
        ])
