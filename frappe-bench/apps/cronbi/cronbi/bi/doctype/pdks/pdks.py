import frappe
from frappe.model.document import Document
from cronbi.bi.utils.pdks_monthly import calculate_pdks_monthly


class PDKS(Document):

    def before_insert(self):
        self.validate_period()

    def validate_period(self):
        if not self.year or not self.month:
            frappe.throw("Yıl ve ay zorunludur.")

    @frappe.whitelist()
    def calculate(self):
        self.pdks_deductions = []  # 🔥 child table temizle

        results = calculate_pdks_monthly(self.year, self.month)

        for r in results:
            row = self.append("pdks_deductions", {})
            row.user_email = r["user_email"]
            row.deduction_type = r["deduction_type"]
            row.deduction_value = r["deduction_value"]
            row.present_days = r["present_days"]
            row.absent_days = r["absent_days"]
            row.worked_hours = r["worked_hours"]
            row.missing_hours = r["missing_hours"]
            row.early_exit_count = r["early_exit_count"]

        self.save(ignore_permissions=True)
