# Prompt format

Store one prompt per Markdown file under `prompts/`.
Use lowercase, hyphenated filenames and a descriptive level-one title.
Use sections for the task, constraints, evidence, and expected output when useful.
Index every prompt with a relative README link.

Use generic wording or placeholders for personal and project details.
Use ordinary Markdown, without model-specific frontmatter or a prompt runtime.
The collection has no application, visual system, or deployment target.

Run `python3 scripts/ci.py` before publishing changes.
Review text for identifying context that pattern checks cannot detect.
