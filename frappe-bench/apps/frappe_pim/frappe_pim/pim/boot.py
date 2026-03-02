"""PIM Boot Session Configuration

This module adds PIM-specific data to the Frappe boot session.
The boot_session function is called during Frappe's boot process
to inject PIM-related configuration and data into the client-side
boot info object.

This allows PIM-specific settings, permissions, and configurations
to be available to the frontend without additional API calls.
"""


def boot_session(bootinfo):
    """Add PIM-specific data to boot session.
    
    This function is called by Frappe during the boot process to
    add PIM-specific configuration and data to the bootinfo dictionary
    that is sent to the client.
    
    Args:
        bootinfo: Dictionary containing boot session data that will
                 be sent to the client. This function modifies it in-place.
    
    The bootinfo dictionary typically contains:
        - user information
        - system settings
        - app configurations
        - permissions
        - custom data
    
    Example additions:
        - PIM module settings
        - User PIM permissions
        - Enabled PIM features
        - Default PIM configurations
    """
    import frappe
    
    try:
        # Initialize PIM section in bootinfo if it doesn't exist
        if "pim" not in bootinfo:
            bootinfo["pim"] = {}
        
        # Add PIM settings if PIM Settings doctype exists
        if frappe.db.exists("DocType", "PIM Settings"):
            try:
                pim_settings = frappe.get_cached_doc("PIM Settings")
                bootinfo["pim"]["settings"] = {
                    "enable_ai_enrichment": getattr(pim_settings, "enable_ai_enrichment", False),
                    "enable_gdsn_sync": getattr(pim_settings, "enable_gdsn_sync", False),
                    "enable_brand_portal": getattr(pim_settings, "enable_brand_portal", False),
                    "default_export_format": getattr(pim_settings, "default_export_format", "bmecat"),
                }
            except Exception:
                # If PIM Settings doesn't exist or can't be loaded, use defaults
                bootinfo["pim"]["settings"] = {
                    "enable_ai_enrichment": False,
                    "enable_gdsn_sync": False,
                    "enable_brand_portal": False,
                    "default_export_format": "bmecat",
                }
        else:
            # Default settings if PIM Settings doctype doesn't exist
            bootinfo["pim"]["settings"] = {
                "enable_ai_enrichment": False,
                "enable_gdsn_sync": False,
                "enable_brand_portal": False,
                "default_export_format": "bmecat",
            }
        
        # Add user PIM permissions
        user = frappe.session.user
        if user and user != "Guest":
            bootinfo["pim"]["permissions"] = {
                "has_pim_access": frappe.has_permission("Product Master", "read", user=user),
                "can_create_product": frappe.has_permission("Product Master", "create", user=user),
                "can_edit_product": frappe.has_permission("Product Master", "write", user=user),
                "can_delete_product": frappe.has_permission("Product Master", "delete", user=user),
                "is_pim_manager": "PIM Manager" in frappe.get_roles(user),
                "is_brand_portal_user": "Brand Portal User" in frappe.get_roles(user),
                "is_data_steward": "Data Steward" in frappe.get_roles(user),
            }
        else:
            bootinfo["pim"]["permissions"] = {
                "has_pim_access": False,
                "can_create_product": False,
                "can_edit_product": False,
                "can_delete_product": False,
                "is_pim_manager": False,
                "is_brand_portal_user": False,
                "is_data_steward": False,
            }
        
        # Add PIM module information
        bootinfo["pim"]["module_info"] = {
            "app_name": "frappe_pim",
            "app_title": "Frappe PIM",
            "version": "0.2.0",
        }
        
        # Add enabled features based on installed doctypes
        enabled_features = []
        
        if frappe.db.exists("DocType", "Channel"):
            enabled_features.append("channels")
        
        if frappe.db.exists("DocType", "AI Approval Queue"):
            enabled_features.append("ai_enrichment")
        
        if frappe.db.exists("DocType", "Brand Portal User"):
            enabled_features.append("brand_portal")
        
        if frappe.db.exists("DocType", "Golden Record"):
            enabled_features.append("mdm")
        
        if frappe.db.exists("DocType", "Data Quality Policy"):
            enabled_features.append("data_quality")
        
        if frappe.db.exists("DocType", "GS1 Packaging Hierarchy"):
            enabled_features.append("gs1")
        
        bootinfo["pim"]["enabled_features"] = enabled_features
    
    except Exception as e:
        # Log error but don't break boot process
        frappe.log_error(
            message=f"Error in PIM boot_session: {str(e)}",
            title="PIM Boot Session Error"
        )
        # Ensure pim key exists even on error
        if "pim" not in bootinfo:
            bootinfo["pim"] = {
                "settings": {},
                "permissions": {},
                "module_info": {},
                "enabled_features": [],
            }

