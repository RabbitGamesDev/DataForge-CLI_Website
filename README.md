<div align="center">

# DataForge CLI — Website

### The place where the terminal tool becomes a story.

<br>

![Static Site](https://img.shields.io/badge/Stack-HTML%20%7C%20CSS%20%7C%20Vanilla%20JS-000000?style=for-the-badge&labelColor=000000&color=7CFF00)
![No Build Step](https://img.shields.io/badge/Build%20Step-None-4CAF50?style=for-the-badge)
![Hosted](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-222222?style=for-the-badge&logo=github)
[![CLI Stars](https://img.shields.io/github/stars/RabbitGamesDev/DataForge-CLI?style=for-the-badge&color=7CFF00&label=CLI%20Stars&labelColor=000000)](https://github.com/RabbitGamesDev/DataForge-CLI)
[![CLI Version](https://img.shields.io/github/v/tag/RabbitGamesDev/DataForge-CLI?style=for-the-badge&color=7CFF00&label=CLI%20Version&labelColor=000000)](https://github.com/RabbitGamesDev/DataForge-CLI)

<br>

**[rabbitgamesdev.github.io/DataForge-CLI_Website](https://rabbitgamesdev.github.io/DataForge-CLI_Website/)**

</div>

---

## What this is

DataForge CLI lives in the terminal. This is where it lives everywhere else — the install guide, the full command reference, the pricing, the roadmap, the proof that real people already use it.

Two repositories, one product, two jobs:

| | Builds the tool | Sells the tool |
|:---|:---:|:---:|
| **Repo** | `DataForge-CLI` | `DataForge-CLI_Website` *(this one)* |
| **Language** | Python | HTML / CSS / JS |
| **Ships** | The CLI itself | Docs, pricing, onboarding, trust |

If the CLI is *local-first, multi-provider, developer-first* — this site follows the same instinct, just applied to the web: **no frameworks, no build pipeline, no dependency you didn't choose yourself.** Open any `.html` file in a browser and it runs. That's the whole deploy story.

---

## Pages

| Page | Purpose |
|:---|:---|
| `index.html` | Home — the pitch |
| `features.html` | Every command, by tier |
| `testimonials.html` | Early Access voices + studio marquee |
| `plans.html` | Free / Pro / Teams pricing |
| `installation.html` | 1-click installer, Git clone, ZIP |
| `docs.html` | Full command reference, guides, troubleshooting |
| `roadmap.html` | What's shipped, what's next |
| `faq.html` | Licensing, privacy, plans |
| `buy.html` | Checkout flow explainer |
| `dashboard.html` | Customer dashboard *(UI preview, not wired up yet)* |
| `admin.html` | Private content editor — not linked in nav |

---

## Design system

One stylesheet, one identity: `assets/css/style.css`. Dark by default, `#7CFF00` as the single accent, Space Grotesk for display type, JetBrains Mono for anything that looks like a terminal. Every page shares the same nav, footer, button, and card components — new pages should reuse them, not reinvent them.

```
assets/
├── css/style.css     # the entire design system
├── js/main.js        # nav, reveal animations, copy buttons, accordions, pricing toggle
└── img/               # favicon, og-cover, and any future screenshots/logos
```

---

## Running it locally

There's nothing to install.

```bash
git clone https://github.com/RabbitGamesDev/DataForge-CLI_Website.git
cd DataForge-CLI_Website
open index.html   # or just double-click it
```

No `npm install`, no dev server required — though any static file server (`python -m http.server`, VS Code's Live Server) works fine if you want clean relative paths while editing.

---

## Editing content without touching HTML

Testimonials and the roadmap timeline change often enough that they have their own tool: `admin.html`. It's not part of the public site — nothing links to it — but it's in this repo for whoever maintains the content. Fill in a form, hit **Generate HTML**, paste the result over the matching block in `testimonials.html` or `roadmap.html`. Export/import JSON if you want to pick up where you left off later.

---

## Feedback

This site and the CLI share one feedback loop — [Issues](https://github.com/RabbitGamesDev/DataForge-CLI/issues) on the CLI repo. If a page is broken, a claim is wrong, or a link 404s, that's where it goes.

---

## License

The DataForge CLI codebase is Apache 2.0. This repository — the site's copy, branding, and design — is © RGS Labs™.

<br>

<div align="center">

Made with ❤️ by **RGS Labs™**

</div>
