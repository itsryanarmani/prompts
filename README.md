# Reusable prompts

Reusable, project-neutral prompts for careful software work.

## Prompts

| Prompt | Use it to |
| --- | --- |
| [Code cleanup](prompts/code-cleanup.md) | Map code knots, prove unused code, consolidate duplicates, and audit dependencies. |

Open a prompt and copy its contents into your agent session.
Supply private project context in that session, outside this collection.

## Add a prompt

Save one prompt per Markdown file in `prompts/`, with a lowercase, hyphenated filename.
Start with a descriptive title. State the task, constraints, verification, and expected output.
Add a relative link to the table above.

Prompts must contain **no personal information or real project or repository names**.
Remove names, usernames, email addresses, phone numbers, hostnames, local paths, and credentials.
Replace project-specific details with placeholders such as `<PROJECT>`, `<PATH>`, and `<URL>`.
Keep private examples, logs, screenshots, and source material outside the repository.

Review every prompt for identifying context before publishing it.
Automated checks catch common patterns; they cannot identify every name or private detail in prose.

## Check changes

Use Python 3.10 or newer. No packages need installation.

```sh
python3 scripts/ci.py
```

The command runs the process tests, privacy checks, Markdown hygiene, and README link checks.
CI runs it on pushes and pull requests. A separate job scans the full Git history for secrets.
Both jobs must pass before merging. This text collection has no separate deployment step.

## License

[MIT](LICENSE).
