---
description: "Build an operator's voice profile from scratch: the guided collection-and-extraction on-ramp that walks you from raw samples to a profile satisfying the voice contract, keeping the interview and the blind test human"
argument-hint: Optional focus (e.g., "start collection", "resume", "just the interview")
---

# Build a voice profile

Invoke the `deliberate-engineering-voice-build` skill against $ARGUMENTS.

Walk the operator from raw writing samples to a voice profile that satisfies the voice contract: help them identify their communication archetypes, collect samples typed by archetype and language, run the analysis and an adversarial recount, drive a findings-based interview, synthesize the profile files, then calibrate them with a blind A/B, keeping the interview and the blind pick human. Delegate the method to the voice skill's `bootstrap.md`. The corpus and the finished profile are kept local, out of every repository, by a best-effort check rather than a guarantee: it declines to write where it cannot confirm the path is out of a repository, and it cannot enforce that: an agent can ignore an instruction and nothing outside it blocks the write. Resumable across sessions; on demand only.
