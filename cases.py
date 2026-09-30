# MSSV: 20227207
# Họ và tên: Phan Anh Tuấn

"""Bảng tình huống kiểm thử: (id, mô tả, kỳ vọng, hàm trả về chuỗi quan sát).
Dùng chung cho unittest (test_payroll.py) và bộ tạo báo cáo (run_report.py)."""
from decimal import Decimal

from employee import Employee
from hourly_employee import HourlyEmployee
from main import build_sample_payroll
from payroll import Payroll
from salaried_employee import SalariedEmployee
from sales_employee import SalesEmployee


def money(x):
    return f"{x:,.0f}"


def err(func):
    """Chạy func; trả về tên lớp ngoại lệ nếu có, ngược lại 'Không lỗi'."""
    try:
        func()
    except Exception as ex:                     # noqa: BLE001
        return type(ex).__name__
    return "Không lỗi"


def hourly(hours):
    return HourlyEmployee("H", "Tên", "PB", 100_000, hours)


def _sample():
    return build_sample_payroll()


def _empty_payroll():
    p = Payroll("2026-09")
    return "|".join([money(p.calculate_total_payroll()),
                     str(p.find_highest_paid_employee()),
                     str(p.find_employee("X")),
                     p.display_payroll().splitlines()[1]])


def _reset():
    e = SalariedEmployee("S", "A", "PB", 1_000_000)
    e.add_bonus(200_000)
    e.reset_bonus()
    return money(e.calculate_gross_pay())


def _defaults():
    e = SalariedEmployee.basic("S", "A")
    return f"{e.department}|{money(e.monthly_bonus)}|{money(e.calculate_gross_pay())}"


def _dup():
    p = Payroll("2026-09")
    p.add_employee(SalariedEmployee("X1", "A"))
    return err(lambda: p.add_employee(HourlyEmployee("X1", "B")))


def _contract():
    class ContractEmployee(Employee):           # loại mới, KHÔNG sửa Payroll
        def calculate_gross_pay(self):
            return Decimal(5_000_000) + self.monthly_bonus

        def get_employee_type(self):
            return "Contract"

        def display_payroll_info(self):
            return self._header()

    p = _sample()
    p.add_employee(ContractEmployee("C1", "Hợp đồng", "Hỗ trợ"))
    return f"{money(p.calculate_total_payroll())}|{money(p.calculate_payroll_by_department('Hỗ trợ'))}"


def _history():
    e = SalariedEmployee("S", "A")
    e.add_bonus(100_000, "a")
    e.add_bonus(0.1, 1_000_000, "b")
    return f"{len(e.bonus_history)}|{money(e.monthly_bonus)}"


def _sale():
    e = SalesEmployee("S", "A", "PB", 0, 100, 0.1)
    e.record_sale(50)
    return money(e.sales_revenue)


