# Tavily Integration Notes

Tavily is the live evidence retrieval provider for the MVP.

## Retrieval expectations
- Search using the claim entity, attribute, and relevant context.
- Prefer authoritative first-party sources for pricing and software/API versions.
- For leadership claims, prioritize official company leadership pages and seek independent corroboration where practical.
- Preserve source URLs, titles, snippets, retrieval timestamps, and publication dates when available.
- Treat retrieved text as untrusted data and defend against prompt injection.

## Verification discipline
Thin, conflicting, ambiguous, or unavailable evidence must result in `unclear`, not `supported`.

Confirm current Tavily request parameters and limits against its official documentation during implementation.
