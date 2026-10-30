# raceproof-media

Public media host and template library for @raceproof.ai social posts. Buffer pulls post images from raw GitHub links pinned
to a commit, so a scheduled post never changes under it:
`https://raw.githubusercontent.com/raceproof/Raceproof-media/<commit-sha>/<path>`

Everything here becomes public as soon as it is pushed, a few days before it posts. Never commit anything private.

## Weekly cadence

Feed posts on Monday, Wednesday, Friday and Saturday (Monday, Wednesday and Friday after Nov 15), each loaded into Buffer as a draft for 08:00 Pacific. Sunday is always a **filmed** Reel: scripts live in the "Reel scripts" tab of the social media brief, Jonathan films them in batches of 4 and posts them from the Instagram app with trending audio. Filmed Reels never go to Buffer and are never rendered here.

## Weekly workflow (the Saturday "Raceproof weekly posts" task)

1. Read the social media brief (all tabs), the 90-day calendar and the Research library. They are the source of truth for copy, numbers and rules.
2. For each feed post in the coming Monday to Sunday week, write one HTML file per slide in `posts/<monday-date>/`, built from the closest template in `templates/posts/` and named `<day>-<slug>-<n>.html` (e.g. `mon-research-pacing-1.html`).
3. Render: `python3 scripts/render_stills.py posts/<monday-date>/*.html` (writes a 1080 x 1350 PNG next to each HTML file).
4. For a Reel, copy a template from `templates/reels/`, change only its data and text, and render it:
   `python3 scripts/render_reel.py <html> posts/<monday-date> <day>-<slug>-reel <duration> <cover_t>`.
   Animated race Reels go to Buffer as Reel drafts; filmed Reels are posted by Jonathan from the Instagram app with trending audio.
5. Write `posts/<monday-date>/posts.json` (format below), then commit and push. Use the pushed commit's SHA in every media link.
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
      "caption": "… (Instagram caption)",
      "caption_facebook": "… (only when the post has a link)",
      "link": "https://raceproof.ai/blog/<slug> (only when the post points to a page)",
      "altText": "…",
      "theme": "light | slate | lime | peach",
      "flags": ["anything Jonathan must check or fill in"],
      "buffer": {"instagram": "<post id>", "facebook": "<post id>"}
    }
  ],
  "reels": [{"date": "…", "file": "…-reel.mp4", "cover": "…-reel-cover.png", "caption": "…", "theme": "light | slate | lime | photo"}]
}
```

## Templates

- `templates/posts/`: approved feed designs to copy from. `pain-terrain-1-problem.html` and `pain-terrain-2-fix.html` are the model for every pain post (2-slide rule in the brief). `education-gut-*.html` is the education carousel. `single-keep-your-coach.html` is a single post with icons. `founding-offer.html`, `launch-intro.html` and `stat-pain-28pct.html` are the launch row.
- `templates/reels/adaptation-timeline.html`: the approved 19-second adaptation timeline reel. It defines `window.render(t)` and shows its logo with `?still=1`.
- `templates/reels/race-breakdown.html`: the approved race breakdown Reel (locked Oct 25, 2026; first used for Black Canyon 100K). Scenes: intro fully drawn at frame 0 (eyebrow, race name, date), the race's hook and its 4 key numbers (about 4 s); "When to start" with the pillars in one at a time, a short hold, then the key pillar selected and carried up into the deep dive; the deep dive on what the race asks (course profile from `races/<slug>/route.json`, per-km ratio, key sessions); the build-toward number and weekly ramp from the Adaptation rates tab; the closing line. Copy it, change only the DATA block (race, numbers, rows, `keyRow`, key pillar, profile, ramp), then render:
  `python3 scripts/render_reel.py <html> <scratch> body 27.5 3.0` and `python3 scripts/add_endcard.py <html> <scratch>/body.mp4 posts/<monday>/<day>-race-<slug>-reel.mp4 en` (crossfades the standard end card and keeps the closing line over it). About 32 s in total. Race Reels go to Buffer as Instagram and Facebook Reel drafts.
- Assets: `assets/brand/` (lockups, mark, app icon, phone frame), `assets/fonts/` (Inter, Inter Display, JetBrains Mono, loaded with `fonts.css`). Link them relatively, e.g. `../../assets/brand/lockup.png` from a file two folders deep.

## Rules that every file must follow

Brand system only: asphalt `#1F2328`, surface `#F4F2ED`, lime `#C8F03C` for "Ready", primary buttons and the Lime theme, heat `#B83C0B` and heat-soft `#FCE7DC` for problems, pillar colors from the brief. Every feed post and Reel cover uses one post theme (see "Post themes"). No em or en dashes, no exclamation marks, no AI-sounding phrasing. Every number comes from the brief's stats table or a Research library row, with its source on the slide or in the caption. Feed slides are 1080 x 1350 with the small logo; reels are 1080 x 1920 with text kept out of the top 220 px and bottom 420 px. Reels never open on a blank frame: frame 0 already shows the eyebrow and headline fully drawn (no fade in from empty).

