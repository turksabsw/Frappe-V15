import frappe

@frappe.whitelist(allow_guest=False)
def whoami():
    user = frappe.session.user

    if not user or user == "Guest":
        frappe.throw("Unauthorized", frappe.PermissionError)

    roles = frappe.get_roles(user)

    return {
        "user": user,
        "roles": roles,
        "is_authenticated": True
    }
