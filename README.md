# raceproof-media

Public media host and template library for @raceproof.ai social posts. GitHub Pages serves every file in this repo at
`https://<owner>.github.io/raceproof-media/<path>`, and Buffer pulls post images and videos from those links.

Everything here becomes public as soon as it is pushed, a few days before it posts. Never commit anything private.

## Weekly workflow (the Saturday "Raceproof weekly posts" task)

1. Read the social media brief (all tabs), the 90-day calendar and the Research library. They are the source of truth for copy, numbers and rules.
2. For each feed post in the coming Monday to Sunday week, write one HTML file per slide in `posts/<monday-date>/`, built from the closest template in `templates/posts/` and named `<day>-<slug>-<n>.html` (e.g. `mon-research-pacing-1.html`).
3. Render: `python3 scripts/render_stills.py posts/<monday-date>/*.html` (writes a 1080 x 1350 PNG next to each HTML file).
4. For a Reel, copy a template from `templates/reels/`, change only its data and text, and render it:
   `python3 scripts/render_reel.py <html> posts/<monday-date> <day>-<slug>-reel <duration> <cover_t>`.
   Reels are not loaded into Buffer. Jonathan posts them himself.
5. Write `posts/<monday-date>/posts.json` (format below), then commit and push. Wait until every file loads from its Pages link before using it.
6. In Buffer (organization "My organization"), create one **draft** per feed post on each channel, Instagram `6ac9cdde6a5c39ccb66d7655` and Facebook page `6acd1c4f778b240e2fe9d9aa`, with `saveToDraft: true`, `mode: customScheduled` and `dueAt` set to the post's date at 08:00 America/Los_Angeles. Carousels list every slide image in order. Use Instagram type `post` and Facebook type `post`. Give each image alt text. Never publish or schedule directly: Jonathan approves drafts in Buffer.

## posts.json

```json
{
  "week": "2026-10-19",
  "posts": [
    {
      "date": "2026-10-19",
      "type": "research",
      "title": "Research: Pacing (Dong & Li 2026)",
      "slides": ["mon-research-pacing-1.png", "mon-research-pacing-2.png"],
      "caption": "…",
      "altText": "…",
      "flags": ["anything Jonathan must check or fill in"],
      "buffer": {"instagram": "<post id>", "facebook": "<post id>"}
    }
  ],
  "reels": [{"date": "…", "file": "…-reel.mp4", "cover": "…-reel-cover.png", "caption": "…"}]
}
```

## Templates

- `templates/posts/`: approved feed designs to copy from. `pain-terrain-1-problem.html` and `pain-terrain-2-fix.html` are the model for every pain post (2-slide rule in the brief). `education-gut-*.html` is the education carousel. `single-keep-your-coach.html` is a single post with icons. `founding-offer.html`, `launch-intro.html` and `stat-pain-28pct.html` are the launch row.
- `templates/reels/adaptation-timeline.html`: the approved 19-second adaptation timeline reel. It defines `window.render(t)` and shows its logo with `?still=1`.
- Assets: `assets/brand/` (lockups, mark, app icon, phone frame), `assets/fonts/` (Inter, Inter Display, JetBrains Mono, loaded with `fonts.css`). Link them relatively, e.g. `../../assets/brand/lockup.png` from a file two folders deep.

## Rules that every file must follow

Brand system only: asphalt `#1F2328`, surface `#F4F2ED`, lime `#C8F03C` only for "ready", heat `#B83C0B` and heat-soft `#FCE7DC` for problems, pillar colors from the brief. No em or en dashes, no exclamation marks, no AI-sounding phrasing. Every number comes from the brief's stats table or a Research library row, with its source on the slide or in the caption. Feed slides are 1080 x 1350 with the small logo; reels are 1080 x 1920 with text kept out of the top 220 px and bottom 420 px.

Fonts: Inter and JetBrains Mono are under the SIL Open Font License 1.1.
