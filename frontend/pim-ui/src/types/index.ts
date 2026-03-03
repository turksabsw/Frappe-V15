/** Core PIM type definitions */

/** Frappe API response wrapper */
export interface FrappeResponse<T> {
  message: T
  exc?: string
  exc_type?: string
  _server_messages?: string
}

/** Frappe list response with pagination */
export interface FrappeListResponse<T> {
  data: T[]
  total_count: number
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

/** PIM Product Type - configuration entity */
export interface PIMProductType extends FrappeEntity {
  type_name: string
  type_code: string
  description?: string
  is_active: boolean
}

/** Product Family - tree structure for attribute inheritance */
export interface ProductFamily extends FrappeEntity {
  family_name: string
  family_code: string
  parent_family?: string
  is_group: boolean
  description?: string
  lft: number
  rgt: number
}

/** PIM Attribute - dynamic product attribute definition */
export interface PIMAttribute extends FrappeEntity {
  attribute_name: string
  attribute_code: string
  attribute_type: string
  attribute_group?: string
  is_required: boolean
  is_filterable: boolean
  is_searchable: boolean
  is_variant_axis: boolean
  is_localizable: boolean
  sort_order: number
}

/** PIM Attribute Option - predefined value for select attributes */
export interface PIMAttributeOption extends FrappeEntity {
  option_code: string
  label: string
  color_hex?: string
  image?: string
  sort_order: number
  is_active: boolean
}

/** Product Master - virtual DocType mapped to ERPNext Item */
export interface ProductMaster extends FrappeEntity {
  product_name: string
  product_code: string
  product_type?: string
  product_family?: string
  status: 'Draft' | 'Active' | 'Discontinued' | 'Archived'
  short_description?: string
  long_description?: string
  brand?: string
  erp_item?: string
  completeness_score: number
}

/** Product Variant - child of Product Master */
export interface ProductVariant extends FrappeEntity {
  variant_code: string
  variant_name: string
  parent_product: string
  parent_variant?: string
  variant_level: number
  sku?: string
  status: 'Draft' | 'Active' | 'Discontinued'
  erp_item?: string
}

/** Product Attribute Value - EAV storage */
export interface ProductAttributeValue extends FrappeEntity {
  attribute: string
  value_type: string
  value_text?: string
  value_int?: number
  value_float?: number
  value_boolean?: boolean
  value_date?: string
  value_datetime?: string
  value_link?: string
  value_json?: string
  display_value?: string
  unit?: string
  source?: string
  locale?: string
}

/** PIM Category - NestedSet navigation taxonomy */
export interface PIMCategory extends FrappeEntity {
  category_name: string
  category_code: string
  parent_category?: string
  is_group: boolean
  description?: string
  lft: number
  rgt: number
}

/** Onboarding state tracking */
export interface PIMOnboardingState extends FrappeEntity {
  current_step: string
  is_completed: boolean
  is_skipped: boolean
  company_name?: string
  industry?: string
  archetype?: string
  step_data?: Record<string, unknown>
}

/** Onboarding step definition */
export interface OnboardingStep {
  id: string
  title: string
  description: string
  component: string
  isCompleted: boolean
  isActive: boolean
  isFutureStep: boolean
}

/** API error response */
export interface APIError {
  message: string
  exc_type?: string
  status_code?: number
}

/** Completeness score breakdown */
export interface CompletenessScore {
  total: number
  filled: number
  required: number
  score: number
  missing_attributes: string[]
}

/** Sync status information */
export interface SyncStatus {
  status: 'Not Synced' | 'Synced' | 'Pending' | 'Error' | 'Conflict'
  last_sync?: string
  erp_item?: string
  error_message?: string
}
