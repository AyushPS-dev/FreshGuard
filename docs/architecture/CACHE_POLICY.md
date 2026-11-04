# Semantic Cache Freshness Policy

## Goal
Prevent a semantically cached response from silently reusing expired freshness verification.

## Required metadata
- Claim category
- Normalized entity and attribute
- Verification timestamp
- Evidence references
- Policy TTL
- Verification status

## Initial policy proposals
| Category | Proposed TTL |
|---|---:|
| Pricing | 24 hours |
| Software/API versions | 24 hours |
| Company leadership | 7 days |

These are starting values for evaluation, not guaranteed truth windows.

## Cache-hit behavior
A cache hit must be checked against its verification metadata. Expired or missing metadata requires re-verification or an explicitly marked unverified result.

## Bifrost feasibility gate
Confirm hook order, cache metadata support, eviction/bypass APIs, and behavior on cache hits against the exact Bifrost version. If eviction is unavailable, document the fallback honestly and do not claim cache invalidation.
