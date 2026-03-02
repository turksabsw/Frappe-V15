# PIM Worktree Merger Instructions
> Instructions for Auto-Claude to merge isolated worktree changes back to main

## Overview

Auto-Claude creates isolated git worktrees for each spec. After completing fixes, these changes must be merged back to the main branch. This document provides merge instructions.

---

## Pre-Merge Checklist

Before merging ANY worktree:

### 1. Verify Build Success
```bash
cd .worktrees/auto-claude/[spec-name]
find frappe_pim -name "*.py" -exec python -m py_compile {} \;
# Must exit with code 0
```

### 2. Verify Migration
```bash
bench --site frappe.local migrate --dry-run
# Must show no errors
```

### 3. Verify Tests Pass
```bash
bench --site frappe.local run-tests --app frappe_pim
# All tests must pass
```

### 4. Check for Conflicts
```bash
git fetch origin main
git diff origin/main --stat
# Review changed files list
```

---

## Merge Strategy

### For Sequential Specs (Recommended)

When specs depend on each other (e.g., Issue 1 must complete before Issue 2):

```
main ─────────────────────────────────────────────►
       \                    /
        ├─ spec-001 ───────┤ (merge first)
        │                  │
        └─ spec-002 ───────┘ (merge after spec-001)
```

**Process**:
1. Complete spec-001
2. Review and merge spec-001 to main
3. Rebase spec-002 onto updated main
4. Complete spec-002
5. Review and merge spec-002 to main

### For Parallel Specs (Advanced)

When specs are independent:

```
main ─────────────────────────────────────────────►
       \                              /
        ├─ spec-001 (attribute fix) ─┤
        │                            │
        └─ spec-002 (variant impl) ──┤ (merge together)
```

**Process**:
1. Complete both specs in parallel
2. Create integration branch
3. Merge spec-001 into integration
4. Merge spec-002 into integration (resolve conflicts)
5. Test integration branch
6. Merge integration to main

---

## Conflict Resolution Rules

### Python Files (.py)

**Import Conflicts**:
- Keep ALL unique imports from both branches
- Sort imports: stdlib → third-party → local
- Remove duplicates

**Method Conflicts**:
- If same method modified in both:
  - Review both implementations
  - Keep the more complete version
  - Ensure all functionality preserved

**Indentation Conflicts**:
- ALWAYS use 4-space indentation
- If conflict shows different indentation, use 4-space version

### JSON Files (.json)

**DocType Field Conflicts**:
- Merge all unique fields
- Preserve field order by `fieldname` alphabetically in conflict sections
- Keep higher `idx` values if both have same field

**Fixture Conflicts**:
- Merge all unique records
- For duplicate records (same `name`), keep newer version

### hooks.py Conflicts

**doc_events Conflicts**:
- Merge all unique DocType event handlers
- For same DocType, merge event lists

**scheduler_events Conflicts**:
- Merge all unique scheduled tasks
- Keep cron expressions from both if different

**fixtures Conflicts**:
- Merge all unique fixture definitions
- Remove exact duplicates

---

## Merge Commands

### Standard Merge (No Conflicts Expected)

```bash
# From main branch
git checkout main
git pull origin main

# Merge spec branch
git merge auto-claude/[spec-name] --no-ff -m "Merge: [Brief description of changes]"

# Push to remote
git push origin main
```

### Merge with Conflict Resolution

```bash
# Start merge
git checkout main
git merge auto-claude/[spec-name] --no-ff

# If conflicts:
# 1. Open conflicted files
# 2. Resolve using rules above
# 3. Mark resolved
git add [resolved-files]
git commit -m "Merge: [spec-name] - Resolved conflicts in [files]"

# Push
git push origin main
```

### Squash Merge (Clean History)

```bash
git checkout main
git merge --squash auto-claude/[spec-name]
git commit -m "feat(pim): [Comprehensive description of all changes]"
git push origin main
```

---

## Post-Merge Verification

### 1. Syntax Check
```bash
find frappe_pim -name "*.py" -exec python -m py_compile {} \;
```

### 2. Migration Check
```bash
bench --site frappe.local migrate
```

### 3. Functional Test
```bash
bench --site frappe.local console
>>> # Test each fixed component
>>> frappe.get_doc({"doctype": "PIM Attribute Type", "type_name": "Test", "type_code": "test", "base_type": "String"}).insert()
>>> frappe.get_doc({"doctype": "Product Family", "family_name": "Test", "family_code": "test"}).insert()
```

### 4. Clear Caches
```bash
bench --site frappe.local clear-cache
bench --site frappe.local clear-website-cache
```

---

## Cleanup After Merge

### Remove Worktree
```bash
# List worktrees
git worktree list

# Remove merged worktree
git worktree remove .worktrees/auto-claude/[spec-name]

# Prune stale worktrees
git worktree prune
```

### Delete Spec Branch (Optional)
```bash
# Delete local branch
git branch -d auto-claude/[spec-name]

# Delete remote branch (if pushed)
git push origin --delete auto-claude/[spec-name]
```

---

## Rollback Procedure

If merge causes issues:

### Immediate Rollback (Before Push)
```bash
git reset --hard HEAD~1
```

### After Push Rollback
```bash
# Create revert commit
git revert HEAD -m 1
git push origin main

# Or force reset (dangerous, requires team coordination)
git reset --hard HEAD~1
git push origin main --force
```

---

## Spec Merge Order for PIM Fix

Merge these specs in EXACT order:

1. **spec-001-attribute-type-fix**
   - Fixes imports and indentation
   - No dependencies

2. **spec-002-child-tables**
   - Creates Family Attribute Template
   - Creates Family Variant Attribute
   - Creates Product Type Field
   - Depends on: spec-001

3. **spec-003-product-type-enhance**
   - Adds type_fields to PIM Product Type
   - Depends on: spec-002 (needs Product Type Field)

4. **spec-004-erpnext-fixtures**
   - Creates custom_field.json
   - Updates hooks.py
   - Depends on: spec-003

5. **spec-005-product-master-mapping**
   - Consolidates field mappings
   - Depends on: spec-004 (needs custom fields)

6. **spec-006-product-variant-impl**
   - Full variant controller implementation
   - Depends on: spec-005

---

## Conflict Scenarios

### Scenario A: Both Specs Modified Same File

**Example**: Both spec-005 and spec-006 modified `product_master.py`

**Resolution**:
1. Merge spec-005 first (it's in the dependency chain)
2. Rebase spec-006 onto main
3. Resolve any conflicts in spec-006 branch
4. Then merge spec-006

### Scenario B: Fixture Conflicts

**Example**: Both specs added Custom Fields

**Resolution**:
1. Open `fixtures/custom_field.json`
2. Merge all unique field definitions
3. Ensure no duplicate `fieldname` values
4. Validate JSON syntax

### Scenario C: hooks.py Conflicts

**Example**: Both specs added scheduler events

**Resolution**:
1. Keep all unique entries in each section
2. For duplicate function references, keep one
3. Validate Python syntax after merge
