# Lesson 3 — Your editor and your first HTML page

**Time:** 2 hours · **Skills:** `core.html-css`, `core.terminal` · **Before this:** Lessons 1–2
**Your folder:** `my-page/` (a new folder, outside your learning repository — see below)

## Goal
By the end you have a code editor set up, have written a complete HTML page by hand, opened
it in a browser, and used the browser's developer tools to look inside it.

## The idea
**An editor** is where you write code. Install **VS Code** (code.visualstudio.com) — it is
free and runs everywhere. On Windows with WSL, install the "WSL" extension and open folders
from the Ubuntu terminal with `code .` so the editor and terminal see the same files.

Useful from day one: **Ctrl+S** saves (look for the dot on the tab: it means unsaved),
**Ctrl+P** opens a file by name, and **Ctrl+`** opens a terminal inside the editor.

**HTML** describes what is on a web page: headings, paragraphs, links, images. It is not a
programming language — it does not calculate anything. It is made of **elements**, written
with **tags**:

```html
<p>Habari, mimi ni Asha.</p>
```

`<p>` opens a paragraph, `</p>` closes it, and the text between is its content. Some tags
take **attributes**, extra information inside the opening tag: `<a href="https://…">`.

Every page needs the same skeleton:

```html
<!DOCTYPE html>
<html lang="sw">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Shown on the browser tab</title>
  </head>
  <body>
    Everything visible goes here.
  </body>
</html>
```

| Line | Why it is there |
|---|---|
| `<!DOCTYPE html>` | tells the browser this is modern HTML |
| `lang="sw"` | the page language (Kiswahili), for screen readers and search engines; `en` for English |
| `charset="utf-8"` | so letters such as `ë` and every emoji show correctly |
| `viewport` | so the page fits a phone screen instead of showing a tiny desktop page |
| `<title>` | the text on the browser tab and in search results |

**Indent** the inside of each element by two spaces. The browser does not care; people
reading your code do.

**Developer tools.** In the browser, right-click anything and choose **Inspect**. You see
the HTML the browser actually understood, and you can change it live to experiment (the
change disappears when you reload). You will use this every day.

## Where this page lives
Your personal page becomes its own Git repository in Lesson 6 and goes live on GitHub in
Lesson 7. So create it in its own folder, *next to* your learning repository, not inside it:

```bash
cd ~
mkdir my-page
cd my-page
code .
```

## Worked example
A page for an invented shop. Type it, save it as `duka.html` somewhere to practise (not in
`my-page`), then open it in the browser by double-clicking it or with `xdg-open duka.html`
(Linux) / `open duka.html` (macOS) / `explorer.exe duka.html` (WSL).

```html
<!DOCTYPE html>
<html lang="sw">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Duka la Mama Neema</title>
  </head>
  <body>
    <h1>Duka la Mama Neema</h1>
    <p>Tunauza sukari, unga, mchele na mafuta.</p>
    <p>Tupo Sinza, Dar es Salaam. Hufunguliwa saa 1 asubuhi hadi saa 3 usiku.</p>
  </body>
</html>
```

Now right-click the heading → Inspect. Double-click the heading text in the developer tools
and change it. See it change on the page. Reload: it is back.

## Predict
1. You forget `</h1>` after the heading. What happens on the page?
2. You remove the `charset` line and write `Zoë` in the page. What might you see?
3. You open the page on a phone without the `viewport` line. What happens?

<details><summary>Answers</summary>

1. The browser guesses: often everything after it becomes part of the heading, big and bold.
   Browsers forgive mistakes, which is why you must check your own HTML (Lesson 4 shows how).
2. Possibly `ZoÃ«` — the bytes of `ë` read with the wrong character set.
3. The phone shows a shrunken desktop-width page that you have to zoom into.
</details>

## Exercises
1. **`index.html`** in `my-page/` — the skeleton, a heading with your name, and two paragraphs:
   who you are, and what you are learning. Type the skeleton from memory if you can; look back
   only when stuck, and note what you had to look up.
2. **Break and inspect.** Remove a closing tag, reload, and use Inspect to see how the browser
   "fixed" it. Write what you saw in `exercises/stage-0/lesson-03/notes.md`. Then repair it.
3. **Change `lang`.** Find out from MDN what `lang` is used for. Decide whether your page is
   mainly Kiswahili or English and set it to match.

## Find the bug
This page looks fine in the browser, but the validator rejects it. What is wrong?

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>My page</title>
    <h1>Hello</h1>
    <p>Welcome to my page.</p>
  </head>
  <body>
  </body>
</html>
```

(Hint: use Inspect to see *where* the browser put the heading and paragraph. It quietly
moved them for you. Other tools, such as search engines and screen readers, may not be so
forgiving.)

## Done when
- [ ] VS Code is installed and opens your `my-page` folder.
- [ ] `my-page/index.html` has the full skeleton, a heading and two paragraphs, and opens in a browser.
- [ ] You changed something live with developer tools.
- [ ] You can explain, without notes, what each line of the skeleton is for.

## Record
```bash
python .emw/tools/emw_track.py log core.html-css --type implement --assistance A1 --task "Wrote an HTML page skeleton by hand, opened it, and inspected and edited it live in developer tools"
```
