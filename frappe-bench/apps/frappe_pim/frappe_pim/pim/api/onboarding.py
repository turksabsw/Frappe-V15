"""PIM Onboarding API Endpoints

This module provides API endpoints for the SaaS onboarding wizard.
All functions support both synchronous use and whitelisted API access.

Endpoints:
- start_onboarding: Start/resume onboarding for the current user
- get_onboarding_state: Get current onboarding state and progress
- save_step_data: Save form data for a specific step (partial save)
- apply_archetype_template: Apply an industry archetype template
- complete_onboarding: Advance through steps or complete onboarding
- get_available_archetypes: List available industry archetype templates
- skip_onboarding: Skip the onboarding wizard entirely
- reset_onboarding: Reset onboarding to initial state
- preview_archetype: Preview what an archetype template will create

Note: frappe imports are deferred to function level to allow module
import without Frappe being available (e.g., for testing/verification).
"""


def start_onboarding(user=None):
    """Start or resume onboarding for a user.

    Creates a new PIM Onboarding State document if one doesn't exist
    for the specified user, or returns the existing state.

    Args:
        user: User email. Defaults to current session user.

    Returns:
        dict: Onboarding state summary
            - user: User email
            - current_step: Current step in the wizard
            - is_completed: Whether onboarding is finished
            - is_skipped: Whether onboarding was skipped
            - progress_percent: Completion percentage (0-100)
            - selected_archetype: Chosen industry archetype (if any)
            - template_applied: Whether a template has been applied
            - started_at: When onboarding began
            - completed_at: When onboarding finished
            - completed_steps: List of completed step names
            - next_step: Next step to complete
            - previous_step: Previous step (for back navigation)
            - total_steps: Total number of steps
            - steps: Detailed step list with status

    Example:
        >>> state = start_onboarding()
        >>> print(f"Current step: {state['current_step']}")
    """
    import frappe
    from frappe import _

    if not user:
        user = frappe.session.user

    # Permission check
    if not frappe.has_permission("PIM Onboarding State", "read"):
        frappe.throw(_("Not permitted to access onboarding"), frappe.PermissionError)

    # Find existing state for this user
    existing = frappe.db.exists("PIM Onboarding State", {"user": user})

    if existing:
        doc = frappe.get_doc("PIM Onboarding State", existing)
    else:
        # Create a new onboarding state
        doc = frappe.new_doc("PIM Onboarding State")
        doc.user = user
        doc.current_step = "pending"
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

    # If still at pending, advance to company_info to start
    if doc.current_step == "pending":
        doc.advance_step()

    return doc.get_status_summary()


def get_onboarding_state(user=None):
    """Get the current onboarding state for a user.

    Returns the full onboarding state including progress, step data,
    and template application status.

    Args:
        user: User email. Defaults to current session user.

    Returns:
        dict: Onboarding state summary with all step details.
            Returns a 'not_started' state if no onboarding exists.

    Example:
        >>> state = get_onboarding_state()
        >>> if state['is_completed']:
        ...     print("Onboarding complete!")
        >>> else:
        ...     print(f"Progress: {state['progress_percent']}%")
    """
    import frappe
    from frappe import _

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "read"):
        frappe.throw(_("Not permitted to access onboarding"), frappe.PermissionError)

    existing = frappe.db.exists("PIM Onboarding State", {"user": user})

    if not existing:
        return {
            "user": user,
            "current_step": "not_started",
            "is_completed": False,
            "is_skipped": False,
            "progress_percent": 0,
            "selected_archetype": None,
            "template_applied": False,
            "started_at": None,
            "completed_at": None,
            "completed_steps": [],
            "next_step": None,
            "previous_step": None,
            "total_steps": 12,
            "steps": [],
        }

    doc = frappe.get_doc("PIM Onboarding State", existing)
    summary = doc.get_status_summary()

    # Include step data for the current step (useful for resuming forms)
    current_data = doc.get_step_data(doc.current_step)
    if current_data:
        summary["current_step_data"] = current_data

    return summary


def save_step_data(step, form_data, user=None, advance=False):
    """Save form data for a specific onboarding step.

    Allows partial saves (drafts) during a step. Optionally
    advances to the next step after saving.

    Args:
        step: The step name to save data for (e.g., "company_info",
            "industry_selection", "product_structure")
        form_data: JSON string or dict of form data collected during the step
        user: User email. Defaults to current session user.
        advance: If True, also advance to the next step after saving

    Returns:
        dict: Updated onboarding state summary

    Example:
        >>> result = save_step_data(
        ...     step="company_info",
        ...     form_data='{"company_name": "Acme Corp", "industry": "retail"}',
        ...     advance=True
        ... )
        >>> print(f"Now at step: {result['current_step']}")
    """
    import frappe
    from frappe import _
    import json

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "write"):
        frappe.throw(_("Not permitted to modify onboarding"), frappe.PermissionError)

    # Find onboarding state
    existing = frappe.db.exists("PIM Onboarding State", {"user": user})
    if not existing:
        frappe.throw(
            _("No onboarding state found for user {0}. Call start_onboarding first.").format(user),
            title=_("Not Found")
        )

    doc = frappe.get_doc("PIM Onboarding State", existing)

    # Parse form_data if it's a JSON string
    if isinstance(form_data, str):
        try:
            parsed_data = json.loads(form_data)
        except (json.JSONDecodeError, TypeError):
            frappe.throw(
                _("Invalid form_data: must be valid JSON"),
                title=_("Invalid Data")
            )
    else:
        parsed_data = form_data

    if not isinstance(parsed_data, dict):
        frappe.throw(
            _("form_data must be a JSON object (dict)"),
            title=_("Invalid Data")
        )

    # Save step data
    doc.save_step_data(step, parsed_data)

    # Optionally advance to next step
    if advance:
        doc.advance_step()

    return doc.get_status_summary()