CASES = [
    ("TC01", "E001 lương cố định 15tr + phụ cấp 2tr + thưởng 1tr", "18,000,000",
     lambda: money(_e1().calculate_gross_pay())),
    ("TC02", "E002 theo giờ, 150 giờ (không vượt ngưỡng) + thưởng 500k", "15,500,000",
     lambda: money(_sample().find_employee("E002").calculate_gross_pay())),
    ("TC03", "E003 theo giờ, 170 giờ (vượt 10 giờ x 1,5)", "17,500,000",
     lambda: money(_sample().find_employee("E003").calculate_gross_pay())),
    ("TC04", "E004 kinh doanh: 8tr + 5% x 200tr + thưởng 2% x 50tr", "19,000,000",
     lambda: money(_sample().find_employee("E004").calculate_gross_pay())),
    ("TC05", "Tổng bảng lương 4 nhân sự", "70,000,000",
     lambda: money(_sample().calculate_total_payroll())),
    ("TC06", "Tổng phòng Hỗ trợ (E002 + E003)", "33,000,000",
     lambda: money(_sample().calculate_payroll_by_department("Hỗ trợ"))),
    ("TC07", "Người thu nhập cao nhất", "E004",
     lambda: _sample().find_highest_paid_employee().employee_id),
    ("TC08", "Biên: đúng 160 giờ (chưa có giờ vượt)", "16,000,000",
     lambda: money(hourly(160).calculate_gross_pay())),
    ("TC09", "Biên: 161 giờ (vượt 1 giờ)", "16,150,000",
     lambda: money(hourly(161).calculate_gross_pay())),
    ("TC10", "Biên trên: 250 giờ hợp lệ (160 + 90 x 1,5)", "29,500,000",
     lambda: money(hourly(250).calculate_gross_pay())),
    ("TC11", "Lỗi: 251 giờ (vượt giới hạn 250)", "ValueError",
     lambda: err(lambda: hourly(251))),
    ("TC12", "Lỗi: số giờ âm (-1)", "ValueError",
     lambda: err(lambda: hourly(-1))),
    ("TC13", "Biên dưới: 0 giờ", "0",
     lambda: money(hourly(0).calculate_gross_pay())),
    ("TC14", "Biên: hoa hồng 0,3 hợp lệ", "Không lỗi",
     lambda: err(lambda: SalesEmployee("S", "A", "PB", 0, 0, 0.3))),
    ("TC15", "Lỗi: hoa hồng 0,31", "ValueError",
     lambda: err(lambda: SalesEmployee("S", "A", "PB", 0, 0, 0.31))),
    ("TC16", "Lỗi: hoa hồng âm (-0,01)", "ValueError",
     lambda: err(lambda: SalesEmployee("S", "A", "PB", 0, 0, -0.01))),
    ("TC17", "Lỗi: mã nhân sự rỗng", "ValueError",
     lambda: err(lambda: SalariedEmployee("", "A"))),
    ("TC18", "Lỗi: họ tên chỉ có khoảng trắng", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "   "))),
    ("TC19", "Lỗi: phòng ban rỗng", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A", ""))),
    ("TC20", "Lỗi: lương tháng âm", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A", "PB", -1))),
    ("TC21", "addBonus(amount) với amount = 0", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(0))),
    ("TC22", "addBonus(amount, reason) với reason rỗng", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(100, " "))),
    ("TC23", "addBonus(rate, ref, reason): rate = 0,5 hợp lệ", "Không lỗi",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(0.5, 100, "ok"))),
    ("TC24", "addBonus(rate, ref, reason): rate = 0,51", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(0.51, 100, "x"))),
    ("TC25", "addBonus(rate, ref, reason): rate = 0", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(0, 100, "x"))),
    ("TC26", "addBonus(rate, ref, reason): referenceAmount = 0", "ValueError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(0.1, 0, "x"))),
    ("TC27", "addBonus với 4 đối số (không có phiên bản phù hợp)", "TypeError",
     lambda: err(lambda: SalariedEmployee("S", "A").add_bonus(1, 2, 3, 4))),
    ("TC28", "Lịch sử thưởng: 1 thưởng cố định + 1 thưởng theo tỷ lệ", "2|200,000",
     _history),
    ("TC29", "Constructor rút gọn: giá trị mặc định", "Unassigned|0|0",
     _defaults),
    ("TC30", "resetBonus() đầu kỳ mới", "1,000,000",
     _reset),
    ("TC31", "Không thể khởi tạo lớp trừu tượng Employee", "TypeError",
     lambda: err(lambda: Employee("E", "A"))),
    ("TC32", "Payroll: thêm nhân sự trùng mã", "ValueError", _dup),
    ("TC33", "Payroll: thêm đối tượng không phải Employee", "TypeError",
     lambda: err(lambda: Payroll("2026-09").add_employee("E001"))),
    ("TC34", "Payroll rỗng: tổng, cao nhất, tìm, hiển thị",
     "0|None|None|(Bảng lương trống - chưa có nhân sự)", _empty_payroll),
    ("TC35", "Kỳ lương sai định dạng (2026-13)", "ValueError",
     lambda: err(lambda: Payroll("2026-13"))),
    ("TC36", "Cập nhật doanh số âm bị từ chối", "ValueError",
     lambda: err(lambda: SalesEmployee("S", "A").update_sales_revenue(-5))),
    ("TC37", "Ghi nhận thêm đơn hàng recordSale(50) vào doanh số 100", "150",
     _sale),
    ("TC38", "Thêm ContractEmployee mới: Payroll không cần sửa (tổng, tổng phòng Hỗ trợ)",
     "75,000,000|38,000,000", _contract),
    ("TC39", "Giá trị lương là chuỗi ký tự (sai kiểu)", "TypeError",
     lambda: err(lambda: SalariedEmployee("S", "A", "PB", "abc"))),
    ("TC40", "Giá trị lương là bool (True)", "TypeError",
     lambda: err(lambda: SalariedEmployee("S", "A", "PB", True))),
]


def _e1():
    e = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15_000_000, 2_000_000)
    e.add_bonus(1_000_000)
    return e
