# Lesson 9 — Designing tables: keys, relationships, and why data is split up

**Time:** 3–4 hours · **Skills:** `core.sql` · **Before this:** Lesson 1
**Your folder:** `exercises/stage-0/sql/`

## Goal
By the end you can design a small database for a real problem: decide the tables, choose the
columns and their types, connect tables with keys, and create it in SQLite.

## The idea
A **relational database** stores data in **tables**. Each table holds one kind of thing; each
**row** is one of those things; each **column** is one fact about it.

| id | name | phone |
|---|---|---|
| 1 | Juma Ally | +255712000001 |
| 2 | Asha Mwamba | +255754000002 |

**SQL** is the language for creating tables and asking questions of them. Almost every
application you build from Stage 2 on keeps its data this way.

**Why split data into separate tables?** Imagine one big table of sales, each row holding the
customer's name and phone as well as the sale:

| sale | customer | phone | item | amount |
|---|---|---|---|---|
| 1 | Juma Ally | +255712000001 | Sukari | 3500 |
| 2 | Juma Ally | +255712000001 | Unga | 2800 |
| 3 | Juma Aly | +255712000009 | Mafuta | 7000 |

Juma's details are repeated, so they drift apart: row 3 has a typo and a different phone. Is
that the same Juma? Nobody can tell. Change his phone and you must find every row. The cure is
to store **each fact once**: customers in one table, sales in another, connected by a key.

**Keys**
- A **primary key** identifies one row uniquely, forever. Use a plain number `id` that means
  nothing else — not a phone number or a name, because those change.
- A **foreign key** is a column that holds another table's primary key: `sales.customer_id`
  points to `customers.id`. That is a **relationship**.

**One-to-many** is the most common relationship: one customer has many sales; each sale has one
customer. The foreign key goes on the "many" side.

**Many-to-many** — one sale contains many products, and one product appears in many sales —
needs a table in between: `sale_items`, with a row for each product in each sale.

**Column types in SQLite** (Stage 2 uses MySQL or PostgreSQL, which have more, but the idea is
the same): `INTEGER` for whole numbers, ids and **money in shillings** (the same rule as the
house rules: never decimals for money); `TEXT` for text and for dates written as `'2026-03-14'`.

**Rules on columns** stop bad data getting in:
- `NOT NULL` — must have a value.
- `UNIQUE` — no two rows the same (a phone number, a product code).
- `CHECK (amount > 0)` — a condition every row must meet.
- `REFERENCES customers(id)` — a foreign key: the id must exist in that table.

**SQLite** is a whole database in one file, perfect for learning. Install the command-line tool:
`sudo apt install sqlite3` (Ubuntu/WSL) or `brew install sqlite` (macOS); check with
`sqlite3 --version`. In SQLite, foreign keys are only enforced after `PRAGMA foreign_keys = ON;`.

## Worked example
A database for an invented bus company's parcel desk.

```sql
-- schema.sql
PRAGMA foreign_keys = ON;

CREATE TABLE offices (
  id    INTEGER PRIMARY KEY,
  town  TEXT NOT NULL UNIQUE
);

CREATE TABLE parcels (
  id              INTEGER PRIMARY KEY,
  tracking_code   TEXT NOT NULL UNIQUE,
  from_office_id  INTEGER NOT NULL REFERENCES offices(id),
  to_office_id    INTEGER NOT NULL REFERENCES offices(id),
  sender_phone    TEXT NOT NULL,
  fee             INTEGER NOT NULL CHECK (fee > 0),   -- whole shillings
  sent_on         TEXT NOT NULL                       -- 'YYYY-MM-DD'
);

INSERT INTO offices (town) VALUES ('Dar es Salaam'), ('Arusha'), ('Mwanza');

INSERT INTO parcels (tracking_code, from_office_id, to_office_id, sender_phone, fee, sent_on)
VALUES ('PX1001', 1, 2, '+255712000001', 8000, '2026-03-14'),
       ('PX1002', 1, 3, '+255754000002', 12000, '2026-03-14');
```

```bash
sqlite3 parcels.db < schema.sql
sqlite3 parcels.db "SELECT tracking_code, fee FROM parcels;"
```

Each town is stored once. A parcel points at two offices. A fee of `0` or a parcel to an office
that does not exist is refused by the database itself.

## Predict
With the schema above:
1. `INSERT INTO offices (town) VALUES ('Arusha');` — what happens?
2. `INSERT INTO parcels (…) VALUES ('PX1003', 1, 9, '+255…', 5000, '2026-03-15');` — office 9
   does not exist. What happens (with the PRAGMA on)?
3. And with a fee of `-500`?

<details><summary>Answers</summary>

1. Refused: `UNIQUE constraint failed: offices.town`.
2. Refused: `FOREIGN KEY constraint failed`. Without `PRAGMA foreign_keys = ON` SQLite would
   accept it silently — check that line is there.
3. Refused: `CHECK constraint failed`.
</details>

## Exercises
Design a database for a small shop: **customers**, **products** (name, price, stock), **sales**
(which customer, when) and the **items** in each sale (which product, how many, at what price).

1. **On paper first** — in `design.md`, list the tables, each column with its type and rules, and
   draw the relationships with arrows. Say which relationship is one-to-many and which needs a
   table in between. Why does `sale_items` store the price at the time of the sale, rather than
   looking it up from `products`? Write your answer.
2. **`schema.sql`** — create the tables in SQLite with primary keys, foreign keys, `NOT NULL`,
   `UNIQUE` and at least two `CHECK`s. Money as `INTEGER` shillings.
3. **`seed.sql`** — invented data: at least 5 customers, 8 products, 10 sales and 20 sale items,
   including one customer who never bought anything and one product never sold. (You will need
   those in Lesson 10.)
4. **Test the rules** — in `rules.md`, write four inserts that *should* be refused, run each,
   and paste the error.

## Find the bug
Find three design problems in this table, and say how you would fix each.

```sql
CREATE TABLE orders (
  phone TEXT PRIMARY KEY,
  customer_name TEXT,
  product_names TEXT,     -- e.g. 'Sukari, Unga, Mafuta'
  total REAL
);
```

## Done when
- [ ] `design.md` explains every table, relationship and the price-at-sale decision.
- [ ] `sqlite3 shop.db < schema.sql` and then `< seed.sql` run with no errors.
- [ ] Four bad inserts are refused, with their errors recorded.
- [ ] You can explain, without notes, why data is split into separate tables, and what a foreign key is.

## Record
```bash
python .emw/tools/emw_track.py log core.sql --type implement --assistance A1 --task "Designed a shop database with primary and foreign keys and constraints, created it in SQLite, and proved the constraints refuse bad data"
```
