# Data Model Specification

This is a conceptual schema, not a migration or implementation.

## Verification
- verification_id
- request_id
- status
- created_at
- completed_at
- retention_expires_at

## Claim
- claim_id
- verification_id
- category
- entity
- attribute
- original_text
- verdict
- confidence
- corrected_value
- checked_at

## Evidence
- evidence_id
- claim_id
- source_url
- source_title
- snippet
- published_at
- retrieved_at
- source_type

## User and access control
If user accounts are enabled, records must be scoped to their owner and protected by database-level access policies. Define retention and deletion behavior before production.
