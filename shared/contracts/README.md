# Shared Contracts

This directory contains cross-component API and event contracts shared between Kamal's Go Bifrost gateway adapter, Ayush's Python verification service, and Krrish's frontend.

## Machine-Readable Schemas
- `shared/schemas/verification_api.json`: JSON Schema definition for `POST /v1/verifications`, `GET /v1/verifications/{id}`, `Claim`, `Evidence`, and `APIError`.

## Key Enums & Policies
- **Verdicts**: `supported`, `contradicted`, `unclear`.
- **Claim Categories**: `pricing`, `software_version`, `leadership`.
- **TTLs**:
  - Pricing: 24 hours
  - Software Versions: 24 hours
  - Leadership: 7 days
