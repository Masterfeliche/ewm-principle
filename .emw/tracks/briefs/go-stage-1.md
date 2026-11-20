# Stage 1 brief: TANQR reader and writer

**Track:** Go · **Mode:** 1, you type everything · **Time:** 2–3 months including the language basics (estimate) · Read `house-rules.md` first.

## The problem
Shops in Tanzania show a QR code and the customer's wallet or bank app reads it. The text inside the code follows a national standard, TANQR, which follows the published EMVCo merchant-presented format: a string of tag-length-value fields that ends with a checksum. Few developers have read the standard, so codes get built by copying examples, and a wrong length or checksum only shows up when a customer's app refuses the code.

## Goal
A Go package, `tanqr`, and a command-line tool, `tanqr`, that build a valid payload from merchant details and parse a payload back into its fields, saying exactly what is wrong when it is invalid. It needs no account with anyone.

## Build
1. **Read the specification first.** Find and read the Bank of Tanzania TANQR guidelines and the EMVCo merchant-presented QR specification they follow (the research report links the guidelines). Write a one-page `SPEC-NOTES.md` in your own words: the field layout, which fields are required, which are nested, the allowed characters and lengths, and how the checksum is calculated. Do not copy a field table or a checksum routine from a blog post or an AI answer; every rule in your code must point to a section of the specification.
2. **Package.** An importable package with no dependencies outside the standard library:
   - parse a payload string into a typed structure, keeping unknown fields rather than dropping them;
   - build a payload string from a typed structure;
   - validate a structure or a payload and return every problem found, not just the first.
3. **Errors.** Each kind of failure (bad length, truncated input, missing required field, wrong checksum, value not allowed) is a distinct error that a caller can test for, and each carries the position or tag where it happened.
4. **Command.** `tanqr parse` reads a payload from an argument, a file or standard input and prints the fields; `tanqr build` takes merchant details as flags or a JSON file and prints the payload; `tanqr check` exits with a non-zero code when the payload is invalid.
5. **Options.** `--json` for machine-readable output; `--lang=sw|en` for labels and error messages, Kiswahili by default.
6. **Amounts.** A fixed amount is optional in the payload. Inside your program it is whole shillings in an integer.
7. **Tests.** Table-driven tests for parsing, building and each error; one fuzz test showing that the parser never panics on any input; a round-trip test (build, then parse, gives back the same structure).
8. **Release.** A Go module with a `go.mod`, the package at the root or under a clear path, the command under `cmd/`, and binaries cross-compiled for Linux, Windows and macOS.

## Edge cases you must handle
- A length that says more characters follow than the payload has left.
- A length that is not two digits.
- The same tag appearing twice at one level.
- A nested field whose inner lengths do not add up to its outer length.
- A correct layout with a wrong checksum, and a payload with no checksum field at all.
- A merchant name with characters outside what the specification allows, or longer than it allows.
- A merchant name where the number of characters and the number of bytes differ. Find out from the specification which one the length counts.
- Lower-case letters in the checksum.
- Empty input, and input with spaces or a line break at the end.

## It works when
- [ ] `go build ./...`, `go vet ./...` and `gofmt -l .` are clean, and `go test ./...` passes.
- [ ] A payload you build is accepted by your own parser and by one independent reader (another learner's parser or a public decoder), using an invented merchant.
- [ ] The parser never panics; the fuzz test has run for at least a few minutes without a failure.
- [ ] Every edge case above has a row in a test table.
- [ ] A caller can tell the kinds of error apart with `errors.Is` or `errors.As`, without reading the message text.
- [ ] No amount is ever held in a float.
- [ ] `SPEC-NOTES.md` names the section of the specification behind each rule, and the README shows the commands with sample output in both languages.
- [ ] Only invented merchant identifiers appear in the code, tests and samples.

## Stretch change (transfer check)
Add support for one more nested template from the specification that you have not handled yet (for example the additional-data field with a bill or reference number) without changing the code that reads tags and lengths. If you have to touch the reader to add a field, redesign until you do not.

## Rebuild from memory (a week later)
Without looking: write the function that splits a payload into its top-level tag, length and value fields, returning a clear error for a truncated or malformed field, with its table-driven tests.

## Gentler alternative
If reading a specification is too much for a first project, build the **mobile-money statement analyser** elective first (a file of transaction messages in, totals per month out), then come back to this one. The stage is passed with either, but TANQR is the better proof.

## Know before real use
Real merchant identifiers are issued only by a bank or a licensed payment provider, and TANQR itself serves licensed institutions. Your tool makes and checks the text of a code; it does not make anyone able to receive payments. Never print a real merchant's identifier in a public repository. See `resources/research/East Africa software problems for PHP projects.md`.

## Evidence to record
Items for `go.syntax-types`, `go.cli-files`, `go.interfaces-methods`, `go.errors`, `go.modules-toolchain`, `go.testing`, `core.testing` and `core.git`. Have a mentor or peer hand you three payloads they have damaged in ways you have not seen, and watch your tool explain each one; mark that item `verified_by: human`.
