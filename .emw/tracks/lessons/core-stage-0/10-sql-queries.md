# Lesson 10 — SQL queries: asking questions of your data

**Time:** 4–5 hours · **Skills:** `core.sql` · **Before this:** Lesson 9
**Your folder:** `exercises/stage-0/sql/`

## Goal
By the end you can answer real questions about your shop database with `SELECT`, filter,
sort, count and total, join tables together, group results, and safely add and change rows —
the ten queries the Stage 0 brief asks for.

## The idea
A query asks a question; the answer is a table.

```sql
SELECT name, price          -- which columns
FROM products               -- which table
WHERE price < 5000          -- which rows
ORDER BY price DESC         -- in what order
LIMIT 3;                    -- how many
```

The clauses always come in that order. Text goes in single quotes: `WHERE name = 'Sukari'`.

**Filtering:** `=`, `<>` (not equal), `<`, `>=`, `AND`, `OR`, `NOT`,
`BETWEEN 1000 AND 5000`, `IN ('Sukari', 'Unga')`, `LIKE 'Su%'` (`%` means "anything"),
`IS NULL` (never `= NULL`, which is never true).

**Totals (aggregates):** `COUNT(*)`, `SUM(amount)`, `AVG(…)`, `MIN(…)`, `MAX(…)`.

**`GROUP BY`** gives one result row per group:
```sql
SELECT customer_id, COUNT(*) AS sales
FROM sales
GROUP BY customer_id;
```
Every column in the `SELECT` must either be in the `GROUP BY` or inside an aggregate.
**`HAVING`** filters groups, the way `WHERE` filters rows: `HAVING COUNT(*) >= 3`.

**`JOIN`** combines tables along a relationship:
```sql
SELECT customers.name, sales.sold_on
FROM sales
JOIN customers ON customers.id = sales.customer_id;
```
- `JOIN` (inner join) keeps only rows that match on both sides.
- `LEFT JOIN` keeps *every* row from the left table, with `NULL` where nothing matched — this is
  how you find "customers who never bought anything".
- Short names (aliases) keep long joins readable: `FROM sales s JOIN customers c ON c.id = s.customer_id`.

**Changing data**
```sql
INSERT INTO products (name, price, stock) VALUES ('Chumvi', 500, 40);
UPDATE products SET price = 3700 WHERE id = 1;
DELETE FROM products WHERE id = 9;
```
**An `UPDATE` or `DELETE` without `WHERE` changes every row in the table.** Always write the
`WHERE` first, and run it as a `SELECT` before turning it into an `UPDATE`.

**Transactions** group changes so they all happen or none do:
```sql
BEGIN;
UPDATE products SET stock = stock - 2 WHERE id = 1;
INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (11, 1, 2, 3500);
COMMIT;      -- or ROLLBACK; to undo both
```
A sale that reduces stock but fails to record the item would leave your shop's numbers wrong.
Stage 2 and Stage 4 rely on this heavily.

**Working in SQLite:** `sqlite3 shop.db` opens a prompt. `.headers on` and `.mode column` make
results readable, `.tables` lists tables, `.schema products` shows a table's design, `.read
queries.sql` runs a file, `.quit` leaves. Practise more at sqlbolt.com.

## Worked example
Questions for the parcel database from Lesson 9.

```sql
.headers on
.mode column

-- How many parcels went to each town, and the fees collected?
SELECT o.town, COUNT(*) AS parcels, SUM(p.fee) AS fees
FROM parcels p
JOIN offices o ON o.id = p.to_office_id
GROUP BY o.town
ORDER BY fees DESC;

-- Which offices have never received a parcel?
SELECT o.town
FROM offices o
LEFT JOIN parcels p ON p.to_office_id = o.id
WHERE p.id IS NULL;
```

With the two parcels from Lesson 9, the first gives Mwanza (1, 12000) then Arusha (1, 8000);
the second gives Dar es Salaam, because both parcels left from there and none arrived.

## Predict
For the parcel database:
1. `SELECT COUNT(*) FROM parcels WHERE fee > 10000;`
2. `SELECT town FROM offices WHERE town LIKE '%a';`
3. The two queries in the worked example with `JOIN` instead of `LEFT JOIN` in the second one.
   What does the second return?

<details><summary>Answers</summary>

1. `1` (PX1002, 12000).
2. `Arusha` and `Mwanza` — both end in "a". `Dar es Salaam` does not.
3. Nothing. An inner join drops the offices with no matching parcel, and then `p.id IS NULL`
   is never true.
</details>

## Exercises
Write `queries.sql` for your shop database. Above every query, a one-line comment saying
what question it answers (the brief requires this). At least ten queries, including:

1. Products under a price you choose, cheapest first.
2. Products with stock of 5 or fewer (what needs reordering).
3. The total value of all stock (price × stock, added up).
4. Each customer's name with the number of sales they made (**`JOIN`** + **`GROUP BY`**).
5. Total sales in shillings per day (`SUM` of quantity × price from `sale_items`, joined to `sales`).
6. The three best-selling products by quantity (**`JOIN`**).
7. Customers who never bought anything (**`LEFT JOIN`**).
8. Products never sold.
9. **`INSERT`** a new product.
10. **`UPDATE`** one product's price — written as a `SELECT` first, then the `UPDATE`.

Then run the whole file with `sqlite3 shop.db < queries.sql` and check every answer by hand
against your seed data for at least three of them.

## Find the bug
The shop owner ran this to raise the price of sugar. Afterwards every product cost 3,700.
What went wrong, how could it have been prevented, and how would you recover?

```sql
UPDATE products SET price = 3700;
WHERE name = 'Sukari';
```

## The Stage 0 gate
You have now covered everything the [Stage 0 brief](../../briefs/core-stage-0.md) asks for.
Run `python .emw/tools/emw_track.py status` and work through what is left:
- **Stretch change** (transfer): break your page on purpose on a branch, open a pull request,
  write in its description how you would find the problem with developer tools, then fix it.
  Log it with `--type transfer`, at A0 or A1.
- **Rebuild from memory**, at least a week after you started the stage: a new repository, a
  page, a commit, a push, published — no notes. Log it with `--type rebuild`.
- **A real person** looks at your repository and live page and hears you explain them. You
  record it with `--verified-by human --reviewer "<their name>"`.
- Then `python .emw/tools/emw_track.py next` opens Stage 1.

## Done when
- [ ] `queries.sql` has at least ten commented queries, including two `JOIN`s, a `GROUP BY`,
  an `INSERT` and an `UPDATE`, and they all run.
- [ ] Three answers checked by hand.
- [ ] The bug explained, with how to prevent it.
- [ ] You can explain, without notes, the difference between `JOIN` and `LEFT JOIN`.

## Record
```bash
python .emw/tools/emw_track.py log core.sql --type implement --assistance A1 --task "Wrote ten commented queries on my shop database with JOIN, LEFT JOIN, GROUP BY, INSERT and UPDATE, checked three by hand"
```