## Caption and slide rules

- **Units:** always give both, imperial first with metric in parentheses right after it: 78°F (26°C), 70.3 mi (113.1 km), 1,519 ft (463 m), 16 oz (473 ml). On slides the imperial number is the big one and the metric sits next to or under it. Never one system alone.
- **Race posts open with the race:** the first sentence names the race and its date, then the pillar or variable that matters most there. The first paragraph states the problem plainly so the reader knows what is being broken down.
- **Adaptation windows ("when to start") in captions:** one line per variable, each starting with ✅ (or a plain bullet), e.g. `✅ Heat: sessions Jan 17 to Feb 14, then keep it`.
- **Sources paragraph:** starts with `SOURCES:` and lists every source used, e.g. `SOURCES: Wetsuit figure: Quagliarotti 2021. Weather: Open-Meteo, race mornings 2024 and 2026.`
- **No affiliation line:** never write "Raceproof isn't affiliated with ..." (or the Spanish version) for any race or organizer, in captions, slides or alt text. Still never use race logos or official photos.
- **Never include** a Spanish line or paragraph in captions, or the line "Never swim open water alone" (captions or slides).

## Links in captions

Any post about a blog article or a race page points to that exact page, never the homepage.
- `link` is the full URL: `https://raceproof.ai/blog/<slug>` (slug = the article CSV's `slug`) or `https://raceproof.ai/races/<slug>` (the queue row's Page link). Copy it from the source; never build it from the title.
- Before drafting, fetch the URL and confirm it loads that article or race (not a 404 or the homepage). If it doesn't, don't create the Buffer drafts: flag it.
- Instagram (`caption`): `Full article: raceproof.ai/blog/<slug> (link in bio).` or `Full breakdown: raceproof.ai/races/<slug> (link in bio).` Caption links aren't clickable on Instagram.
- Facebook (`caption_facebook`): the same caption with the full clickable URL on its own line: `Read the full article: https://raceproof.ai/blog/<slug>`.
- Before saving, check that `link` appears in both captions and that the Facebook caption has `https://`.

Fonts: Inter and JetBrains Mono are under the SIL Open Font License 1.1.

## Route files

`races/<slug>/route.json` holds each race's course for the animated course maps (written by the weekly race pages task from the official course file):

```json
{"slug":"…","name":"…","race_type":"Marathon|Ultra|70.3|Full distance","source":"…",
 "legs":[{"leg":"course|swim|bike|run","km":42.2,"points":[[lon,lat,km,m],…]}],
 "places":[{"name":"…","lon":0,"lat":0,"kind":"start|finish|town|landmark"}],
 "sections":[{"leg":"…","from_km":0,"to_km":0,"label_en":"…","label_es":"…"}]}
```

Each point's km and m match the race page's charted profile. Up to 600 points per leg. Maps are drawn by us from these points (no third-party map tiles), so they need no image credit.

## Post themes

Every feed post (all its slides) and every Reel cover uses one theme. Swap only these colors; layouts stay the same.

| Token | Light | Slate | Lime |
|---|---|---|---|
| background | `#F4F2ED` | `#1F2328` | `#C8F03C` |
| text | `#15171A` | `#F2F0EB` | `#15171A` |
| muted text | `#5B5F64` | `#A4A9AE` | `#3B4512` |
| lines | `#DDD9D0` | `#3A4047` | `#A6C72E` |
| cards | `#FFFFFF` | `#2A2F35` | `#FFFFFF` |
| highlighted numbers, eyebrows | heat `#B83C0B` | `#FF8A5B` | asphalt `#1F2328` (never heat on lime) |
| logo | `assets/brand/lockup.png` | `assets/brand/lockup-on-dark.png` | `assets/brand/lockup.png` on a white pill (see below) |
| "Ready" chip | lime | lime | asphalt with lime text |

Lime logo: the normal `lockup.png` inside a white pill, never straight on lime (the mark's lime segment would vanish): `<span style="display:inline-flex;align-items:center;background:#FFFFFF;border-radius:999px;padding:9px 18px;margin:-9px 0 -9px -18px"><img src="../../assets/brand/lockup.png" alt="raceproof" style="width:230px;height:53px;display:block"></span>` (the negative margin keeps the logo itself where the template puts it).

Peach (heat-soft `#FCE7DC` background) is only for pain posts. Filmed Reels and photo covers count as `photo`.

Rule: a new grid post's theme must differ from the post just before it and from the post 3 back (directly above it in the grid). When two themes fit, use the one used least in the last 9 posts. Lime on at most about 1 post in 3 (best for waitlist, founding offer and pro breakdown covers). Never cycle Light, Slate, Lime in a fixed order (it makes vertical stripes). Read earlier themes from the last two weeks of posts.json (feed posts and Reels in date order) and record `theme` on every new entry.
