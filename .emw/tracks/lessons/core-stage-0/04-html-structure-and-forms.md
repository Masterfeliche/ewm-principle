# Lesson 4 — HTML structure: headings, lists, links, images and forms

**Time:** 3 hours · **Skills:** `core.html-css` · **Before this:** Lesson 3
**Your folder:** `my-page/`

## Goal
By the end your page has a clear structure, a list, links, an image and a contact form —
everything the Stage 0 brief asks for — written so that a screen reader and a search engine
understand it, and it passes the HTML validator.

## The idea
**Structure is meaning, not looks.** Choose an element for what the content *is*, never for
how big or bold it looks. Looks are CSS's job (Lesson 5).

**Headings** `<h1>` to `<h6>` are an outline: one `<h1>` for the page, `<h2>` for each
section, `<h3>` inside those. Never skip a level to get a smaller font.

**Page regions** tell the browser what each part is for:
```html
<header> … </header>   <!-- name, maybe navigation -->
<main> … </main>       <!-- the page's real content, once per page -->
<section> … </section> <!-- a themed group, normally with its own heading -->
<footer> … </footer>   <!-- contact, copyright -->
```

**Lists:** `<ul>` for a list where order does not matter, `<ol>` where it does; each item
is an `<li>`.

**Links:** `<a href="…">text</a>`.
- `href="https://example.com"` — another site (absolute).
- `href="projects.html"` — a file next to this one (relative, like terminal paths in Lesson 1).
- `href="#contact"` — a part of this page with `id="contact"`.
- Link text should make sense on its own: "my GitHub profile", never "click here".

**Images:** `<img src="photo.jpg" alt="Asha standing outside a library" width="400" height="300">`
- `alt` describes the image for people who cannot see it, and is shown if it fails to load.
  Every image needs one. A purely decorative image gets an empty `alt=""`.
- `width` and `height` stop the page jumping about while the image loads.
- Keep images small — under about 200 KB. Many of your users will be on slow, expensive
  mobile data.

**Forms** collect input:
```html
<form>
  <label for="name">Jina</label>
  <input id="name" name="name" type="text" required>
  <button type="submit">Tuma</button>
</form>
```
- A `<label>` with `for` matching the input's `id` — clicking the label focuses the input,
  and screen readers read it out. Never leave an input without a label.
- `type` changes the keyboard on a phone and adds checks: `email`, `tel`, `number`, `date`.
- `name` is the key the data is sent under (that matters in Stage 2, when a server receives it).
- `required` stops an empty submit. This is a convenience for users, **not** security —
  anyone can bypass it. Servers must check everything again (Stage 2).

**Check your HTML** at validator.w3.org ("Validate by File Upload" or "Direct Input"). Browsers
forgive mistakes silently; the validator does not.

## Worked example
A section listing an invented shop's products, with an image and a link.

```html
<section id="bidhaa">
  <h2>Bidhaa zetu</h2>
  <img src="images/shelf.jpg" alt="Shelves of sugar, flour and cooking oil" width="480" height="320">
  <ul>
    <li>Sukari — TZS 3,500 kwa kilo</li>
    <li>Unga — TZS 2,800 kwa kilo</li>
    <li>Mafuta — TZS 7,000 kwa lita</li>
  </ul>
  <p>Tutumie ujumbe kupitia <a href="#mawasiliano">fomu ya mawasiliano</a>.</p>
</section>
```

## Predict
1. An `<img>` has a wrong `src`. What does the user see?
2. A visitor clicks a `<label>` with `for="email"`, but the input's `id` is `mail`. What happens?
3. A form has `<input type="email" required>`. A user types `asha`. What happens on submit?

<details><summary>Answers</summary>

1. A broken-image icon and the `alt` text — another reason `alt` matters.
2. Nothing: the label is not connected to anything, and a screen reader will not announce it either.
3. The browser blocks the submit and shows a message. (A script or a determined user can
   still send `asha` to a server, which is why the server must check too.)
</details>

## Exercises
All in `my-page/`. The brief lists what the page needs.

1. **Structure** — give `index.html` a `<header>`, `<main>` with at least three `<section>`s
   (about you, what you are learning, your projects), and a `<footer>`. One `<h1>`, an `<h2>`
   per section.
2. **Content** — a list of the five projects you will build on your track (from
   `.emw/tracks/README.md`), at least two links (one to another site, one to a section of your
   own page), and one image you took yourself or are allowed to use, in an `images/` folder,
   under 200 KB, with a good `alt`.
3. **Contact form** — name, email, phone (`type="tel"`) and a message (`<textarea>`), each with
   a label, and a submit button. It does not need to send anything yet.
4. **Validate** — run the page through validator.w3.org and fix every error.

## Find the bug
The validator reports problems in this snippet, and a screen reader user cannot use the form.
Find every problem (there are four).

```html
<h1>Asha</h1>
<h3>About me</h3>
<img src="me.jpg">
<form>
  Email: <input type="text" id="email">
  <button>Send</button>
</form>
```

## Done when
- [ ] The page has header, main with three sections, and footer, with a correct heading outline.
- [ ] It has a list, two kinds of link, an image with `alt` under 200 KB, and a labelled contact form.
- [ ] validator.w3.org shows no errors.
- [ ] You can explain, without notes, why every input needs a label.

## Record
```bash
python .emw/tools/emw_track.py log core.html-css --type implement --assistance A1 --task "Structured my page with semantic regions, a list, links, an image with alt text and a labelled form; passes the validator"
```
