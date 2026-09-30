# MSSV: 20227207
# Họ và tên: Phan Anh Tuấn


import sys

from hourly_employee import HourlyEmployee
from payroll import Payroll
from salaried_employee import SalariedEmployee
from sales_employee import SalesEmployee
from validators import format_money


def build_sample_payroll():
    e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15_000_000, 2_000_000)
    e1.add_bonus(1_000_000)                                    # phiên bản 1
    e2 = HourlyEmployee("E002", "Trần Thu Bình", "Hỗ trợ", 100_000, 150)
    e2.add_bonus(500_000, "Hoàn thành dự án")                  # phiên bản 2
    e3 = HourlyEmployee("E003", "Lê Hoàng Chi", "Hỗ trợ", 100_000, 170)
    e4 = SalesEmployee("E004", "Phạm Quốc Dũng", "Kinh doanh",
                       8_000_000, 200_000_000, 0.05)
    e4.add_bonus(0.02, 50_000_000, "Thưởng vượt chỉ tiêu")     # phiên bản 3
    payroll = Payroll("2026-09")
    for e in (e1, e2, e3, e4):
        payroll.add_employee(e)
    return payroll


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = build_sample_payroll()
    print(p.display_payroll())
    print("Tổng phòng Hỗ trợ:", format_money(p.calculate_payroll_by_department("Hỗ trợ")))
    top = p.find_highest_paid_employee()
    print("Thu nhập cao nhất:", top.full_name, format_money(top.calculate_gross_pay()))
