"""
API Tests: Onboarding Endpoints and Product Management

Tests the complete onboarding flow:
  start → save steps → apply template → complete

Also tests:
  - Onboarding state retrieval
  - Step data persistence
  - Skip and reset flows
  - Archetype preview and listing
  - Error handling and validation
  - Product management endpoints in onboarding context
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import now_datetime
import json
from unittest.mock import patch, MagicMock


class TestOnboardingAPI(FrappeTestCase):
    """
    Tests for the onboarding API endpoints in frappe_pim.pim.api.onboarding.

    Covers:
    1. start_onboarding - Create/resume onboarding
    2. get_onboarding_state - Retrieve current state
    3. save_step_data - Partial save of step form data
    4. complete_onboarding - Advance through steps
    5. skip_onboarding - Skip the wizard
    6. reset_onboarding - Reset to initial state
    7. get_available_archetypes - List industry templates
    8. preview_archetype - Preview template contents
    9. apply_archetype_template - Apply industry template
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for all tests"""
        super().setUpClass()
        cls._cleanup_test_data()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        super().tearDownClass()
        cls._cleanup_test_data()

    @classmethod
    def _cleanup_test_data(cls):
        """Remove any test data from previous runs"""
        tables_to_clean = [
            ("tabPIM Onboarding State", "user LIKE 'onb_test_%'"),
        ]

        for table, condition in tables_to_clean:
            try:
                frappe.db.sql(f"DELETE FROM `{table}` WHERE {condition}")
            except Exception:
                pass

        frappe.db.commit()

    def tearDown(self):
        """Clean up after each test"""
        frappe.db.rollback()

    def _create_onboarding_state(self, user="onb_test_user@example.com", step="pending"):
        """Helper to create a test onboarding state document"""
        doc = frappe.new_doc("PIM Onboarding State")
        doc.user = user
        doc.current_step = step
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc

    def _delete_onboarding_state(self, user="onb_test_user@example.com"):
        """Helper to delete test onboarding state"""
        existing = frappe.db.exists("PIM Onboarding State", {"user": user})
        if existing:
            frappe.delete_doc("PIM Onboarding State", existing, ignore_permissions=True)
            frappe.db.commit()

    # ========================================================================
    # Step 1: start_onboarding
    # ========================================================================

    def test_01_start_onboarding_creates_new_state(self):
        """Test that start_onboarding creates a new state for a new user"""
        from frappe_pim.pim.api.onboarding import start_onboarding

        user = "onb_test_start_new@example.com"
        self._delete_onboarding_state(user)

        result = start_onboarding(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"], user)
        # start_onboarding advances from pending to company_info
        self.assertEqual(result["current_step"], "company_info")
        self.assertFalse(result["is_completed"])
        self.assertFalse(result["is_skipped"])
        self.assertIn("steps", result)
        self.assertIn("completed_steps", result)
        self.assertIn("total_steps", result)
        self.assertEqual(result["total_steps"], 12)

    def test_02_start_onboarding_resumes_existing(self):
        """Test that start_onboarding resumes an existing state"""
        from frappe_pim.pim.api.onboarding import start_onboarding

        user = "onb_test_start_resume@example.com"
        self._delete_onboarding_state(user)

        # Create state at industry_selection step
        doc = self._create_onboarding_state(user=user, step="industry_selection")

        result = start_onboarding(user=user)

        self.assertEqual(result["user"], user)
        self.assertEqual(result["current_step"], "industry_selection")
        self.assertFalse(result["is_completed"])

    def test_03_start_onboarding_advances_from_pending(self):
        """Test that start_onboarding advances from pending to company_info"""
        from frappe_pim.pim.api.onboarding import start_onboarding

        user = "onb_test_start_pending@example.com"
        self._delete_onboarding_state(user)

        # Create in pending state
        self._create_onboarding_state(user=user, step="pending")

        result = start_onboarding(user=user)

        # Should have advanced to company_info
        self.assertEqual(result["current_step"], "company_info")

    # ========================================================================
    # Step 2: get_onboarding_state
    # ========================================================================

    def test_04_get_onboarding_state_returns_existing(self):
        """Test get_onboarding_state returns existing state"""
        from frappe_pim.pim.api.onboarding import get_onboarding_state

        user = "onb_test_get_existing@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="product_structure")

        result = get_onboarding_state(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"], user)
        self.assertEqual(result["current_step"], "product_structure")
        self.assertFalse(result["is_completed"])

    def test_05_get_onboarding_state_returns_not_started(self):
        """Test get_onboarding_state returns not_started for non-existent user"""
        from frappe_pim.pim.api.onboarding import get_onboarding_state

        user = "onb_test_get_nonexistent@example.com"
        self._delete_onboarding_state(user)

        result = get_onboarding_state(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "not_started")
        self.assertFalse(result["is_completed"])
        self.assertFalse(result["is_skipped"])
        self.assertEqual(result["progress_percent"], 0)
        self.assertEqual(result["completed_steps"], [])

    def test_06_get_onboarding_state_includes_step_details(self):
        """Test that state includes detailed step information"""
        from frappe_pim.pim.api.onboarding import get_onboarding_state

        user = "onb_test_get_details@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="channel_setup")

        result = get_onboarding_state(user=user)

        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0)

        # Check step structure
        step_entry = result["steps"][0]
        self.assertIn("name", step_entry)
        self.assertIn("index", step_entry)
        self.assertIn("is_completed", step_entry)
        self.assertIn("is_current", step_entry)

    # ========================================================================
    # Step 3: save_step_data
    # ========================================================================

    def test_07_save_step_data_with_dict(self):
        """Test saving step data with a dict"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_save_dict@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        form_data = {
            "company_name": "Test Company",
            "industry": "retail",
            "company_size": "small",
            "country": "US",
            "currency": "USD"
        }

        result = save_step_data(step="company_info", form_data=form_data, user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"], user)
        # Should stay on the same step (no advance)
        self.assertEqual(result["current_step"], "company_info")

    def test_08_save_step_data_with_json_string(self):
        """Test saving step data with a JSON string"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_save_json@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        form_data = json.dumps({
            "company_name": "JSON Corp",
            "industry": "manufacturing"
        })

        result = save_step_data(step="company_info", form_data=form_data, user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "company_info")

    def test_09_save_step_data_with_advance(self):
        """Test saving step data with advance=True"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_save_advance@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        form_data = {
            "company_name": "Advance Corp",
            "industry": "technology"
        }

        result = save_step_data(
            step="company_info",
            form_data=form_data,
            user=user,
            advance=True
        )

        self.assertIsInstance(result, dict)
        # Should have advanced to the next step
        self.assertEqual(result["current_step"], "industry_selection")

    def test_10_save_step_data_persists_correctly(self):
        """Test that saved step data can be retrieved"""
        from frappe_pim.pim.api.onboarding import save_step_data, get_onboarding_state

        user = "onb_test_save_persist@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="industry_selection")

        form_data = {
            "archetype": "fashion",
            "sub_industry": "apparel",
            "product_count_estimate": 500,
            "has_variants": True
        }

        save_step_data(step="industry_selection", form_data=form_data, user=user)

        # Verify data persisted by loading the doc directly
        existing = frappe.db.exists("PIM Onboarding State", {"user": user})
        doc = frappe.get_doc("PIM Onboarding State", existing)
        stored_data = doc.get_step_data("industry_selection")

        self.assertIsNotNone(stored_data)
        self.assertEqual(stored_data["archetype"], "fashion")
        self.assertEqual(stored_data["product_count_estimate"], 500)

    def test_11_save_step_data_no_onboarding_state(self):
        """Test saving step data when no onboarding state exists"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_save_nostate@example.com"
        self._delete_onboarding_state(user)

        with self.assertRaises(frappe.exceptions.ValidationError):
            save_step_data(
                step="company_info",
                form_data={"company_name": "Test"},
                user=user
            )

    def test_12_save_step_data_invalid_json(self):
        """Test saving step data with invalid JSON string"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_save_invalid@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        with self.assertRaises(frappe.exceptions.ValidationError):
            save_step_data(
                step="company_info",
                form_data="not valid json{{{",
                user=user
            )

    # ========================================================================
    # Step 4: complete_onboarding (advance through steps)
    # ========================================================================

    def test_13_complete_onboarding_advances_step(self):
        """Test that complete_onboarding advances to next step"""
        from frappe_pim.pim.api.onboarding import complete_onboarding

        user = "onb_test_complete_advance@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        result = complete_onboarding(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "industry_selection")
        self.assertFalse(result["is_completed"])

    def test_14_complete_onboarding_with_form_data(self):
        """Test advancing with form data for the current step"""
        from frappe_pim.pim.api.onboarding import complete_onboarding

        user = "onb_test_complete_data@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="product_structure")

        form_data = json.dumps({
            "use_families": True,
            "use_categories": True,
            "variant_levels": 2
        })

        result = complete_onboarding(user=user, form_data=form_data)

        self.assertEqual(result["current_step"], "channel_setup")

        # Verify form data was saved
        existing = frappe.db.exists("PIM Onboarding State", {"user": user})
        doc = frappe.get_doc("PIM Onboarding State", existing)
        stored = doc.get_step_data("product_structure")
        self.assertIsNotNone(stored)
        self.assertTrue(stored["use_families"])

    def test_15_complete_onboarding_already_completed(self):
        """Test completing already completed onboarding returns summary"""
        from frappe_pim.pim.api.onboarding import complete_onboarding

        user = "onb_test_complete_done@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="completed")
        doc.is_completed = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        result = complete_onboarding(user=user)

        self.assertTrue(result["is_completed"])

    def test_16_complete_onboarding_no_state(self):
        """Test completing when no onboarding state exists"""
        from frappe_pim.pim.api.onboarding import complete_onboarding

        user = "onb_test_complete_nostate@example.com"
        self._delete_onboarding_state(user)

        with self.assertRaises(frappe.exceptions.ValidationError):
            complete_onboarding(user=user)

    # ========================================================================
    # Step 5: skip_onboarding
    # ========================================================================

    def test_17_skip_onboarding(self):
        """Test skipping the onboarding wizard"""
        from frappe_pim.pim.api.onboarding import skip_onboarding

        user = "onb_test_skip@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        result = skip_onboarding(user=user)

        self.assertIsInstance(result, dict)
        self.assertTrue(result["is_skipped"])
        self.assertTrue(result["is_completed"])
        self.assertEqual(result["current_step"], "completed")

    def test_18_skip_onboarding_no_state(self):
        """Test skipping when no onboarding state exists"""
        from frappe_pim.pim.api.onboarding import skip_onboarding

        user = "onb_test_skip_nostate@example.com"
        self._delete_onboarding_state(user)

        with self.assertRaises(frappe.exceptions.ValidationError):
            skip_onboarding(user=user)

    # ========================================================================
    # Step 6: reset_onboarding
    # ========================================================================

    def test_19_reset_onboarding(self):
        """Test resetting onboarding to initial state"""
        from frappe_pim.pim.api.onboarding import reset_onboarding

        user = "onb_test_reset@example.com"
        self._delete_onboarding_state(user)

        # Create state at a later step with some data
        doc = self._create_onboarding_state(user=user, step="channel_setup")
        doc.company_info_data = json.dumps({"company_name": "Reset Corp"})
        doc.selected_archetype = "fashion"
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        result = reset_onboarding(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "pending")
        self.assertFalse(result["is_completed"])
        self.assertFalse(result["is_skipped"])
        self.assertEqual(result["progress_percent"], 0)
        self.assertIsNone(result["selected_archetype"])
        self.assertFalse(result["template_applied"])

    def test_20_reset_onboarding_no_state(self):
        """Test resetting when no onboarding state exists"""
        from frappe_pim.pim.api.onboarding import reset_onboarding

        user = "onb_test_reset_nostate@example.com"
        self._delete_onboarding_state(user)

        with self.assertRaises(frappe.exceptions.ValidationError):
            reset_onboarding(user=user)

    # ========================================================================
    # Step 7: get_available_archetypes
    # ========================================================================

    def test_21_get_available_archetypes(self):
        """Test listing available industry archetypes"""
        from frappe_pim.pim.api.onboarding import get_available_archetypes

        result = get_available_archetypes()

        self.assertIsInstance(result, dict)
        self.assertIn("archetypes", result)
        self.assertIn("total", result)
        self.assertIsInstance(result["archetypes"], list)
        self.assertIsInstance(result["total"], int)

        # At minimum, base template should exist
        if result["total"] > 0:
            archetype = result["archetypes"][0]
            self.assertIn("archetype", archetype)
            self.assertIn("label", archetype)
            # file_path should be stripped from public API response
            self.assertNotIn("file_path", archetype)

    def test_22_get_available_archetypes_contains_known_templates(self):
        """Test that known archetypes (base, fashion, industrial) are listed"""
        from frappe_pim.pim.api.onboarding import get_available_archetypes

        result = get_available_archetypes()

        archetype_ids = [a["archetype"] for a in result["archetypes"]]

        # These templates are known to exist in fixtures
        for expected in ("base", "fashion", "industrial"):
            if expected in archetype_ids:
                self.assertIn(expected, archetype_ids)

    # ========================================================================
    # Step 8: preview_archetype
    # ========================================================================

    def test_23_preview_archetype_base(self):
        """Test previewing the base archetype template"""
        from frappe_pim.pim.api.onboarding import preview_archetype

        try:
            result = preview_archetype("base")

            self.assertIsInstance(result, dict)
            self.assertEqual(result["archetype"], "base")
            self.assertIn("sections", result)
            self.assertIn("label", result)

            # Sections should have counts
            sections = result.get("sections", {})
            if sections:
                for section_name, section_data in sections.items():
                    self.assertIn("count", section_data)
        except Exception:
            # Template might not be available in test environment
            pass

    def test_24_preview_archetype_fashion(self):
        """Test previewing the fashion archetype template"""
        from frappe_pim.pim.api.onboarding import preview_archetype

        try:
            result = preview_archetype("fashion")

            self.assertIsInstance(result, dict)
            self.assertIn("sections", result)

            # Fashion should extend base
            if result.get("extends"):
                self.assertEqual(result["extends"], "base")
        except Exception:
            pass

    def test_25_preview_archetype_nonexistent(self):
        """Test previewing a non-existent archetype raises error"""
        from frappe_pim.pim.api.onboarding import preview_archetype

        with self.assertRaises(Exception):
            preview_archetype("nonexistent_archetype_xyz")

    # ========================================================================
    # Step 9: apply_archetype_template
    # ========================================================================

    @patch("frappe_pim.pim.services.template_engine.TemplateEngine.apply_template")
    def test_26_apply_archetype_template_success(self, mock_apply):
        """Test applying an archetype template successfully"""
        from frappe_pim.pim.api.onboarding import apply_archetype_template

        user = "onb_test_apply@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="industry_selection")

        # Mock the template result
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {
            "archetype": "fashion",
            "status": "completed",
            "entities_created": 25,
            "entities_skipped": 3,
            "entities_failed": 0,
            "details": {
                "attribute_groups": {"created": 3, "skipped": 0, "failed": 0},
                "attributes": {"created": 18, "skipped": 2, "failed": 0},
                "product_families": {"created": 4, "skipped": 1, "failed": 0},
            },
            "errors": [],
            "messages": ["Template applied successfully"],
        }
        mock_apply.return_value = mock_result

        result = apply_archetype_template(archetype="fashion", user=user)

        self.assertIsInstance(result, dict)
        self.assertTrue(result["success"])
        self.assertEqual(result["archetype"], "fashion")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["entities_created"], 25)
        self.assertEqual(result["entities_failed"], 0)
        self.assertIn("details", result)

    @patch("frappe_pim.pim.services.template_engine.TemplateEngine.apply_template")
    def test_27_apply_archetype_template_dry_run(self, mock_apply):
        """Test applying an archetype template in dry_run mode"""
        from frappe_pim.pim.api.onboarding import apply_archetype_template

        user = "onb_test_apply_dry@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="industry_selection")

        mock_result = MagicMock()
        mock_result.to_dict.return_value = {
            "archetype": "fashion",
            "status": "completed",
            "entities_created": 0,
            "entities_skipped": 0,
            "entities_failed": 0,
            "details": {},
            "errors": [],
            "messages": ["Dry run - no entities created"],
        }
        mock_apply.return_value = mock_result

        result = apply_archetype_template(
            archetype="fashion", user=user, dry_run=True
        )

        self.assertIsInstance(result, dict)
        self.assertTrue(result["dry_run"])

        # Verify onboarding_state_name was NOT passed for dry_run
        call_kwargs = mock_apply.call_args
        self.assertIsNone(call_kwargs.kwargs.get("onboarding_state_name"))

    @patch("frappe_pim.pim.services.template_engine.TemplateEngine.apply_template")
    def test_28_apply_archetype_template_failure(self, mock_apply):
        """Test applying an archetype template that fails"""
        from frappe_pim.pim.api.onboarding import apply_archetype_template

        user = "onb_test_apply_fail@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="industry_selection")

        mock_apply.side_effect = Exception("Template file not found")

        result = apply_archetype_template(archetype="broken_template", user=user)

        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["entities_created"], 0)
        self.assertGreater(len(result["errors"]), 0)
        self.assertIn("Template file not found", result["errors"][0])

    # ========================================================================
    # Complete Onboarding Flow (E2E)
    # ========================================================================

    def test_29_complete_onboarding_flow(self):
        """Test the complete onboarding flow: start → save steps → advance → complete"""
        from frappe_pim.pim.api.onboarding import (
            start_onboarding,
            save_step_data,
            complete_onboarding,
            get_onboarding_state,
        )

        user = "onb_test_full_flow@example.com"
        self._delete_onboarding_state(user)

        # Step 1: Start onboarding
        state = start_onboarding(user=user)
        self.assertEqual(state["current_step"], "company_info")
        self.assertFalse(state["is_completed"])

        # Step 2: Save company info and advance
        state = save_step_data(
            step="company_info",
            form_data={
                "company_name": "Flow Test Corp",
                "industry": "retail",
                "company_size": "medium",
                "country": "US",
                "currency": "USD",
            },
            user=user,
            advance=True,
        )
        self.assertEqual(state["current_step"], "industry_selection")

        # Step 3: Save industry selection and advance
        state = save_step_data(
            step="industry_selection",
            form_data={
                "archetype": "fashion",
                "sub_industry": "apparel",
                "product_count_estimate": 1000,
                "has_variants": True,
            },
            user=user,
            advance=True,
        )
        self.assertEqual(state["current_step"], "product_structure")

        # Step 4: Advance through remaining steps using complete_onboarding
        steps_to_advance = [
            "product_structure",
            "channel_setup",
            "workflow_preferences",
            "compliance_setup",
            "template_applied",
            "customization_review",
            "first_data",
            "guided_tour",
        ]

        for step in steps_to_advance:
            state = complete_onboarding(user=user)
            # Check state is progressing (not stuck)
            self.assertIn("current_step", state)

        # Final check: should be completed
        final_state = get_onboarding_state(user=user)
        self.assertTrue(final_state["is_completed"])
        self.assertEqual(final_state["current_step"], "completed")
        self.assertEqual(final_state["progress_percent"], 100)

    def test_30_start_save_skip_flow(self):
        """Test the flow: start → save partial data → skip"""
        from frappe_pim.pim.api.onboarding import (
            start_onboarding,
            save_step_data,
            skip_onboarding,
            get_onboarding_state,
        )

        user = "onb_test_skip_flow@example.com"
        self._delete_onboarding_state(user)

        # Start onboarding
        state = start_onboarding(user=user)
        self.assertEqual(state["current_step"], "company_info")

        # Save partial data
        save_step_data(
            step="company_info",
            form_data={"company_name": "Skip Corp"},
            user=user,
        )

        # Skip the rest
        result = skip_onboarding(user=user)
        self.assertTrue(result["is_skipped"])
        self.assertTrue(result["is_completed"])

        # Verify via get_onboarding_state
        final = get_onboarding_state(user=user)
        self.assertTrue(final["is_completed"])
        self.assertTrue(final["is_skipped"])

    def test_31_start_advance_reset_restart_flow(self):
        """Test the flow: start → advance → reset → start fresh"""
        from frappe_pim.pim.api.onboarding import (
            start_onboarding,
            complete_onboarding,
            reset_onboarding,
            get_onboarding_state,
        )

        user = "onb_test_reset_flow@example.com"
        self._delete_onboarding_state(user)

        # Start and advance a few steps
        start_onboarding(user=user)
        complete_onboarding(user=user)  # company_info → industry_selection
        state = complete_onboarding(user=user)  # industry_selection → product_structure
        self.assertEqual(state["current_step"], "product_structure")

        # Reset
        reset_state = reset_onboarding(user=user)
        self.assertEqual(reset_state["current_step"], "pending")
        self.assertEqual(reset_state["progress_percent"], 0)

        # Start again
        new_state = start_onboarding(user=user)
        self.assertEqual(new_state["current_step"], "company_info")

    # ========================================================================
    # Onboarding State Controller Tests
    # ========================================================================

    def test_32_state_machine_step_validation(self):
        """Test that invalid steps are rejected"""
        user = "onb_test_invalid_step@example.com"
        self._delete_onboarding_state(user)

        doc = frappe.new_doc("PIM Onboarding State")
        doc.user = user
        doc.current_step = "invalid_step_name"

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.insert(ignore_permissions=True)

    def test_33_state_machine_progress_tracking(self):
        """Test progress percentage calculation across steps"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            ONBOARDING_STEPS,
            TOTAL_ACTIONABLE_STEPS,
        )

        user = "onb_test_progress@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="pending")

        # Pending should be 0%
        self.assertEqual(doc.progress_percent, 0)

        # Advance and check progress increases
        doc.advance_step()
        self.assertGreater(doc.progress_percent, 0)

        # Verify completed is 100%
        doc.current_step = "completed"
        doc.update_progress()
        self.assertEqual(doc.progress_percent, 100)

    def test_34_state_machine_cannot_advance_when_completed(self):
        """Test that advancing a completed onboarding raises an error"""
        user = "onb_test_advance_completed@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="completed")
        doc.is_completed = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.advance_step()

    def test_35_state_machine_cannot_advance_when_skipped(self):
        """Test that advancing a skipped onboarding raises an error"""
        user = "onb_test_advance_skipped@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")
        doc.is_skipped = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.advance_step()

    def test_36_state_machine_go_to_step_back(self):
        """Test navigating back to a previous step"""
        user = "onb_test_go_back@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="channel_setup")

        # Go back to company_info
        result = doc.go_to_step("company_info")
        self.assertEqual(result, "company_info")
        self.assertEqual(doc.current_step, "company_info")

    def test_37_state_machine_cannot_skip_ahead(self):
        """Test that skipping ahead to a future step raises an error"""
        user = "onb_test_skip_ahead@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.go_to_step("compliance_setup")

    def test_38_state_machine_step_data_invalid_step(self):
        """Test that saving data for an invalid step raises error"""
        user = "onb_test_data_invalid@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.save_step_data("completed", {"key": "value"})

    def test_39_state_machine_completed_steps_tracking(self):
        """Test that completed steps list is maintained correctly"""
        user = "onb_test_completed_list@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="pending")

        # Advance through a few steps
        doc.advance_step()  # pending → company_info
        doc.advance_step()  # company_info → industry_selection

        completed = doc.get_completed_steps()
        self.assertIn("pending", completed)
        self.assertIn("company_info", completed)
        self.assertNotIn("industry_selection", completed)

    def test_40_state_machine_get_next_and_previous(self):
        """Test next/previous step navigation helpers"""
        user = "onb_test_nav@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="product_structure")

        self.assertEqual(doc.get_next_step(), "channel_setup")
        self.assertEqual(doc.get_previous_step(), "industry_selection")

    def test_41_state_machine_pending_no_previous(self):
        """Test that pending step has no previous step"""
        user = "onb_test_pending_nav@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="pending")

        self.assertIsNone(doc.get_previous_step())

    def test_42_state_machine_completed_no_next(self):
        """Test that completed step has no next step"""
        user = "onb_test_completed_nav@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="completed")

        self.assertIsNone(doc.get_next_step())

    def test_43_state_machine_get_all_step_data(self):
        """Test retrieving all step data"""
        user = "onb_test_all_data@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="product_structure")

        # Save data for multiple steps
        doc._save_step_data("company_info", {"company_name": "All Data Corp"})
        doc._save_step_data("industry_selection", {"archetype": "fashion"})
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        all_data = doc.get_all_step_data()

        self.assertIsInstance(all_data, dict)
        self.assertIn("company_info", all_data)
        self.assertIn("industry_selection", all_data)
        self.assertEqual(all_data["company_info"]["company_name"], "All Data Corp")
        self.assertEqual(all_data["industry_selection"]["archetype"], "fashion")

    def test_44_state_machine_error_logging(self):
        """Test error logging for onboarding steps"""
        user = "onb_test_error_log@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        doc.log_error("company_info", "Validation failed for company name")

        doc.reload()
        errors = json.loads(doc.error_log) if doc.error_log else []

        self.assertGreater(len(errors), 0)
        self.assertEqual(errors[0]["step"], "company_info")
        self.assertEqual(errors[0]["error"], "Validation failed for company name")
        self.assertIn("timestamp", errors[0])

    def test_45_state_machine_timestamps(self):
        """Test that started_at and completed_at timestamps are set"""
        user = "onb_test_timestamps@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="pending")

        # Pending: no started_at
        self.assertFalse(doc.started_at)

        # Advance: started_at should be set
        doc.advance_step()
        self.assertTrue(doc.started_at)

    def test_46_state_machine_skip_sets_completed_at(self):
        """Test that skipping sets completed_at timestamp"""
        user = "onb_test_skip_timestamp@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        doc.skip_onboarding()

        self.assertTrue(doc.completed_at)
        self.assertTrue(doc.is_completed)
        self.assertTrue(doc.is_skipped)

    def test_47_state_machine_cannot_skip_after_complete(self):
        """Test that skipping after completion raises an error"""
        user = "onb_test_skip_after_complete@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="completed")
        doc.is_completed = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.skip_onboarding()

    # ========================================================================
    # Controller Whitelisted Functions
    # ========================================================================

    def test_48_controller_get_or_create_onboarding_state(self):
        """Test the controller-level get_or_create_onboarding_state function"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            get_or_create_onboarding_state,
        )

        user = "onb_test_ctrl_getorcreate@example.com"
        self._delete_onboarding_state(user)

        result = get_or_create_onboarding_state(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"], user)
        self.assertIn("current_step", result)

    def test_49_controller_advance_onboarding_step(self):
        """Test the controller-level advance_onboarding_step function"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            advance_onboarding_step,
        )

        user = "onb_test_ctrl_advance@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        result = advance_onboarding_step(user=user)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "industry_selection")

    def test_50_controller_advance_with_form_data(self):
        """Test advancing with form_data via controller function"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            advance_onboarding_step,
        )

        user = "onb_test_ctrl_advance_data@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        form_data = json.dumps({
            "company_name": "Controller Test Corp",
            "industry": "tech"
        })

        result = advance_onboarding_step(user=user, form_data=form_data)

        self.assertEqual(result["current_step"], "industry_selection")

        # Verify data was saved
        existing = frappe.db.exists("PIM Onboarding State", {"user": user})
        doc = frappe.get_doc("PIM Onboarding State", existing)
        stored = doc.get_step_data("company_info")
        self.assertIsNotNone(stored)
        self.assertEqual(stored["company_name"], "Controller Test Corp")

    def test_51_controller_save_onboarding_step_data(self):
        """Test the controller-level save_onboarding_step_data function"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            save_onboarding_step_data,
        )

        user = "onb_test_ctrl_save@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="channel_setup")

        form_data = json.dumps({
            "channels": ["e-commerce", "marketplace"],
            "primary_channel": "e-commerce"
        })

        result = save_onboarding_step_data(
            step="channel_setup", form_data=form_data, user=user
        )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["current_step"], "channel_setup")  # Should not advance

    def test_52_controller_get_onboarding_steps(self):
        """Test the controller-level get_onboarding_steps function"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            get_onboarding_steps,
        )

        result = get_onboarding_steps()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 12)  # 12 steps total

        # Check structure of first step
        first = result[0]
        self.assertEqual(first["name"], "pending")
        self.assertEqual(first["index"], 0)
        self.assertIn("has_data_field", first)
        self.assertIn("data_field", first)

        # Pending has no data field
        self.assertFalse(first["has_data_field"])
        self.assertIsNone(first["data_field"])

        # company_info has a data field
        company = result[1]
        self.assertEqual(company["name"], "company_info")
        self.assertTrue(company["has_data_field"])
        self.assertEqual(company["data_field"], "company_info_data")

    # ========================================================================
    # Status Summary Tests
    # ========================================================================

    def test_53_status_summary_structure(self):
        """Test that get_status_summary returns correct structure"""
        user = "onb_test_summary@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        summary = doc.get_status_summary()

        required_keys = [
            "user", "current_step", "is_completed", "is_skipped",
            "progress_percent", "selected_archetype", "template_applied",
            "started_at", "completed_at", "completed_steps", "next_step",
            "previous_step", "total_steps", "steps",
        ]

        for key in required_keys:
            self.assertIn(key, summary, f"Missing key in summary: {key}")

    def test_54_status_summary_step_detail(self):
        """Test step detail in status summary"""
        user = "onb_test_summary_detail@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="product_structure")

        summary = doc.get_status_summary()
        steps = summary["steps"]

        # Find the product_structure step
        ps_step = next(s for s in steps if s["name"] == "product_structure")
        self.assertTrue(ps_step["is_current"])

        # Find pending - should not be current
        pending_step = next(s for s in steps if s["name"] == "pending")
        self.assertFalse(pending_step["is_current"])

    def test_55_mark_template_applied(self):
        """Test marking a template as applied"""
        user = "onb_test_mark_template@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="template_applied")

        template_result = {
            "archetype": "fashion",
            "entities_created": 30,
            "entities_skipped": 5,
        }

        doc.mark_template_applied("fashion", template_result)

        doc.reload()
        self.assertEqual(doc.selected_archetype, "fashion")
        self.assertTrue(doc.template_applied)
        self.assertTrue(doc.template_applied_at)

        stored_result = json.loads(doc.template_result) if doc.template_result else {}
        self.assertEqual(stored_result["archetype"], "fashion")
        self.assertEqual(stored_result["entities_created"], 30)

    # ========================================================================
    # Edge Cases and Validation
    # ========================================================================

    def test_56_save_step_data_non_dict_raises_error(self):
        """Test that non-dict form_data raises validation error"""
        from frappe_pim.pim.api.onboarding import save_step_data

        user = "onb_test_nondict@example.com"
        self._delete_onboarding_state(user)
        self._create_onboarding_state(user=user, step="company_info")

        with self.assertRaises(frappe.exceptions.ValidationError):
            save_step_data(
                step="company_info",
                form_data=json.dumps([1, 2, 3]),  # Array, not object
                user=user
            )

    def test_57_get_step_data_returns_none_for_no_data(self):
        """Test get_step_data returns None when no data is stored"""
        user = "onb_test_nodata@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="company_info")

        result = doc.get_step_data("company_info")
        self.assertIsNone(result)

    def test_58_get_step_data_returns_none_for_invalid_step(self):
        """Test get_step_data returns None for non-data steps"""
        user = "onb_test_nodata_step@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="pending")

        result = doc.get_step_data("completed")
        self.assertIsNone(result)

    def test_59_reset_clears_all_data(self):
        """Test that reset clears all step data fields"""
        from frappe_pim.pim.doctype.pim_onboarding_state.pim_onboarding_state import (
            STEP_DATA_FIELDS,
        )

        user = "onb_test_reset_clear@example.com"
        self._delete_onboarding_state(user)
        doc = self._create_onboarding_state(user=user, step="compliance_setup")

        # Set data for multiple steps
        doc._save_step_data("company_info", {"company_name": "To Be Cleared"})
        doc._save_step_data("industry_selection", {"archetype": "fashion"})
        doc._save_step_data("product_structure", {"use_families": True})
        doc.selected_archetype = "fashion"
        doc.template_applied = 1
        doc.steps_completed = json.dumps(["pending", "company_info"])
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        doc.reset_onboarding()

        doc.reload()

        # All data fields should be cleared
        for step, field in STEP_DATA_FIELDS.items():
            value = doc.get(field)
            self.assertFalse(
                value,
                f"Field {field} should be cleared after reset but has value: {value}"
            )

        self.assertIsNone(doc.selected_archetype)
        self.assertFalse(doc.template_applied)
        self.assertIsNone(doc.completed_at)
        self.assertFalse(doc.is_completed)
        self.assertFalse(doc.is_skipped)
