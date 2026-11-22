# Lesson 5 — CSS basics and mobile-first layout

**Time:** 3–4 hours · **Skills:** `core.html-css` · **Before this:** Lesson 4
**Your folder:** `my-page/`

## Goal
By the end your page has its own stylesheet, readable text, a sensible layout on a phone,
and a slightly wider layout on a computer — and you can use developer tools to see why any
element looks the way it does.

## The idea
**CSS** says how HTML looks. Keep it in its own file and link it from the `<head>`:

```html
<link rel="stylesheet" href="style.css">
```

A CSS **rule** is a selector and some declarations:

```css
h1 {
  color: #1d4e3f;
  font-size: 2rem;
}
```

**Selectors** — which elements a rule applies to:

| Selector | Matches |
|---|---|
| `p` | every `<p>` |
| `.price` | every element with `class="price"` |
| `#contact` | the one element with `id="contact"` |
| `footer a` | links inside the footer |

Prefer classes for styling. Keep ids for links and labels.

**The box model.** Every element is a box: its **content**, then **padding** (space inside
the border), then the **border**, then **margin** (space outside). Add this at the top of
every stylesheet so widths include padding and border, which is what you will expect:

```css
*, *::before, *::after { box-sizing: border-box; }
```

**Units.** `px` is a fixed size. `rem` is relative to the user's chosen text size — use it for
fonts and spacing, so people who set larger text get larger text. `%` is relative to the parent.

**Readable text** — the most important styling there is:
- body text around `1rem` to `1.125rem`, `line-height: 1.5`;
- lines no wider than about 70 characters: `max-width: 40rem` on the main content;
- enough contrast between text and background (check with the contrast tool in developer
  tools, or webaim.org/resources/contrastchecker).

**Mobile first.** Most of your users will be on phones, often cheap ones on slow connections.
So write the CSS for a narrow screen *first*, with no media query. Then add rules for wider
screens inside a **media query**:

```css
/* phone: one column, the default */
.projects { display: grid; gap: 1rem; }

/* 48rem (about 768px) and wider: two columns */
@media (min-width: 48rem) {
  .projects { grid-template-columns: 1fr 1fr; }
}
```

**Images that fit:** `img { max-width: 100%; height: auto; }` stops images overflowing a phone.

**Developer tools for CSS.** Inspect an element: the **Styles** panel shows every rule that
applies and which ones were overridden (crossed out). The **Computed** panel shows the box
model. The **device toolbar** (the phone icon) shows your page at phone sizes.

## Worked example
Styles for the invented shop page from Lessons 3–4.

```css
*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  color: #222;
  background: #fdfaf4;
}

main {
  max-width: 40rem;
  margin: 0 auto;      /* centre it */
  padding: 1rem;
}

h1 { color: #1d4e3f; font-size: 1.75rem; }

img { max-width: 100%; height: auto; border-radius: 0.5rem; }

.price { font-weight: bold; white-space: nowrap; }

@media (min-width: 48rem) {
  h1 { font-size: 2.5rem; }
  main { padding: 2rem; }
}
```

`system-ui` uses the phone's own font, so there is nothing extra to download.

## Predict
1. A rule `p { color: red; }` and a rule `.note { color: blue; }`. What colour is `<p class="note">`?
2. A box is `width: 300px` with `padding: 20px` and no `box-sizing` rule. How wide is it on screen?
3. With `@media (min-width: 48rem) { … }`, does the rule apply on a phone 360px wide?

<details><summary>Answers</summary>

1. Blue. A class selector is more specific than an element selector, so it wins.
2. 340px — without `border-box`, padding is added on top of the width.
3. No. 48rem is about 768px, and the phone is narrower.
</details>

## Exercises
1. **`style.css`** for `my-page/` — link it, add `border-box`, readable body text, a
   centred `main` with a maximum width, and image rules.
2. **Projects layout** — give your projects section a class and show it as one column on a
   phone and two columns from 48rem.
3. **Form styling** — make the contact form easy to use on a phone: each label above its input,
   inputs full width, at least `0.75rem` of padding, and a button big enough to tap.
4. **Check** — in the device toolbar, view the page at 360px wide and at 1280px wide. Nothing
   should overflow sideways on the phone. Check one text colour against its background in the
   contrast tool. Note the results in `exercises/stage-0/lesson-05/notes.md`.

## Find the bug
On a phone, this page scrolls sideways and the text is tiny. Find the two causes.

```html
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>
```
```css
main { width: 900px; margin: 0 auto; }
```

## Done when
- [ ] `style.css` is linked and has every rule from exercise 1.
- [ ] The projects are one column on a phone and two on a wide screen.
- [ ] Nothing overflows sideways at 360px.
- [ ] You can explain, without notes, what "mobile first" means and why it suits your users.

## Record
```bash
python .emw/tools/emw_track.py log core.html-css --type implement --assistance A1 --task "Styled my page mobile-first with a linked stylesheet, readable text, a two-column layout from 48rem and a phone-friendly form"
```
