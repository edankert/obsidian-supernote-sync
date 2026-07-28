---
type: "[[design]]"
id: DES-0001
aliases: ["DES-0001"]
title: "Supernote Sync design system — plugin and dashboard"
role: system
status: draft
owner: user:edwin
created: 2026-07-28
updated: 2026-07-28
source: ["obsidian-plugin/styles.css", "web-dashboard/src/index.css"]
asset: "DES-0001-style-guide.html"
stylesheets:
  - obsidian-plugin/styles.css
  - web-dashboard/src/index.css
implements: []
supersedes: ""
superseded_by: ""
reviewed_by: ""
review_date: ""
review_verdict: ""
related: []
---

# Supernote Sync design system

**One note, two surfaces.** They belong to one product and share intent, but their constraints are opposite: the plugin lives inside someone else's application and the dashboard owns its window. Read from both stylesheets as the page renders; no value in this note is load-bearing.

## The Obsidian plugin — a system defined by what it does *not* declare

`obsidian-plugin/styles.css` declares **zero custom properties**. That is the system, not a gap.

Every colour it uses is a **host token**: `--text-success`, `--text-error`, `--interactive-accent`. The plugin styles four things — a status-bar state, a ribbon hover, and two status colours — and each defers to whatever theme the user has chosen. A user running a dark community theme gets the plugin in that theme without the plugin knowing it exists.

**The rule, stated so it can be broken deliberately rather than by accident: never introduce a colour the host has not already named.** A hardcoded hex here would look correct in the default theme and wrong in the thousands of others, and the person who sees it wrong is never the person who wrote it.

The consequence for this page: the style guide will show almost nothing for the plugin, and that is the correct output. There is nothing to show, because the plugin declares nothing.

## The web dashboard — Tailwind, with two escapes

`web-dashboard/src/index.css` is `@import "tailwindcss"` plus **two** custom properties: `--color-primary` (`#6366f1`) and `--color-primary-hover`. Everything else is utility classes, and the base `body` rule carries literal hex values rather than tokens.

So its palette is **mostly not readable by this page**, and the page will say so rather than invent one. That is a real observation about the dashboard, not a limitation of the tooling: a design system expressed only as utility classes has no vocabulary a document can point at, and the two tokens that do exist are the ones someone needed to name because Tailwind had no word for them.

**Worth deciding, not assumed:** whether the dashboard should declare its palette as tokens. It would make this page useful, and it would give the two surfaces a shared word for "primary" — but Tailwind projects legitimately live without one, and adopting tokens to satisfy a document would be the wrong reason.

## What the two share

Nothing, today, at the token level — and given the plugin's rule, nothing is the right answer for colour. What they could share is *behavioural*: what a connected state looks like, what an error reads like, whether a sync in progress is a spinner or a count. None of that is written down anywhere yet.

## Conformance

Nothing here is checked. The page reads both stylesheets so the page cannot drift; this prose can. If they disagree, the stylesheets are right.
