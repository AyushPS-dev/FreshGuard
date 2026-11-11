# FreshGuard Verification Service

FastAPI-based real-time freshness and factual verification service for LLM-generated responses.

**Implementation Owner**: Ayush

---

## Capabilities

- **Factual Claim Extraction**: Extracts discrete, time-sensitive factual assertions from text across categories (`software_version`, `pricing`, `leadership`, `product_availability`, `recent_events`, `statistics`).
- **Real-Time Evidence Retrieval**: Bounded, concurrent web search using the Tavily Search API.
- **Deterministic & Semantic Verification**: Fast-path SemVer comparisons for software releases combined with model-driven verdict assessments.
- **Freshness Policy Enforcement**: Dynamic TTL calculation and staleness detection.
- **Semantic Caching & Idempotency**: Persistent cache with fingerprinting and fast-path duplicate `request_id` resolution.
- **Contract Compatibility**: Conforms to `shared/schemas/verification_api.json` and the Bifrost Go Gateway plugin.

---

## Supported LLM Providers

Configured via the `LLM_PROVIDER` environment variable:

1. **`mock`** *(Default)*:
   - Zero external credentials required.
   - Deterministic canned responses for local development, integration, and contract testing.
2. **`gemini`**:
   - Google Gemini Developer API using the official `google-genai` Python SDK.
   - Default model: `gemini-2.5-flash` (free tier eligible: 15 RPM, 1M TPM, 1,500 RPD in Google AI Studio).
   - Asynchronous structured outputs validated against Pydantic schemas.
   - Environment variables: `GEMINI_API_KEY`, `GEMINI_MODEL`.
3. **`openai`**:
   - OpenAI or OpenAI-compatible inference endpoints via asynchronous HTTPX.
   - Default model: `gpt-4o-mini`.
   - Environment variables: `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`.

---

## Configuration

Copy `.env.example` to `.env` and configure appropriate variables:

```bash
# LLM Provider Selection (mock, gemini, openai)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.5-flash

# Search Configuration
TAVILY_API_KEY=tvly-...

# Server & Database
ENVIRONMENT=development
PORT=8000
DATABASE_URL=sqlite+aiosqlite:///./freshguard.db
```

---

## Running the Service

```bash
# Start server using the dynamic runner
python run.py

# Or directly with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Testing

```bash
# Run all unit and integration tests
pytest tests/ -v
```
