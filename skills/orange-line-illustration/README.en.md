# Orange Line Illustration · 橙线插画

[中文](README.md) | **English**

Last week I wrote an article — "Six Principles of Building Products with AI" — and many friends loved the illustrations, asking how I made them. So I packaged it into a skill and open-sourced it.

On Saturday I gave a talk at a community event. The PPT was made with this same illustration style. Again, people loved it.

In a world flooded with AI infographics and HTML text blocks, maybe a drawing with lots of white space is what actually focuses attention. They say the best PPTs have just one sentence per slide.

So I spent the weekend iterating on this, making it more stable, more beautiful, more fun.

What I'm going for: you get it at a glance, and it makes you smile.

Two workflows:
- **Single illustrations** — conceptual editorial images for articles, principles, covers
- **PPT slide decks** — turn articles/outlines into illustrated HTML presentations

![Cover example](examples/cover-walking-through-the-draft.png)

---

## Demo: 20 Slices of "Inside DingTalk"

We used this skill to illustrate 20 key moments from a viral 75,000-word essay about product management at Alibaba's DingTalk. Each image captures one quote from the original text.

👉 [**Full article (WeChat, Chinese)**](https://mp.weixin.qq.com/s/GHZvaKlrHFIC71VMlmKl6A)

Selected examples:

| | |
|---|---|
| ![Swift 300 days](examples/xiaocheng-swift-300days.png) | ![Greedy scale](examples/xiaocheng-greedy-scale.png) |
| "300+ days of non-stop flight" | "Want everything, get nothing" |
| ![Sender power](examples/xiaocheng-sender-power.png) | ![Flag overloaded](examples/xiaocheng-flag-overloaded.png) |
| "Always on the sender's side" | "A flag gathers people — and too many things" |
| ![Tech debt](examples/xiaocheng-tech-debt.png) | ![Kong Yiji](examples/xiaocheng-kong-yiji.png) |
| "AI must cut through legacy tech debt" | "DingTalk walks in like Kong Yiji" |
| ![Constant in storm](examples/xiaocheng-constant-in-storm.png) | ![Context inequality](examples/xiaocheng-context-inequality.png) |
| "Seek the constants, not the fluctuations" | "Intelligence is equal; context is not" |
| ![Balloon tethered](examples/xiaocheng-balloon-tethered.png) | ![Empty table](examples/xiaocheng-empty-table.png) |
| "The opportunity is trapped in an old city" | "Only 3 people stayed longer than 3 months" |

---

## Style Examples (General)

| | |
|---|---|
| ![Amplifier](examples/01-amplifier.png) | ![Subtraction](examples/02-subtraction.png) |

Notice the scale: people are always **tiny**, objects always monumental. This imbalance is the signature drama of the style.

---

## Character IP System

Three reusable character IPs, each with a fixed visual form. They are not decoration — they must carry the core action.

### 小橙 / Xiao Cheng (default character)

A geometric line-drawn figure with an orange dot on its chest. Quiet, focused, does the work.

- Circle head (outline only) + two dot eyes + no mouth
- Narrow rectangular body outline + thin stick limbs
- Single orange dot `#F97316` on chest = the entire image's accent color

| | |
|---|---|
| ![Trophy weight](examples/xiaocheng-trophy-weight.png) | ![Inbox overload](examples/xiaocheng-inbox-overload.png) |
| "Hardest to escape: not failure, but success" | "Dozens of group chats exploding with unread messages" |

### 线人 / Xian Ren (line-person)

Minimal abstract human — circle head + single arc body + single-line limbs. The fewest strokes that say "someone is here."

| Old City Wall |
|---|
| ![](examples/xianren-old-city-wall.png) |

> "Standing at an attractive frontier — but it's in the middle of an old city."

### 线猫 / Xian Mao (line-cat)

A kitten drawn in 10–12 strokes — open arcs, two dot eyes, two ear-strokes. The viewer's brain fills in the rest.

| Schrödinger's User |
|---|
| ![](examples/xianmao-schrodinger-user.png) |

> "And so we set off, carrying a box of Schrödinger's users."

---

## Style Rules (quick reference)

- **Line**: thin black ink, hand-drawn wobble, not mechanical
- **Background**: pure white — no texture, no gradients, no shadows
- **Accent**: one warm orange `#F97316`, placed on the single most meaningful element
- **Figures**: TINY. Objects are monumental, people are small. This imbalance is the signature drama.
- **Caption**: bottom-right, light gray, quiet and readable
- **Mood**: witty, restrained, intelligent

See `SKILL.md` and `references/` for the full specification.

---

## Two Workflows

### Workflow A: Single Concept Illustration

Generate a 16:9 editorial image for a judgment, principle, or metaphor in an article.

```
Generate three orange-line illustrations for this article
```

Flow: extract metaphor → design scene → generate candidates → human picks

### Workflow B: PPT Slide Deck

Turn an article/outline into an illustrated HTML slide deck, one scene per slide.

```
Turn this article into an orange-line PPT
```

Flow: read article → write slide outline → confirm → batch-generate illustrations → user picks → output HTML

See `references/ppt-workflow.md` for details.

---

## What's Inside

```
.
├── SKILL.md                          # Main spec: style, metaphor method, prompt template
├── references/
│   ├── xiao-orange-ip.md             # 小橙 character definition
│   ├── xiao-orange-prompt-template.md # 小橙 prompt template
│   ├── xianren-ip.md                 # 线人 character definition
│   ├── xianmao-ip.md                 # 线猫 character definition
│   └── ppt-workflow.md               # PPT slide deck workflow
├── examples/                         # Example images
├── LICENSE.md
└── README.md
```

## Installation

Works with any AI agent that supports the SKILL.md convention (Cola, Claude Code, Codex, etc.). Drop the directory into your agent's skills folder:

```bash
# Cola
~/.cola/skills/orange-line-illustration/

# Claude Code
~/.claude/skills/orange-line-illustration/
```

Then tell your agent — "generate three orange-line illustrations for this article" or "turn this article into an orange-line PPT" — and it follows the spec.

## License

**Dual license**: free for open-source & personal use; commercial license required for closed-source/proprietary use. See [LICENSE.md](LICENSE.md).
