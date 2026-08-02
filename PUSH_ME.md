# Getting this onto GitHub

This folder is already a git repository with two commits. Delete this file once it's pushed.

## Step 1 — Make the empty repo

Go to https://github.com/new and create a repository named **BoomerEZ**.

Leave every checkbox unchecked — no README, no .gitignore, no license. Those already exist here, and adding them on GitHub creates a conflict you'd have to untangle.

## Step 2 — Push

From inside this folder:

```
git remote add origin https://github.com/JamesTRichmond/BoomerEZ.git
git push -u origin main
```

## Step 3 — Turn on Pages

In the repo: **Settings → Pages → Source: Deploy from a branch → main → / (root) → Save**.

A minute later the landing page is live at `https://jamestrichmond.github.io/BoomerEZ/` and Mode Studio at `https://jamestrichmond.github.io/BoomerEZ/apps/mode-studio/`.

That URL is a real one you can send to someone 65+ without asking them to download anything — which makes the first usability sessions possible without a laptop handoff.

## Note for the toolchain lane

The scaffold is done. Do not create the repo structure from scratch — clone this one and build into `tools/` and `packages/`. See [docs/AGENT_LANES.md](docs/AGENT_LANES.md) for what belongs where.
