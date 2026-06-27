# Candidate queue

Pending, generalized, employer-neutral candidates for the deliberate-engineering catalog, produced on demand by the `deliberate-engineering-contribute` skill.

Each file is one proposed lens or rule change (`status: pending`). The skill deposits files here but never commits them. Promotion to the catalog is gated: a human reviews the candidate, runs a leak-audit, and uses the `deliberate-engineering-promote` skill (which edits the catalog in the working tree and stops before commit/PR/push). Nothing here is part of the shipped catalog until it is promoted and merged.
