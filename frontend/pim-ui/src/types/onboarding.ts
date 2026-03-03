/**
 * Onboarding-related type definitions for the SaaS onboarding wizard.
 *
 * Maps to backend:
 * - PIM Onboarding State DocType (12-step state machine)
 * - Onboarding API (frappe_pim.pim.api.onboarding)
 * - Template Engine service
 */

import type { FrappeEntity } from './index'

// ============================================================================
// Onboarding Steps
// ============================================================================

/** All valid onboarding step identifiers, matching backend ONBOARDING_STEPS */
export type OnboardingStepName =
  | 'pending'
  | 'company_info'
  | 'industry_selection'
  | 'product_structure'
  | 'channel_setup'
  | 'workflow_preferences'
  | 'compliance_setup'
  | 'template_applied'
  | 'customization_review'
  | 'first_data'
  | 'guided_tour'
  | 'completed'

/** Ordered list of onboarding steps (mirrors backend constant) */
export const ONBOARDING_STEPS: readonly OnboardingStepName[] = [
  'pending',
  'company_info',
  'industry_selection',
  'product_structure',
  'channel_setup',
  'workflow_preferences',
  'compliance_setup',
  'template_applied',
  'customization_review',
  'first_data',
  'guided_tour',
  'completed',
] as const

/** Steps that collect user form data (mirrors backend STEP_DATA_FIELDS) */
export const STEP_DATA_FIELDS: Partial<Record<OnboardingStepName, string>> = {
  company_info: 'company_info_data',
  industry_selection: 'industry_selection_data',
  product_structure: 'product_structure_data',
  channel_setup: 'channel_setup_data',
  workflow_preferences: 'workflow_preferences_data',
  compliance_setup: 'compliance_setup_data',
  customization_review: 'customization_review_data',
  first_data: 'first_data_data',
  guided_tour: 'guided_tour_data',
}

// ============================================================================
// Onboarding State
// ============================================================================

/** PIM Onboarding State - DocType entity */
export interface PIMOnboardingState extends FrappeEntity {
  user: string
  current_step: OnboardingStepName
  is_completed: boolean
  is_skipped: boolean
  started_at?: string
  completed_at?: string
  selected_archetype?: string
  template_applied: boolean
  template_applied_at?: string
  template_result?: string
  progress_percent: number
  steps_completed?: string
  last_step_completed_at?: string
  error_log?: string
  /** Step data JSON fields */
  company_info_data?: string
  industry_selection_data?: string
  product_structure_data?: string
  channel_setup_data?: string
  workflow_preferences_data?: string
  compliance_setup_data?: string
  customization_review_data?: string
  first_data_data?: string
  guided_tour_data?: string
}

// ============================================================================
// API Response Types
// ============================================================================

/** Step detail in the onboarding state summary */
export interface OnboardingStepDetail {
  name: OnboardingStepName
  index: number
  is_completed: boolean
  is_current: boolean
  has_data: boolean
}

/** Onboarding state summary returned by backend APIs */
export interface OnboardingStateSummary {
  user: string
  current_step: OnboardingStepName | 'not_started'
  is_completed: boolean
  is_skipped: boolean
  progress_percent: number
  selected_archetype?: string | null
  template_applied: boolean
  started_at?: string | null
  completed_at?: string | null
  completed_steps: string[]
  next_step?: OnboardingStepName | null
  previous_step?: OnboardingStepName | null
  total_steps: number
  steps: OnboardingStepDetail[]
  /** Included when resuming a step that has saved data */
  current_step_data?: Record<string, unknown>
}

/** Step metadata from get_onboarding_steps API */
export interface OnboardingStepMetadata {
  name: OnboardingStepName
  index: number
  has_data_field: boolean
  data_field?: string | null
}

// ============================================================================
// Step Form Data Types
// ============================================================================

/** Company info step data */
export interface CompanyInfoData {
  company_name: string
  industry?: string
  company_size?: 'small' | 'medium' | 'large' | 'enterprise'
  country?: string
  currency?: string
  website?: string
}

/** Industry selection step data */
export interface IndustrySelectionData {
  archetype: string
  sub_industry?: string
  product_count_estimate?: string
  has_variants?: boolean
}

/** Product structure step data */
export interface ProductStructureData {
  use_families?: boolean
  use_categories?: boolean
  variant_levels?: number
  use_sku_generation?: boolean
  sku_pattern?: string
}

/** Channel setup step data */
export interface ChannelSetupData {
  channels?: string[]
  primary_channel?: string
  marketplace_integrations?: string[]
}

/** Workflow preferences step data */
export interface WorkflowPreferencesData {
  require_approval?: boolean
  auto_sync_to_erp?: boolean
  sync_direction?: 'PIM Master' | 'ERP Master' | 'Bidirectional'
  enable_quality_scoring?: boolean
}

/** Compliance setup step data */
export interface ComplianceSetupData {
  regulatory_standards?: string[]
  certifications_required?: string[]
  enable_safety_warnings?: boolean
}

/** Union of all step form data types */
export type StepFormData =
  | CompanyInfoData
  | IndustrySelectionData
  | ProductStructureData
  | ChannelSetupData
  | WorkflowPreferencesData
  | ComplianceSetupData
  | Record<string, unknown>

// ============================================================================
// Industry Archetype Types
// ============================================================================

/** Available archetype information */
export interface ArchetypeInfo {
  archetype: string
  label: string
  description: string
  version?: string
}

/** Response from get_available_archetypes API */
export interface AvailableArchetypesResponse {
  archetypes: ArchetypeInfo[]
  total: number
}

/** Section preview in archetype template */
export interface ArchetypeSectionPreview {
  count: number
  items: string[]
}

/** Response from preview_archetype API */
export interface ArchetypePreviewResponse {
  archetype: string
  label: string
  description: string
  version?: string
  extends?: string
  sections: Record<string, ArchetypeSectionPreview>
}

/** Template application result from apply_archetype_template API */
export interface TemplateApplicationResult {
  success: boolean
  archetype: string
  status: 'completed' | 'partial' | 'failed'
  entities_created: number
  entities_skipped: number
  entities_failed: number
  details: Record<string, TemplateEntityDetail>
  errors: string[]
  messages: string[]
  dry_run?: boolean
}

/** Per-entity-type details in template application result */
export interface TemplateEntityDetail {
  created: number
  skipped: number
  failed: number
  items: string[]
}

// ============================================================================
// UI Step Types (for the Vue.js wizard component)
// ============================================================================

/** Onboarding step definition for the UI wizard */
export interface OnboardingWizardStep {
  id: string
  title: string
  description: string
  component: string
  isCompleted: boolean
  isActive: boolean
  isFutureStep: boolean
  hasDataField?: boolean
}
