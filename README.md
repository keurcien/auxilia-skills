# auxilia-skills

The company skill library for [auxilia](https://github.com/keurcien/auxilia),
laid out the [Agent Skills](https://agentskills.io/specification) way so it
also works with `npx skills add` and any agent that reads the same layout.

```
skills/
├── weekly-brief/            # instructions only — runs on any agent
├── margin-audit/            # instructions + scripts — needs an agent with code execution
├── finance/kyc-check/       # one category level is fine
└── .experimental/…          # surfaced as its own container
environment.yaml             # what the runtime image provides (generated in CI, for now by hand)
```

Each skill is a folder with a `SKILL.md`: YAML frontmatter (`name`,
`description`, optional `license`, `compatibility`, `metadata`,
`allowed-tools`) and the procedure in Markdown. Scripts under `scripts/` need
an agent that runs code; requirements go in `metadata.auxilia-requires`.

auxilia syncs this repository as a *skill source*: every skill here becomes
available in the workspace library, pinned by content digest and adopted per
skill against a diff. Nothing here is edited from the app.
