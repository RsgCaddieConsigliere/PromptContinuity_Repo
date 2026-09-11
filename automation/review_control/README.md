# Review Control

Public-safe, source-free control patterns for bounded review runs.

Core invariants:
- source identity and fixity are preserved;
- review coverage is recorded by stable locator;
- candidate deltas are separated from approved state changes;
- conflicts, adverse facts, errata, and missing evidence are never silently discarded;
- source closeout requires explicit coverage and QA checks;
- archives are indexed but not substantively re-reviewed by default;
- restricted paths are fail-closed;
- no matter evidence, provider identifiers, or confidential excerpts belong in this repository.

This directory contains generic schemas and synthetic tests only.
