---
name: speckit-bio-provenance-collect
description: Collect a reproducibility manifest
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: bio-provenance:commands/collect.md
---

# Provenance collection

Collect input hashes, repository revision, execution timestamp, Python version,
and the selected pipeline metadata. The resulting JSON is part of the run
evidence and must be retained with the final report.

User request:

$ARGUMENTS