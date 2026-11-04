# Verification Service Client

This package implements the Go HTTP client communicating with Ayush's Python verification service.

## Endpoints
- `POST /v1/verifications`: Submits text for claim extraction, Tavily retrieval, and verdict judgment.
- `GET /v1/verifications/{verification_id}`: Polls or retrieves verification results by ID.

## Reliability Features
- **Bounded Timeouts**: Configurable per-request timeout (default 3s).
- **Exponential Backoff & Jitter**: Retries transient failures (429, 502, 503, 504, transport timeouts) with randomized jitter.
- **Request Correlation**: Propagates `X-Request-ID` header across all outgoing calls.
- **Fail-Open / Fail-Closed**: Configurable failure policy protecting user experience while guaranteeing strict safety.
- **Safe Error Model**: Deserializes into `APIError` without exposing provider credentials or raw stack traces.