def apply_archetype_template(archetype, user=None, dry_run=False):
    """Apply an industry archetype template to configure PIM.

    Loads the specified archetype template (and its base template if
    declared) and creates all configuration entities: attribute groups,
    attribute types, attributes, product types, product families, and
    categories.

    Args:
        archetype: Archetype identifier (e.g., "fashion", "industrial",
            "food", "base")
        user: User email. Defaults to current session user.
        dry_run: If True, validate and preview without creating records

    Returns:
        dict: Template application result
            - success: Whether application succeeded
            - archetype: The archetype that was applied
            - status: Application status (completed, partial, failed)
            - entities_created: Number of entities created
            - entities_skipped: Number of entities skipped (already exist)
            - entities_failed: Number of entities that failed
            - details: Per-section breakdown
            - errors: List of error messages
            - messages: List of informational messages

    Example:
        >>> result = apply_archetype_template("fashion")
        >>> if result['success']:
        ...     print(f"Created {result['entities_created']} entities")
    """
    import frappe
    from frappe import _

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "write"):
        frappe.throw(_("Not permitted to apply templates"), frappe.PermissionError)

    # Resolve onboarding state name for integration
    onboarding_state_name = None
    existing = frappe.db.exists("PIM Onboarding State", {"user": user})
    if existing:
        onboarding_state_name = existing

    # Apply via the template engine
    from frappe_pim.pim.services.template_engine import TemplateEngine

    try:
        template_result = TemplateEngine.apply_template(
            archetype_name=archetype,
            onboarding_state_name=onboarding_state_name if not dry_run else None,
            dry_run=dry_run,
        )
    except Exception as e:
        frappe.log_error(
            message=f"Template application failed for archetype '{archetype}': {str(e)}",
            title="PIM Onboarding Template Error"
        )
        return {
            "success": False,
            "archetype": archetype,
            "status": "failed",
            "entities_created": 0,
            "entities_skipped": 0,
            "entities_failed": 0,
            "details": {},
            "errors": [str(e)],
            "messages": [],
        }

    result_dict = template_result.to_dict()
    success = result_dict["status"] in ("completed", "partial")

    return {
        "success": success,
        "archetype": result_dict["archetype"],
        "status": result_dict["status"],
        "entities_created": result_dict["entities_created"],
        "entities_skipped": result_dict["entities_skipped"],
        "entities_failed": result_dict["entities_failed"],
        "details": result_dict["details"],
        "errors": result_dict["errors"],
        "messages": result_dict["messages"],
        "dry_run": dry_run,
    }


def complete_onboarding(user=None, form_data=None):
    """Advance the onboarding wizard to the next step, or complete it.

    If on the last actionable step, marks onboarding as completed.
    Saves form data for the current step if provided.

    Args:
        user: User email. Defaults to current session user.
        form_data: Optional JSON string or dict of form data for the
            current step before advancing.

    Returns:
        dict: Updated onboarding state summary

    Example:
        >>> result = complete_onboarding(
        ...     form_data='{"confirm": true}'
        ... )
        >>> if result['is_completed']:
        ...     print("Onboarding finished!")
    """
    import frappe
    from frappe import _
    import json

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "write"):
        frappe.throw(_("Not permitted to modify onboarding"), frappe.PermissionError)

    existing = frappe.db.exists("PIM Onboarding State", {"user": user})
    if not existing:
        frappe.throw(
            _("No onboarding state found for user {0}. Call start_onboarding first.").format(user),
            title=_("Not Found")
        )

    doc = frappe.get_doc("PIM Onboarding State", existing)

    if doc.is_completed:
        return doc.get_status_summary()

    # Parse form_data
    parsed_data = None
    if form_data:
        if isinstance(form_data, str):
            try:
                parsed_data = json.loads(form_data)
            except (json.JSONDecodeError, TypeError):
                frappe.throw(
                    _("Invalid form_data: must be valid JSON"),
                    title=_("Invalid Data")
                )
        else:
            parsed_data = form_data

    # Advance to next step (handles completion automatically)
    doc.advance_step(form_data=parsed_data)

    return doc.get_status_summary()


