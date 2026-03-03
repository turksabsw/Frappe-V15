/**
 * Core PIM type definitions and barrel exports.
 *
 * This module contains Frappe framework types and re-exports
 * all domain-specific types from their respective modules.
 */

// ============================================================================
// Frappe Framework Types
// ============================================================================

/** Frappe API response wrapper for method calls */
export interface FrappeResponse<T = unknown> {
  message: T
  exc?: string
  exc_type?: string
  _server_messages?: string
}

/** Frappe list response with pagination from resource API */
export interface FrappeListResponse<T> {
  data: T[]
  total_count: number
}

/** Frappe document resource API response */
export interface FrappeDocResponse<T> {
  data: T
}

/** Base entity with Frappe standard fields */
export interface FrappeEntity {
  name: string
  owner: string
  creation: string
  modified: string
  modified_by: string
  docstatus: number
  idx: number
}

/** Frappe field filter for get_list calls */
export type FrappeFilter = string | [string, string] | [string, string, string | number]

/** Frappe filters object */
export type FrappeFilters = Record<string, FrappeFilter | string | number | boolean>

/** Frappe or_filters (array of filter arrays) */
export type FrappeOrFilters = Array<[string, string, string | number]>

/** Options for Frappe get_list API */
export interface FrappeListParams {
  doctype: string
  fields?: string[]
  filters?: FrappeFilters
  or_filters?: FrappeOrFilters
  order_by?: string
  limit_start?: number
  limit_page_length?: number
  parent?: string
  group_by?: string
}

/** Options for Frappe get_count API */
export interface FrappeCountParams {
  doctype: string
  filters?: FrappeFilters
}

// ============================================================================
// API Error Types
// ============================================================================

/** API error response */
export interface APIError {
  message: string
  exc_type?: string
  status_code?: number
  indicator?: 'red' | 'orange' | 'yellow'
  server_messages?: string[]
}

/** Validation error detail */
export interface ValidationError {
  field: string
  message: string
}

// ============================================================================
// Re-exports from Domain Modules
// ============================================================================

// Product types
export type {
  PIMProductType,
  ProductTypeField,
  ProductTypeAllowedFamily,
  PIMAttributeType,
  AttributeBaseType,
  PIMAttributeGroup,
  PIMAttributeTemplate,
  TemplateAttribute,
  PIMAttribute,
  PIMAttributeOption,
  ProductFamily,
  FamilyAttribute,
  FamilyVariantAttribute,
  PIMCategory,
  PIMBrand,
  ProductStatus,
  VariantStatus,
  ProductMaster,
  ProductVariant,
  ProductAttributeValue,
  ProductVariantAxisValue,
  ProductMedia,
  MediaType,
  SyncStatusValue,
  SyncStatus,
  CompletenessScore,
  QualityRule,
  QualityScoreResult,
  ProductListResponse,
  ProductListParams,
  CategoryTreeNode,
  FamilyTreeNode,
  VariantGenerationRequest,
  VariantAxisDefinition,
  VariantGenerationResult,
} from './product'

// Onboarding types
export type {
  OnboardingStepName,
  PIMOnboardingState,
  OnboardingStepDetail,
  OnboardingStateSummary,
  OnboardingStepMetadata,
  CompanyInfoData,
  IndustrySelectionData,
  ProductStructureData,
  ChannelSetupData,
  WorkflowPreferencesData,
  ComplianceSetupData,
  StepFormData,
  ArchetypeInfo,
  AvailableArchetypesResponse,
  ArchetypeSectionPreview,
  ArchetypePreviewResponse,
  TemplateApplicationResult,
  TemplateEntityDetail,
  OnboardingWizardStep,
} from './onboarding'

// Re-export onboarding constants
export { ONBOARDING_STEPS, STEP_DATA_FIELDS } from './onboarding'

// Legacy compatibility: OnboardingStep (used by OnboardingWizard.vue)
export type { OnboardingWizardStep as OnboardingStep } from './onboarding'
