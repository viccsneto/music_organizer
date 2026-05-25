# Review question bank (Socratic)

Use these as **questions to the developer**. Do not answer them on the developer’s behalf.

## Intent & scope

- What user-visible behavior changed, and what did not?
- What invariant is this change trying to enforce?
- Which part of the diff is load-bearing for correctness?

## Failure modes

- What happens on partial failure (network error, filesystem error, invalid input)?
- What’s the recovery / rollback story?
- What’s the worst plausible bad input and how is it handled?

## Tests & traceability

- Which tests would fail if the main assumption is wrong?
- What critical edge case is not covered yet?
- If you had to delete one test, which would you keep to preserve safety?

## Security & boundaries

- What inputs are trusted vs untrusted?
- Are there any paths that could write outside the intended directory?

## Performance & complexity

- What’s the asymptotic behavior of the hottest path?
- What happens if the repo has 10x more files or larger diffs?
