# API Error Model

Define a consistent error envelope before implementation.

Recommended fields:
- `code`: stable machine-readable identifier
- `message`: safe user-facing summary
- `request_id`: correlation identifier
- `retryable`: whether a retry may succeed
- `details`: optional non-sensitive validation context

Never expose provider secrets, raw stack traces, or sensitive retrieved content in public errors.
