---
name: verify-as-you-go
description: >-
  An AI coding agent skill for continuously checking work while writing code.
  Verification is incremental, local, and explicit, reducing error accumulation
  and compounding mistakes.
license: MIT
compatibility: Designed for GitHub Copilot and VS Code Copilot agents that can discover skills under .github/skills.
---

You are an AI coding agent that must **verify its work as it goes**.
This means you continuously check your work while writing code—instead of generating a large solution first and validating it only at the end. Your verification must be incremental, local, and explicit to reduce error accumulation and compounding mistakes.

Think of it as tight feedback loops embedded directly into your reasoning and execution.

## Goal

The primary goal is to **ensure incremental correctness** to prevent small logical errors from invalidating an entire solution.

## Core Principles

1.  **Incremental Correctness Over Global Correctness**
    -   **Rule**: Every small step must be correct before moving on.
    -   **Actions**:
        -   Verify each function, assumption, or transformation immediately.
        -   Avoid “I’ll fix it later” reasoning.

2.  **Assumption Surfacing and Checking**
    -   **Rule**: Every non-trivial assumption must be stated explicitly and checked against constraints, specs, or known facts.
    -   **Examples of assumptions**:
        -   Input ranges and data formats.
        -   Time/space complexity limits.
        -   API behavior and contracts.

3.  **Local Validation Mechanisms**
    -   **Rule**: Use the cheapest possible validation at each step. Do not jump directly to heavy tests if a lighter check suffices.
    -   **Validation hierarchy (cheapest → strongest)**:
        1.  Mental/type checks
        2.  Static reasoning (types, invariants)
        3.  Assertions
        4.  Unit tests
        5.  Property-based tests
        6.  Integration tests

4.  **Forward-and-Backward Reasoning**
    -   **Rule**: After producing a step, perform both a forward and backward check.
    -   **Checks**:
        -   **Forward check**: “Does this do what I intend?”
        -   **Backward check**: “What must be true for this to be correct?”

5.  **Invariant Preservation**
    -   **Rule**: Define invariants early and re-check them after each change. If an invariant breaks, stop and repair immediately.
    -   **Examples**: Data structure invariants (a BST remains sorted), loop invariants, security invariants (no plaintext secrets).

## Guardrails

-   **Error Localization Discipline**: When a verification fails, identify the smallest step that could be wrong. Do not regenerate everything. Isolate the fault, fix it locally, and re-verify downstream steps.
-   **No Silent Uncertainty**: If verification cannot be completed, you must not proceed silently. Unverified code must never be treated as verified. You must mark the uncertainty explicitly, reduce scope to a verifiable subset, or ask for clarification.
