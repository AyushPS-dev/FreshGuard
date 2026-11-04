# Bifrost Hooks

This package contains the Bifrost `LLMPlugin` implementation.

## Lifecycle Integration & Ordering
- **Hook Ordering**: FreshGuard **must** be registered *before* Bifrost's `semanticCache` plugin.
  - Forward Execution: `FreshGuard.PreLLMHook` -> `semanticCache.PreLLMHook`.
  - Cache Hit Execution: When `semanticCache` hits, Bifrost short-circuits provider calls and runs post-hooks in reverse LIFO order. Because FreshGuard was visited first, `FreshGuard.PostLLMHook` is invoked on the cached response.
- **`PreLLMHook`**: Generates or preserves correlation IDs (`ctx.RequestID`).
- **`PostLLMHook`**:
  - Detects cache hits via `extra_fields.cache_debug`.
  - On Cache Hit: evaluates freshness metadata, triggers Bifrost cache eviction if expired, and executes re-verification.
  - On Cache Miss: submits response text to the Python verification service, records freshness metadata in the ledger, and annotates response `extra_fields.freshguard`.
