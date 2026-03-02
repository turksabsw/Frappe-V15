import frappe
from frappe.utils import now_datetime


# ========================
# CHECK IN
# ========================
@frappe.whitelist()
def check_in():
    user = frappe.session.user

    existing = frappe.get_all(
        "Daily Checkin",
        filters={
            "user_email": user,
            "status": "Checked In",
        },
        limit=1,
    )

    if existing:
        frappe.throw("Zaten giriş yapılmış")

    doc = frappe.new_doc("Daily Checkin")
    doc.user_email = user
    doc.check_in_time = now_datetime()
    doc.status = "Checked In"
    doc.insert(ignore_permissions=True)

    frappe.db.commit()

    return {
        "status": "checked_in",
        "time": doc.check_in_time,
        "name": doc.name,
    }


# ========================
# CHECK OUT
# ========================
@frappe.whitelist()
def check_out():
    user = frappe.session.user

    records = frappe.get_all(
        "Daily Checkin",
        filters={
            "user_email": user,
            "check_out_time": ["is", "not set"],
        },
        order_by="check_in_time desc",
        limit=1,
        pluck="name",
        ignore_permissions=True,
    )

    if not records:
        frappe.throw("Açık giriş bulunamadı")

    doc = frappe.get_doc("Daily Checkin", records[0])
    doc.check_out_time = now_datetime()
    doc.status = "Checked Out"
    doc.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "status": "checked_out",
        "time": doc.check_out_time,
        "name": doc.name,
    }


# ========================
# USER – KENDİ KAYITLARI
# ========================
@frappe.whitelist()
def my_daily_checkins():
    user = frappe.session.user

    return frappe.get_all(
        "Daily Checkin",
        filters={"user_email": user},
        fields=[
            "name",
            "date",
            "check_in_time",
            "check_out_time",
            "status",
            "work_duration_minutes",
        ],
        order_by="check_in_time desc",
    )


# ========================
# ADMIN – TÜM KAYITLAR
# ========================
@frappe.whitelist()
def all_daily_checkins():
    user = frappe.session.user

    if "System Manager" not in frappe.get_roles(user):
        frappe.throw("Yetkin yok", frappe.PermissionError)

    return frappe.get_all(
        "Daily Checkin",
        fields=[
            "name",
            "user_email",
            "date",
            "check_in_time",
            "check_out_time",
            "status",
            "work_duration_minutes",
        ],
        order_by="check_in_time desc",
    )
