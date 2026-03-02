"""PIM Product API Endpoints

This module provides API endpoints for Product Master CRUD operations.
All functions support both synchronous use and whitelisted API access.

Endpoints:
- get_products: List products with filtering and pagination
- get_product_detail: Get full product details with attributes
- create_product: Create a new product
- update_product: Update an existing product
- delete_product: Delete a product

Note: frappe imports are deferred to function level to allow module
import without Frappe being available (e.g., for testing/verification).
"""

from datetime import datetime


def get_products(
    product_family=None,
    status=None,
    search=None,
    completeness_min=None,
    completeness_max=None,
    page=1,
    page_size=50,
    order_by="modified",
    order_dir="desc",
    fields=None
):
    """Get list of products with filtering and pagination.

    Args:
        product_family: Filter by Product Family name
        status: Filter by status (Draft, Active, Inactive, Archived)
        search: Search term for product_name, product_code, or short_description
        completeness_min: Minimum completeness score (0-100)
        completeness_max: Maximum completeness score (0-100)
        page: Page number (1-based, default: 1)
        page_size: Number of products per page (default: 50, max: 200)
        order_by: Field to order by (default: modified)
        order_dir: Order direction - asc or desc (default: desc)
        fields: JSON list of fields to return (optional)

    Returns:
        dict: Paginated product list with metadata
            - products: List of product records
            - total: Total count matching filters
            - page: Current page number
            - page_size: Items per page
            - total_pages: Total number of pages

    Example:
        >>> result = get_products(status="Active", page=1, page_size=20)
        >>> print(f"Found {result['total']} products")
    """
    import frappe
    from frappe import _
    import json

    # Permission check
    if not frappe.has_permission("Product Master", "read"):
        frappe.throw(_("Not permitted to read products"), frappe.PermissionError)

    # Validate and sanitize parameters
    page = max(1, int(page))
    page_size = min(200, max(1, int(page_size)))

    # Build filters
    filters = {}

    if product_family:
        filters["product_family"] = product_family

    if status:
        filters["status"] = status

    if completeness_min is not None:
        filters["completeness_score"] = [">=", float(completeness_min)]

    if completeness_max is not None:
        if "completeness_score" in filters:
            # Both min and max specified
            filters["completeness_score"] = [
                "between",
                [float(completeness_min or 0), float(completeness_max)]
            ]
        else:
            filters["completeness_score"] = ["<=", float(completeness_max)]

    # Handle search
    or_filters = None
    if search:
        search_term = f"%{search}%"
        or_filters = [
            ["product_name", "like", search_term],
            ["product_code", "like", search_term],
            ["short_description", "like", search_term]
        ]

    # Determine fields to return
    if fields:
        if isinstance(fields, str):
            fields = json.loads(fields)
    else:
        fields = [
            "name", "product_name", "product_code", "status",
            "short_description", "product_family", "completeness_score",
            "image", "creation", "modified"
        ]

    # Validate order_by field
    allowed_order_fields = [
        "name", "product_name", "product_code", "status",
        "completeness_score", "creation", "modified"
    ]
    if order_by not in allowed_order_fields:
        order_by = "modified"

    order_dir = "desc" if order_dir.lower() not in ["asc", "desc"] else order_dir.lower()

    # Get total count
    total = frappe.db.count("Product Master", filters=filters, or_filters=or_filters)

    # Calculate pagination
    start = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    # Get products
    products = frappe.get_all(
        "Product Master",
        filters=filters,
        or_filters=or_filters,
        fields=fields,
        order_by=f"{order_by} {order_dir}",
        start=start,
        page_length=page_size
    )

    return {
        "products": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


def get_product_detail(name, include_attributes=True, include_media=True, include_variants=False):
    """Get full product details including attributes and media.

    Args:
        name: Product Master name (document ID)
        include_attributes: Include EAV attribute values (default: True)
        include_media: Include media attachments (default: True)
        include_variants: Include linked Product Variants (default: False)

    Returns:
        dict: Complete product data with optional nested data

    Example:
        >>> product = get_product_detail("PROD-001", include_variants=True)
        >>> print(product["product_name"])
    """
    import frappe
    from frappe import _

    if not frappe.has_permission("Product Master", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    try:
        doc = frappe.get_doc("Product Master", name)
    except frappe.DoesNotExistError:
        frappe.throw(_("Product '{0}' not found").format(name), frappe.DoesNotExistError)

    # Build response
    product = {
        "name": doc.name,
        "product_name": doc.product_name,
        "product_code": doc.product_code,
        "status": doc.status,
        "short_description": doc.short_description,
        "long_description": doc.get("long_description"),
        "product_family": doc.product_family,
        "completeness_score": doc.completeness_score,
        "image": doc.get("image"),
        "creation": doc.creation.isoformat() if doc.creation else None,
        "modified": doc.modified.isoformat() if doc.modified else None,
        "owner": doc.owner,
        "modified_by": doc.modified_by
    }

    # Include EAV attributes
    if include_attributes:
        product["attributes"] = _get_product_attributes(doc)

    # Include media
    if include_media:
        product["media"] = _get_product_media_list(doc)

    # Include variants
    if include_variants:
        product["variants"] = _get_product_variants(name)

    return product


def create_product(
    product_name,
    product_code=None,
    product_family=None,
    status="Draft",
    short_description=None,
    long_description=None,
    attributes=None,
    image=None
):
    """Create a new product.

    Args:
        product_name: Display name for the product (required)
        product_code: Unique product code/SKU (auto-generated if not provided)
        product_family: Link to Product Family
        status: Initial status (default: Draft)
        short_description: Brief product description
        long_description: Full product description (HTML supported)
        attributes: JSON dict of attribute_code -> value mappings
        image: Primary product image URL/path

    Returns:
        dict: Created product data with name and key fields

    Example:
        >>> result = create_product(
        ...     product_name="Widget Pro",
        ...     product_family="Electronics",
        ...     attributes={"color": "Blue", "size": "Large"}
        ... )
        >>> print(result["name"])
    """
    import frappe
    from frappe import _
    import json

    if not frappe.has_permission("Product Master", "create"):
        frappe.throw(_("Not permitted to create products"), frappe.PermissionError)

    # Parse attributes if JSON string
    if attributes and isinstance(attributes, str):
        attributes = json.loads(attributes)

    # Prepare document data
    doc_data = {
        "doctype": "Product Master",
        "product_name": product_name,
        "status": status
    }

    if product_code:
        doc_data["product_code"] = product_code

    if product_family:
        # Validate product family exists
        if not frappe.db.exists("Product Family", product_family):
            frappe.throw(
                _("Product Family '{0}' does not exist").format(product_family),
                title=_("Invalid Product Family")
            )
        doc_data["product_family"] = product_family

    if short_description:
        doc_data["short_description"] = short_description

    if long_description:
        doc_data["long_description"] = long_description

    if image:
        doc_data["image"] = image

    # Create document
    try:
        doc = frappe.get_doc(doc_data)
        doc.insert()

        # Add attribute values if provided
        if attributes:
            _set_product_attributes(doc, attributes)
            doc.save()

        frappe.db.commit()

        return {
            "success": True,
            "name": doc.name,
            "product_name": doc.product_name,
            "product_code": doc.product_code,
            "status": doc.status,
            "product_family": doc.product_family,
            "completeness_score": doc.completeness_score
        }

    except frappe.DuplicateEntryError as e:
        frappe.throw(
            _("A product with this code already exists"),
            title=_("Duplicate Product Code")
        )
    except Exception as e:
        frappe.log_error(
            message=f"Product creation failed: {str(e)}",
            title="PIM Product API Error"
        )
        frappe.throw(
            _("Failed to create product: {0}").format(str(e)),
            title=_("Product Creation Failed")
        )


def update_product(
    name,
    product_name=None,
    product_code=None,
    product_family=None,
    status=None,
    short_description=None,
    long_description=None,
    attributes=None,
    image=None
):
    """Update an existing product.

    Only provided fields will be updated. Pass None to skip a field.

    Args:
        name: Product Master name (document ID) - required
        product_name: New display name
        product_code: New product code/SKU
        product_family: New Product Family link
        status: New status
        short_description: New short description
        long_description: New long description
        attributes: JSON dict of attribute_code -> value mappings to update
        image: New primary image URL/path

    Returns:
        dict: Updated product data

    Example:
        >>> result = update_product(
        ...     name="PROD-001",
        ...     status="Active",
        ...     attributes={"color": "Red"}
        ... )
    """
    import frappe
    from frappe import _
    import json

    if not frappe.has_permission("Product Master", "write"):
        frappe.throw(_("Not permitted to update products"), frappe.PermissionError)

    try:
        doc = frappe.get_doc("Product Master", name)
    except frappe.DoesNotExistError:
        frappe.throw(_("Product '{0}' not found").format(name), frappe.DoesNotExistError)

    # Parse attributes if JSON string
    if attributes and isinstance(attributes, str):
        attributes = json.loads(attributes)

    # Update fields if provided
    if product_name is not None:
        doc.product_name = product_name

    if product_code is not None:
        doc.product_code = product_code

    if product_family is not None:
        if product_family and not frappe.db.exists("Product Family", product_family):
            frappe.throw(
                _("Product Family '{0}' does not exist").format(product_family),
                title=_("Invalid Product Family")
            )
        doc.product_family = product_family

    if status is not None:
        doc.status = status

    if short_description is not None:
        doc.short_description = short_description

    if long_description is not None:
        doc.long_description = long_description

    if image is not None:
        doc.image = image

    # Update attributes if provided
    if attributes:
        _set_product_attributes(doc, attributes)

    try:
        doc.save()
        frappe.db.commit()

        return {
            "success": True,
            "name": doc.name,
            "product_name": doc.product_name,
            "product_code": doc.product_code,
            "status": doc.status,
            "product_family": doc.product_family,
            "completeness_score": doc.completeness_score,
            "modified": doc.modified.isoformat() if doc.modified else None
        }

    except frappe.DuplicateEntryError:
        frappe.throw(
            _("A product with this code already exists"),
            title=_("Duplicate Product Code")
        )
    except Exception as e:
        frappe.log_error(
            message=f"Product update failed for {name}: {str(e)}",
            title="PIM Product API Error"
        )
        frappe.throw(
            _("Failed to update product: {0}").format(str(e)),
            title=_("Product Update Failed")
        )


def delete_product(name, force=False):
    """Delete a product.

    Args:
        name: Product Master name (document ID)
        force: Force delete even if product has variants (default: False)

    Returns:
        dict: Deletion result

    Example:
        >>> result = delete_product("PROD-001")
        >>> print(result["message"])
    """
    import frappe
    from frappe import _

    if not frappe.has_permission("Product Master", "delete"):
        frappe.throw(_("Not permitted to delete products"), frappe.PermissionError)

    # Check if product exists
    if not frappe.db.exists("Product Master", name):
        frappe.throw(_("Product '{0}' not found").format(name), frappe.DoesNotExistError)

    # Check for linked variants
    variant_count = frappe.db.count("Product Variant", {"product_master": name})
    if variant_count > 0 and not force:
        frappe.throw(
            _("Cannot delete product with {0} linked variant(s). Use force=True to delete anyway.").format(variant_count),
            title=_("Product Has Variants")
        )

    try:
        # Delete variants first if force=True
        if variant_count > 0 and force:
            variants = frappe.get_all(
                "Product Variant",
                filters={"product_master": name},
                pluck="name"
            )
            for variant in variants:
                frappe.delete_doc("Product Variant", variant, ignore_permissions=True)

        # Delete the product
        frappe.delete_doc("Product Master", name)
        frappe.db.commit()

        return {
            "success": True,
            "message": _("Product '{0}' deleted successfully").format(name),
            "variants_deleted": variant_count if force else 0
        }

    except Exception as e:
        frappe.log_error(
            message=f"Product deletion failed for {name}: {str(e)}",
            title="PIM Product API Error"
        )
        frappe.throw(
            _("Failed to delete product: {0}").format(str(e)),
            title=_("Product Deletion Failed")
        )


def bulk_update_products(products, field, value):
    """Bulk update a field across multiple products.

    Args:
        products: JSON list of product names to update
        field: Field name to update
        value: New value to set

    Returns:
        dict: Update result with count of updated products

    Example:
        >>> result = bulk_update_products(
        ...     products=["PROD-001", "PROD-002"],
        ...     field="status",
        ...     value="Active"
        ... )
    """
    import frappe
    from frappe import _
    import json

    if not frappe.has_permission("Product Master", "write"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    if isinstance(products, str):
        products = json.loads(products)

    # Validate field is allowed for bulk update
    allowed_fields = ["status", "product_family"]
    if field not in allowed_fields:
        frappe.throw(
            _("Field '{0}' is not allowed for bulk update. Allowed: {1}").format(
                field, ", ".join(allowed_fields)
            ),
            title=_("Invalid Field")
        )

    updated = 0
    errors = []

    for product_name in products:
        try:
            if frappe.db.exists("Product Master", product_name):
                frappe.db.set_value("Product Master", product_name, field, value)
                updated += 1
            else:
                errors.append(f"{product_name}: not found")
        except Exception as e:
            errors.append(f"{product_name}: {str(e)}")
            frappe.log_error(
                f"Bulk update failed for {product_name}: {e}",
                "PIM Bulk Update"
            )

    frappe.db.commit()

    return {
        "success": len(errors) == 0,
        "updated": updated,
        "total": len(products),
        "errors": errors if errors else None
    }


def get_product_families():
    """Get list of Product Families for dropdowns/filters.

    Returns:
        list: Product Family records with name and label
    """
    import frappe
    from frappe import _

    if not frappe.has_permission("Product Family", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    return frappe.get_all(
        "Product Family",
        fields=["name", "family_name", "parent_product_family"],
        order_by="family_name asc"
    )


def get_product_statuses():
    """Get available product status options.

    Returns:
        list: Status options
    """
    return [
        {"value": "Draft", "label": "Draft"},
        {"value": "Active", "label": "Active"},
        {"value": "Inactive", "label": "Inactive"},
        {"value": "Archived", "label": "Archived"}
    ]


# ============================================================================
# Internal Helper Functions
# ============================================================================

def _get_product_attributes(doc):
    """Extract attributes from product document as dict.

    Args:
        doc: Product Master document

    Returns:
        dict: Attribute code -> value mapping with metadata
    """
    import frappe

    attributes = {}

    for attr_row in (doc.get("attribute_values") or []):
        attr_code = attr_row.get("attribute")
        if not attr_code:
            continue

        # Determine value from appropriate column
        value = None
        value_type = "text"

        if attr_row.get("value_text"):
            value = attr_row.value_text
            value_type = "text"
        elif attr_row.get("value_int") is not None:
            value = attr_row.value_int
            value_type = "integer"
        elif attr_row.get("value_float") is not None:
            value = attr_row.value_float
            value_type = "float"
        elif attr_row.get("value_boolean") is not None:
            value = attr_row.value_boolean
            value_type = "boolean"
        elif attr_row.get("value_date"):
            value = str(attr_row.value_date)
            value_type = "date"
        elif attr_row.get("value_link"):
            value = attr_row.value_link
            value_type = "link"

        # Get attribute metadata
        attr_meta = {}
        try:
            attr_meta = frappe.get_cached_value(
                "PIM Attribute", attr_code,
                ["attribute_name", "data_type", "attribute_group"],
                as_dict=True
            ) or {}
        except Exception:
            pass

        attributes[attr_code] = {
            "value": value,
            "value_type": value_type,
            "label": attr_meta.get("attribute_name", attr_code),
            "data_type": attr_meta.get("data_type"),
            "group": attr_meta.get("attribute_group")
        }

    return attributes


def _get_product_media_list(doc):
    """Extract media items from product document.

    Args:
        doc: Product Master document

    Returns:
        list: Media items
    """
    media_list = []

    # Primary image
    if doc.get("image"):
        media_list.append({
            "type": "image",
            "url": doc.image,
            "is_primary": True,
            "sort_order": 0
        })

    # Additional media from child table
    for idx, media in enumerate(doc.get("media") or [], start=1):
        media_list.append({
            "type": media.get("media_type", "image"),
            "url": media.get("file_url"),
            "title": media.get("title"),
            "is_primary": False,
            "sort_order": idx
        })

    return media_list


def _get_product_variants(product_master):
    """Get variants for a product.

    Args:
        product_master: Product Master name

    Returns:
        list: Variant records
    """
    import frappe

    return frappe.get_all(
        "Product Variant",
        filters={"product_master": product_master},
        fields=[
            "name", "variant_name", "variant_code", "status",
            "variant_attribute_1", "variant_value_1",
            "variant_attribute_2", "variant_value_2",
            "variant_attribute_3", "variant_value_3",
            "barcode", "price_override", "completeness_score", "image"
        ],
        order_by="variant_code asc"
    )


def _set_product_attributes(doc, attributes):
    """Set attribute values on a product document.

    Args:
        doc: Product Master document
        attributes: Dict of attribute_code -> value mappings
    """
    import frappe

    if not attributes:
        return

    # Get existing attribute rows indexed by attribute code
    existing = {}
    for row in (doc.get("attribute_values") or []):
        if row.attribute:
            existing[row.attribute] = row

    for attr_code, value in attributes.items():
        # Validate attribute exists
        if not frappe.db.exists("PIM Attribute", attr_code):
            continue

        # Get attribute data type
        data_type = frappe.db.get_value("PIM Attribute", attr_code, "data_type") or "Text"

        # Update existing or create new row
        if attr_code in existing:
            row = existing[attr_code]
        else:
            row = doc.append("attribute_values", {"attribute": attr_code})

        # Clear all value columns first
        row.value_text = None
        row.value_int = None
        row.value_float = None
        row.value_boolean = None
        row.value_date = None
        row.value_link = None

        # Set value in appropriate column based on data type
        if value is None:
            continue

        if data_type in ["Text", "Textarea", "HTML", "Select"]:
            row.value_text = str(value)
        elif data_type == "Integer":
            row.value_int = int(value)
        elif data_type in ["Float", "Currency", "Percent"]:
            row.value_float = float(value)
        elif data_type == "Boolean":
            row.value_boolean = bool(value)
        elif data_type == "Date":
            row.value_date = value
        elif data_type == "Link":
            row.value_link = str(value)
        else:
            # Default to text
            row.value_text = str(value)


# ============================================================================
# Whitelist Wrapper
# ============================================================================

def _wrap_for_whitelist():
    """Add @frappe.whitelist() decorators at runtime."""
    import frappe

    global get_products, get_product_detail, create_product, update_product
    global delete_product, bulk_update_products, get_product_families
    global get_product_statuses

    get_products = frappe.whitelist()(get_products)
    get_product_detail = frappe.whitelist()(get_product_detail)
    create_product = frappe.whitelist()(create_product)
    update_product = frappe.whitelist()(update_product)
    delete_product = frappe.whitelist()(delete_product)
    bulk_update_products = frappe.whitelist()(bulk_update_products)
    get_product_families = frappe.whitelist()(get_product_families)
    get_product_statuses = frappe.whitelist(allow_guest=True)(get_product_statuses)


# Apply whitelist decorators if frappe is available
try:
    _wrap_for_whitelist()
except ImportError:
    pass  # Decorators will be added when module is used in Frappe context