def get_available_archetypes():
    """Get list of available industry archetype templates.

    Scans the PIM fixtures directory for archetype template JSON files
    and returns metadata for each.

    Returns:
        dict: Available archetypes information
            - archetypes: List of archetype dicts, each containing:
                - archetype: Identifier (e.g., "fashion")
                - label: Human-readable name (e.g., "Fashion & Apparel")
                - description: Brief description
                - version: Template version
            - total: Total number of available archetypes

    Example:
        >>> result = get_available_archetypes()
        >>> for arch in result['archetypes']:
        ...     print(f"{arch['label']}: {arch['description']}")
    """
    import frappe
    from frappe import _

    if not frappe.has_permission("PIM Onboarding State", "read"):
        frappe.throw(_("Not permitted to view archetypes"), frappe.PermissionError)

    from frappe_pim.pim.services.template_engine import TemplateEngine

    archetypes = TemplateEngine.get_available_archetypes()

    # Remove internal file_path from response
    for arch in archetypes:
        arch.pop("file_path", None)

    return {
        "archetypes": archetypes,
        "total": len(archetypes),
    }


def skip_onboarding(user=None):
    """Skip the onboarding wizard entirely.

    Marks the onboarding as skipped so the user can configure
    PIM manually without the guided wizard.

    Args:
        user: User email. Defaults to current session user.

    Returns:
        dict: Updated onboarding state summary with is_skipped=True

    Example:
        >>> result = skip_onboarding()
        >>> assert result['is_skipped'] is True
    """
    import frappe
    from frappe import _

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "write"):
        frappe.throw(_("Not permitted to modify onboarding"), frappe.PermissionError)

    existing = frappe.db.exists("PIM Onboarding State", {"user": user})
    if not existing:
        frappe.throw(
            _("No onboarding state found for user {0}. Call start_onboarding first.").format(user),
            title=_("Not Found")
        )

    doc = frappe.get_doc("PIM Onboarding State", existing)
    doc.skip_onboarding()

    return doc.get_status_summary()


def reset_onboarding(user=None):
    """Reset onboarding to initial state.

    Clears all step data, template application, and resets progress
    to zero. Requires System Manager role.

    Args:
        user: User email. Defaults to current session user.

    Returns:
        dict: Reset onboarding state summary

    Example:
        >>> result = reset_onboarding()
        >>> assert result['current_step'] == 'pending'
        >>> assert result['progress_percent'] == 0
    """
    import frappe
    from frappe import _

    if not user:
        user = frappe.session.user

    if not frappe.has_permission("PIM Onboarding State", "write"):
        frappe.throw(_("Not permitted to reset onboarding"), frappe.PermissionError)

    existing = frappe.db.exists("PIM Onboarding State", {"user": user})
    if not existing:
        frappe.throw(
            _("No onboarding state found for user {0}").format(user),
            title=_("Not Found")
        )

    doc = frappe.get_doc("PIM Onboarding State", existing)
    doc.reset_onboarding()

    return doc.get_status_summary()


def preview_archetype(archetype):
    """Preview what an archetype template will create without applying it.

    Returns a summary of all entities that would be created, including
    counts and item keys per section.

    Args:
        archetype: Archetype identifier (e.g., "fashion", "industrial")

    Returns:
        dict: Preview information
            - archetype: Archetype identifier
            - label: Human-readable name
            - description: Brief description
            - version: Template version
            - extends: Base template name (if any)
            - sections: Per-section details with counts and item keys

    Example:
        >>> preview = preview_archetype("fashion")
        >>> print(f"Will create {preview['sections']['attributes']['count']} attributes")
    """
    import frappe
    from frappe import _

    if not frappe.has_permission("PIM Onboarding State", "read"):
        frappe.throw(_("Not permitted to preview archetypes"), frappe.PermissionError)

    from frappe_pim.pim.services.template_engine import TemplateEngine

    try:
        return TemplateEngine.preview_template(archetype)
    except FileNotFoundError:
        frappe.throw(
            _("Archetype template '{0}' not found").format(archetype),
            title=_("Template Not Found")
        )
    except ValueError as e:
        frappe.throw(
            _("Invalid template: {0}").format(str(e)),
            title=_("Template Error")
        )


# ============================================================================
# Whitelist Wrapper
# ============================================================================

def _wrap_for_whitelist():
    """Add @frappe.whitelist() decorators at runtime."""
    import frappe

    global start_onboarding, get_onboarding_state, save_step_data
    global apply_archetype_template, complete_onboarding, get_available_archetypes
    global skip_onboarding, reset_onboarding, preview_archetype

    start_onboarding = frappe.whitelist()(start_onboarding)
    get_onboarding_state = frappe.whitelist()(get_onboarding_state)
    save_step_data = frappe.whitelist()(save_step_data)
    apply_archetype_template = frappe.whitelist()(apply_archetype_template)
    complete_onboarding = frappe.whitelist()(complete_onboarding)
    get_available_archetypes = frappe.whitelist()(get_available_archetypes)
    skip_onboarding = frappe.whitelist()(skip_onboarding)
    reset_onboarding = frappe.whitelist()(reset_onboarding)
    preview_archetype = frappe.whitelist()(preview_archetype)


# Apply whitelist decorators if frappe is available
try:
    _wrap_for_whitelist()
except ImportError:
    pass  # Decorators will be added when module is used in Frappe context
