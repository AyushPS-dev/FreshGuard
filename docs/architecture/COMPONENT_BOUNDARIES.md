# Component Boundaries

## Gateway and Go plugin
Owns Bifrost hook integration, request correlation, service communication, metadata propagation, and cache-policy integration where supported by Bifrost.

## Python verification service
Owns candidate detection, claim extraction, Tavily retrieval, evidence assessment, deterministic checks, and verification result formatting.

## Frontend
Owns user-facing dashboard, manual verification workflows, result presentation, history, and settings UI.

## Shared contracts
Owns versioned request/response schemas and common enums.

## Boundary rule
Business verification logic must not be duplicated in the Go adapter or frontend.
