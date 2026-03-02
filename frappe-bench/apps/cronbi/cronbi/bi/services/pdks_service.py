import frappe
from frappe.utils import nowdate
from cronbi.bi.utils.pdks_monthly import calculate_pdks_monthly


@frappe.whitelist()
def create_pdks_monthly(year: int, month: int):
    year = int(year)
    month = int(month)
    month_str = f"{month:02d}"

    # 1 Aynı ay varsa sil (senin tercihin, OK)
    existing = frappe.db.get_value(
        "PDKS",
        {"year": year, "month": month_str},
        "name"
    )

    if existing:
        frappe.delete_doc("PDKS", existing, force=1)

    # 2 Hesapla
    results = calculate_pdks_monthly(year, month)

    if not results:
        frappe.throw("Bu ay için Daily Checkin bulunamadı.")

    # 3 Ana PDKS belge
    doc = frappe.get_doc({
        "doctype": "PDKS",
        "year": year,
        "month": month_str,
        "generated_on": nowdate(),
        "status": "Draft",
    })

    unique_users = set()

    # 4 Child table – SATIR BAZLI (DOĞRU MODEL)
    for r in results:
        unique_users.add(r["user_email"])

        doc.append("employees", {
            "user_email": r["user_email"],
            "present_days": r["present_days"],
            "absent_days": r["absent_days"],
            "expected_hours": r["present_days"] * 9,
            "worked_hours": r["worked_hours"],
            "missing_hours": r["missing_hours"],
            "early_exit_count": r["early_exit_count"],

            "deduction_type": r["deduction_type"],   # Day | Hour | None
            "deduction_value": r["deduction_value"],
        })

    doc.total_employees = len(unique_users)

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return doc.name
