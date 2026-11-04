# Verification API Contract

This document defines the intended HTTP contract. It is a specification only; no endpoint implementation is included.

## Submit verification
`POST /v1/verifications`

Request fields:
- `request_id`: caller-generated correlation identifier
- `text`: response text to inspect
- `mode`: `async` or `blocking`
- `categories`: optional allowed claim categories

Response fields:
- `verification_id`
- `status`: `accepted`, `completed`, or `failed`
- `result_url`: available for asynchronous retrieval

## Retrieve result
`GET /v1/verifications/{verification_id}`

Expected result fields:
- `verification_id`
- `status`
- `claims[]`
- `checked_at`
- `error`: safe machine-readable failure information when applicable

## Claim result
Each claim should include `claim_id`, `category`, `entity`, `attribute`, `original_text`, `verdict`, `confidence`, `evidence[]`, `checked_at`, and optional `corrected_value`.

## Verdict enum
- `supported`
- `contradicted`
- `unclear`

## Contract status
Proposed. Confirm naming, validation rules, authentication, limits, and error envelope with all team members before implementation.
