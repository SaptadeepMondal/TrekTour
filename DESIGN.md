---
name: TrekTour
description: An Advanced Online Trek Management System
colors:
  primary: "#06b6d4"
  neutral-bg: "#09090b"
  surface: "#18181b"
  neutral-text: "#f4f4f5"
  neutral-muted: "#a1a1aa"
  border: "#27272a"
typography:
  display:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontWeight: 500
    letterSpacing: "-0.03em"
  mono:
    fontFamily: "'JetBrains Mono', monospace"
    fontWeight: 400
    letterSpacing: "0.1em"
rounded:
  sm: "6px"
  md: "12px"
spacing:
  sm: "0.5rem"
  md: "1rem"
  lg: "1.5rem"
  xl: "2.5rem"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#000000"
    rounded: "{rounded.sm}"
    padding: "0.5rem 1rem"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.neutral-muted}"
    rounded: "{rounded.sm}"
    padding: "0.5rem 1rem"
---

# Design System: TrekTour

## Overview

**Creative North Star: "The Modern SaaS Command Center"**

High-contrast, lightning-fast, and technically precise. This aesthetic sheds the heavy outdoorsy metaphors in favor of a professional, enterprise-ready data-density feel. It uses a strict dark-mode color palette, clean grid layouts, and sharp monospaced accents.

**Key Characteristics:**
- True off-black dark mode (`zinc-950`).
- Strict 1px `border-zinc-800` outlining cards and surfaces.
- Translucent `backdrop-blur` for elevated containers (like bento cards and nav bars).
- A single, electric cyan accent color.

## Colors

A very restrained palette. Only one accent color is permitted.

### Primary (Accent)
- **Electric Cyan** (`#06b6d4`): Used exclusively for primary calls to action, active states, and critical highlights. Hover shifts to `#0891b2`.

### Neutral
- **Base (Zinc-950)** (`#09090b`): The absolute background of the page.
- **Surface (Zinc-900)** (`#18181b`): Used for elevated elements, form inputs, and solid backgrounds.
- **Text Main (Zinc-50)** (`#f4f4f5`): High-contrast white for headings and primary copy.
- **Text Muted (Zinc-400)** (`#a1a1aa`): For secondary descriptions and UI labels.
- **Border (Zinc-800)** (`#27272a`): 1px borders used everywhere to separate layout structures.

## Typography

**Display Font:** Inter
**Body Font:** Inter
**Label/Mono Font:** JetBrains Mono

**Character:** Completely neutral, highly legible, and engineered.

### Hierarchy
- **Display** (500, -0.03em): Large hero titles.
- **Headline** (500, -0.03em): Bento card titles and section headers.
- **Body** (400, 1.5 line-height): Standard paragraph text.
- **Label / Mono** (400, 0.1em tracking): Eyebrows, footer status markers, and system data.

## Layout

**The Split Screen & Bento Grid Rule.**
- We explicitly avoid centered hero text over generic backgrounds. The hero uses a left-text, right-image split grid.
- Features are mapped into asymmetric Bento grids using CSS grid (`span 2` for featured items).

## Elevation & Depth

No soft drop shadows. Depth is conveyed entirely through `backdrop-filter: blur(12px)` and strict 1px borders layered over grid backgrounds.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. If elevation is needed, we rely on translucency (backdrop-blur) rather than box-shadows.

## Shapes

- **Radius Strategy:** Tight and controlled.
- **Buttons:** 6px radius.
- **Cards/Containers:** 12px radius.
- **Form/Input:** 6px radius.

## Components

### Buttons
- **Shape:** 6px radius.
- **Primary:** Cyan background, Black text. Hover shifts background darker and triggers `translateY(-1px)`. Active triggers `scale(0.98)`.
- **Ghost:** Transparent background, Muted text. Hover shifts text to bright white and background to Surface (Zinc-900).

### Bento Cards
- **Corner Style:** 12px radius.
- **Background:** Translucent base (Zinc-900 at 0.7 opacity) with a 12px backdrop blur.
- **Border:** 1px solid Zinc-800. Hover shifts border color to a faint Cyan.

## Do's and Don'ts

### Do:
- **Do** rely on 1px borders to establish layout boundaries.
- **Do** ensure hero headlines are succinct (max 2 lines).
- **Do** check button contrast (e.g., Cyan background requires dark/black text for WCAG AA).

### Don't:
- **Don't** use soft, blurry box shadows.
- **Don't** use more than one eyebrow per three sections.
- **Don't** introduce secondary accent colors (no purple, no green). Stick strictly to Cyan.
