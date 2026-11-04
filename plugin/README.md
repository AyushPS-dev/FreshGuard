# FreshGuard Bifrost Plugin

The FreshGuard Bifrost Plugin integrates freshness verification and semantic cache protection directly into the Bifrost LLM gateway.

## Responsibilities
- Intercepts requests and responses within Bifrost's request lifecycle (`PreLLMHook` and `PostLLMHook`).
- Propagates and generates correlation IDs (`X-Request-ID`).
- Communicates with Ayush's Python verification service via bounded HTTP client with exponential backoff and retries.
- Enforces Category TTL Policies (Pricing: 24h, Software Versions: 24h, Leadership: 7d).
- Intercepts semantic cache hits to prevent stale verification metadata reuse.
- Triggers eviction on stale cache entries via Bifrost's Cache Eviction API (`DELETE /api/cache/clear/{cacheId}`).
- Respects configurable `fail_open` and `fail_closed` resilience policies.

## Package Structure
- `schemas/`: Normalized Bifrost data types (`BifrostContext`, `BifrostRequest`, `BifrostResponse`, `LLMPlugin`).
- `client/`: Verification service client calling `POST /v1/verifications` and `GET /v1/verifications/{id}`.
- `cache/`: Freshness metadata ledger, category TTL policies, cache hit evaluator, and Bifrost eviction client.
- `hooks/`: Bifrost `LLMPlugin` implementation (`PreLLMHook`, `PostLLMHook`).
- `main.go`: Entry point exporting standard Bifrost plugin lifecycle symbols (`Init`, `GetName`, `PreLLMHook`, `PostLLMHook`).
- `integration_test.go`: End-to-end integration tests simulating a full Bifrost gateway and verification engine.

## Running Tests
```bash
cd plugin
go test -v ./...
```
