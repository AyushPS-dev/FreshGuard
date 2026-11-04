# Security and Failure Handling

## Trust boundaries
- User prompts and model responses are untrusted input.
- Tavily results and webpages are untrusted evidence.
- Retrieved content must never override system or developer instructions.

## Secrets
Keep API keys in environment configuration or approved secret storage. Never commit secrets or include them in logs.

## Reliability requirements
- Bounded request timeouts
- Bounded retries with backoff
- Request correlation IDs
- Explicit fail-open/fail-closed configuration
- No Supported verdict when retrieval or judgment fails
- Safe handling of malformed provider responses

## Privacy
Avoid storing full prompts/responses unless required and disclosed. Define retention and user-data deletion behavior before production use.
