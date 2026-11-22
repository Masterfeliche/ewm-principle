# Lesson 8 — How the web works

**Time:** 2–3 hours · **Skills:** `core.http` · **Before this:** Lesson 7 (your page must be live)
**Your folder:** `my-page/` and `exercises/stage-0/lesson-08/`

## Goal
By the end you can explain what happens between typing an address and seeing a page, read a
request and a response in the browser's network tab, and name the common status codes and
headers and what they are for.

## The idea
**The parts of an address (URL)**
```
https://asha.github.io/my-page/projects.html?lang=sw#contact
└─┬─┘   └──────┬──────┘└─────────┬─────────┘└──┬──┘└──┬──┘
scheme       host              path          query  fragment
```
The **fragment** (`#contact`) never leaves the browser; it only jumps within the page.

**What happens when you press Enter**
1. **DNS:** the browser asks "what is the IP address of `asha.github.io`?" and gets a number
   such as `185.199.108.153`. DNS is the internet's phone book.
2. **Connection:** it connects to that address. With `https`, it also sets up encryption
   (**TLS**) and checks the site's certificate, so nobody in between can read or change the
   traffic — not the café Wi-Fi, not the mobile network.
3. **Request:** it sends an HTTP request: a **method**, a **path**, and **headers**.
4. **Response:** the server sends back a **status code**, headers, and a **body** (the HTML).
5. **More requests:** the browser reads the HTML, finds the CSS and images it links to, and
   requests each of those too.
6. **Render:** it draws the page.

**A request** (simplified)
```
GET /my-page/ HTTP/1.1
Host: asha.github.io
User-Agent: Mozilla/5.0 (Linux; Android 13) …
Accept: text/html
```

**A response** (simplified)
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 4120
Cache-Control: max-age=600

<!DOCTYPE html> …
```

**Methods:** `GET` asks for something and must not change anything. `POST` sends data to be
processed, such as a form. (Others — `PUT`, `PATCH`, `DELETE` — come with APIs in Stage 3.)

**Status codes** — the first digit tells you the kind:

| Code | Meaning |
|---|---|
| `200 OK` | here it is |
| `301` / `302` | it is somewhere else — the `Location` header says where |
| `304 Not Modified` | you already have the latest copy; use your cached one |
| `400 Bad Request` | the request itself was wrong |
| `401` / `403` | you are not signed in / you are not allowed |
| `404 Not Found` | nothing at that path |
| `500 Internal Server Error` | the server's code broke |
| `503 Service Unavailable` | the server is overloaded or down |

`4xx` means the **client** (the request) has a problem; `5xx` means the **server** does.

**Headers worth knowing:** `Content-Type` (what the body is), `Cache-Control` (how long the
browser may keep a copy), `Location` (where a redirect points), `User-Agent` (which browser),
`Set-Cookie` and `Cookie` (small pieces of data the server asks the browser to send back on
every request — how a site remembers you are signed in).

**HTTP is stateless:** each request stands alone. The server does not remember your last one
unless something — usually a cookie — reminds it.

## Worked example
The terminal can make requests too. `curl -I` shows only the response's status and headers:

```bash
curl -I https://example.com
```
```
HTTP/2 200
content-type: text/html
cache-control: max-age=…
…
```

```bash
curl -I http://github.com
```
```
HTTP/1.1 301 Moved Permanently
Location: https://github.com/
```

The second one shows a redirect: the plain `http` address sends you to the `https` one.
(Exact headers change over time; what matters is that you can read them.)

## Predict
1. You visit `https://<you>.github.io/<repo>/nothing-here.html`. Which status code?
2. You reload your page twice quickly. What status might the CSS file show the second time?
3. Is the part after `#` in a URL sent to the server?
4. A form uses `method="get"`. Where does the typed data end up?

<details><summary>Answers</summary>

1. `404`.
2. `304`, or "(memory cache)" / "(disk cache)" in the network tab — the browser reused its copy.
3. No. The fragment stays in the browser.
4. In the URL, as the query: `?name=Asha&message=…`. That is why passwords are never sent with GET.
</details>

## Exercises
1. **The network tab.** Open your live page, open developer tools → Network, and reload. In
   `my-page/http-notes.md` (the brief asks for this file) write, in your own words:
   - how many requests the page made, and what each was for;
   - the status code of each, and what it means;
   - one **request** header and one **response** header, and what each is for;
   - the total size the page downloaded. Is it light enough for a cheap phone on slow data?
2. **Status codes on purpose.** Cause a `404` on your own site. Find a `301` with `curl -I`.
   Add both to `http-notes.md`.
3. **Explain it.** In `exercises/stage-0/lesson-08/explain.md`, write the six steps from
   "typing the address" to "seeing the page" in your own words, as you would explain them to a
   friend. The brief requires that you can explain this *without notes*, so practise saying it
   out loud too.

## Find the bug
"The site is down!" says a colleague, showing a `404` for `https://asha.github.io/my-page/Projects.html`.
The file `projects.html` exists and the rest of the site works. What is wrong, and is the site
actually down?

## Done when
- [ ] `http-notes.md` has every item from exercise 1, in your own words, and is committed.
- [ ] You have seen a `404` and a `301` yourself.
- [ ] You can explain, without notes, what happens between typing an address and seeing the page.
- [ ] You can say what `4xx` and `5xx` codes have in common.

## Record
```bash
python .emw/tools/emw_track.py log core.http --type explain --assistance A1 --task "Read my live page's requests and responses in the network tab and wrote http-notes.md; explained the path from address to page"
```
