# Cache Integration & Freshness Policy

This package implements semantic cache freshness protection for Bifrost.

## Core Components
- `policy.go`: Defines TTL policies per category:
  - **Pricing**: 24 hours (`DefaultTTLPrice`)
  - **Software/API Versions**: 24 hours (`DefaultTTLSoftwareVersion`)
  - **Company Leadership**: 7 days (`DefaultTTLLeadership`)
  - Automatic minimum TTL calculation across multi-claim responses.
- `metadata.go`: Represents verified claim metadata, expiration timestamps, and verdict states.
- `ledger.go`: Thread-safe ledger mapping `cache_id` and response content hashes to freshness records.
- `evaluator.go`: Evaluates cache hits against strict rules:
  1. Missing verification metadata must **never** be treated as fresh.
  2. Expired metadata requires re-verification.
  3. Expiration does not mean a claim is false.
  4. Cache hits must **never** silently inherit expired `supported` verdicts.
- `evictor.go`: Interacts with Bifrost's management API (`DELETE /api/cache/clear/{cacheId}`) to invalidate stale entries.
