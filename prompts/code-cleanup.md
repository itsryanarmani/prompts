# Untangle and clean up a codebase

Untangle the knotted code in this repository: leaky abstractions, copied code that has drifted apart,
temporary workarounds that never got deleted, and empty wrappers.

Keep existing behavior and public interfaces intact. Do not add layers just to reduce line counts.
Read the repository instructions and identify its entry points, tests, and build commands before editing.
Give periodic progress updates with findings, measured results, and remaining work.

## Map the knots first

Create an HTML wiring diagram that fits on one screen.
Draw a line from each feature to every file it touches.
Mark the worst knots in red and number them.
For each knot, give the file, line number, and a concrete way to untangle it.
State the limits of the map, including dynamic references you cannot resolve.

Then work on a new branch. Start with the worst knot.
After each change, run the tests and the build.
If there are no tests, at least verify that the build passes.
If a check fails, restore that change and preserve the failure evidence.

## Remove code only after proving it is unused

Find:

- Functions, classes, components, and exports that nothing calls.
- Files and folders that no entry point references.
- Branches that can never run and feature flags that are hard-coded off.
- Whole blocks of commented-out code and obsolete temporary workarounds.

Show the evidence before deleting anything:

- Repository-wide search results, including relevant configuration and scripts.
- Whether the code is reachable from an entry point.
- Whether any test imports or uses it.
- Whether removing it also removes an initializer, side effect, or diagnostic.

Put uncertain cases on a separate list and keep them.
This includes dynamic imports, calls by string name, framework conventions, and public APIs.
Do not treat a missing text match as proof of non-use.

Delete proven unused code on a new branch, in small batches.
Run the tests and build after each batch. Restore any batch that breaks either check.

## Consolidate code that behaves exactly the same

Find:

- Functions and helpers with different names that do the same job.
- Near-identical components, request wrappers, and validation logic.
- Code that was copied and then changed slightly in each place.

For each group, say which version you will keep and why.
Compare defaults, outputs, errors, side effects, asynchronous ordering, and type contracts.
Point every other call site at the retained implementation.
Keep diagnostics when moving code.

Only merge implementations that behave exactly the same.
Keep versions with meaningful differences separate. Show those differences in the final report.
Do not replace distinct policies with a configurable helper merely because their syntax looks alike.

Work on a new branch. Run the tests after each group and the build after each batch.
Restore any group that breaks a check.

## Audit every installed dependency

Find:

- Dependencies that are installed but unused.
- Dependencies used for one or two features that fit in a few dozen lines.
- Multiple libraries that do the same job.

Check code, scripts, configuration, build tools, package exports, and workspace ownership.
Prove a dependency is unused before removing it.
Keep required transitive dependencies and development tools.

Remove unused dependencies outright.
For a small replacement, write the failure cases and tests first, then implement it.
Remove the dependency only after the replacement passes those tests.
Where two libraries behave the same, keep one and move every call site to it.
Keep the manifest and lockfile consistent. Avoid unrelated lockfile changes.

Work on a new branch. Run the tests and build after each dependency change.
Restore a change that fails either check.
List large or uncertain dependencies separately and let me decide whether to replace them.

## Finish with evidence

Provide the wiring diagram, changes made, retained differences, and uncertain cases.
Include the exact commands and results for each batch, including failures and restorations.
Distinguish checks you ran from evidence supplied by others or reused from a cache.
Do not claim that a passing rerun explains an earlier failure without measuring the cause.
Do not call the cleanup complete while required checks or requested work remain.
