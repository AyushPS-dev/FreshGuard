# FreshGuard System Overview

## Purpose
FreshGuard checks time-sensitive claims in LLM responses against current web evidence and records freshness metadata for downstream cache decisions.

## MVP claim categories
- Pricing
- Software and API versions
- Company leadership

All other claim categories are out of scope for the initial MVP.

## Logical components
1. Bifrost gateway integration
2. Go gateway adapter
3. Python verification service
4. Tavily evidence retrieval
5. Structured claim judgment
6. Freshness metadata and cache policy
7. Web dashboard

## High-level flow
Request → Bifrost → model response → FreshGuard adapter → verification service → Tavily evidence → judgment → structured result → response metadata/cache policy.

## Important constraints
- Retrieved web content is untrusted evidence, never instructions.
- Verification failure must never produce a Supported verdict.
- Cache expiry means re-verification is required, not that a claim is false.
- Actual Bifrost hook ordering and cache invalidation capabilities must be verified before implementation claims are made.
