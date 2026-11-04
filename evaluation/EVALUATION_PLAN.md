# Evaluation Plan

## Dataset
Build a manually reviewed dataset of 60–100 claims across the three supported categories. Include current, stale, contradicted, ambiguous, and conflicting-evidence examples.

## Ground truth
Record independently checked expected values, authoritative sources, and the date each label was established.

## Metrics
- Claim extraction precision and recall
- Verdict accuracy
- False-supported rate
- False-contradicted rate
- Unclear rate
- Per-category performance
- p50 and p95 verification latency
- Tavily and model cost per verification
- Cache freshness enforcement rate

## Reporting
Publish methodology, dataset limitations, sample counts, and results. Do not present unmeasured targets as achieved results.
