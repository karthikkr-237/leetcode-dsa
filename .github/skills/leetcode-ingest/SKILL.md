---

name: leetcode-ingest
description: Ingests an accepted LeetCode solution into the repository by verifying problem metadata, determining the primary topic and language, creating the correct Topic/Difficulty solution path, checking duplicates, and preserving the submitted code.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# LeetCode Ingestion Skill

Use this skill when the user provides an accepted LeetCode solution and wants it added to the `leetcode-dsa` repository.

## Input

The user may provide:

* LeetCode problem URL
* problem number
* problem title
* accepted solution code
* programming language
* any combination of the above

The submitted source code is authoritative for the implementation itself.

LeetCode is authoritative for problem metadata when it can be verified.

## Step 1 — Identify the problem

Extract the problem number and title from:

1. explicit user information
2. a supplied LeetCode URL
3. identifiable information in the prompt

If the identity is ambiguous, ask the user.

Do not guess.

## Step 2 — Verify LeetCode metadata

When web access is available, verify the problem against LeetCode.

Collect:

* problem number
* exact title
* difficulty
* topics

Prefer the official LeetCode problem page.

Do not invent metadata.

If verification is unavailable, say so clearly.

## Step 3 — Determine primary repository topic

Map LeetCode topics into the repository's existing categories.

Use the submitted solution as a secondary signal when multiple topics are possible.

Prefer the most representative algorithm/data-structure category.

Do not create unnecessary categories.

Current categories include:

* Arrays
* Strings
* Hashing
* Two-Pointers
* Sliding-Window
* Binary-Search
* Linked-List
* Stack
* Queue
* Heap
* Trees
* Graphs
* Greedy
* Backtracking
* Dynamic-Programming
* Bit-Manipulation
* Math
* Recursion

If no category is appropriate, ask the user before creating a new one.

## Step 4 — Determine language

Inspect the syntax and context of the submitted source.

Use:

| Language   | Extension |
| ---------- | --------- |
| C          | `.c`      |
| C++        | `.cpp`    |
| Python     | `.py`     |
| Java       | `.java`   |
| JavaScript | `.js`     |
| TypeScript | `.ts`     |
| Go         | `.go`     |
| Rust       | `.rs`     |
| Kotlin     | `.kt`     |
| Swift      | `.swift`  |

If ambiguous, ask.

## Step 5 — Build the path

Format:

```
<Topic>/<Difficulty>/<4-digit-problem-number>-<kebab-case-title>.<extension>
```

Example:

```
Arrays/Easy/03471-find-the-largest-almost-missing-integer.c
```

Rules:

* topic directory must match repository conventions
* difficulty must be exactly `Easy`, `Medium`, or `Hard`
* problem number should be zero-padded to four digits
* filename should use lowercase kebab-case
* preserve the official problem title semantically
* do not put spaces in filenames

## Step 6 — Check duplicates

Search the repository for the problem number.

Possible cases:

### Case A — Problem does not exist

Create the solution normally.

### Case B — Same problem and same language exists

STOP.

Do not overwrite.

Report the existing path.

### Case C — Same problem exists in another language

Allow a new language implementation.

The total problem count remains one because repository statistics deduplicate by problem ID.

### Case D — Same problem ID exists under conflicting topics/difficulties

STOP and report the conflict.

Do not silently move existing files.

## Step 7 — Preserve source

The user's submitted solution must be copied exactly.

Do not automatically:

* refactor
* optimize
* rename variables
* add comments
* remove comments
* change algorithms
* change formatting

The agent may normalize the filename and directory only.

## Step 8 — Validate

Before reporting success:

* verify the file exists
* verify the file has the submitted code
* verify the path matches metadata
* run `git status`
* ensure unrelated changes are untouched

Do not compile or execute the solution unless the user asks for that or it is necessary to diagnose a problem.

## Step 9 — Commit and push

Only commit/push if the user explicitly requests it.

If requested:

1. stage only intended files
2. inspect staged changes
3. commit
4. synchronize with remote using rebase
5. push

Never use force push.

Never overwrite remote history.

If a rebase conflict occurs, stop and ask the user.

## Step 10 — README

Never manually alter the generated statistics section.

The repository's existing GitHub Action calculates:

* unique problem count
* difficulty distribution
* topic distribution
* language distribution
* recently added problems
* duplicate metadata conflicts

The README should update through GitHub Actions after the solution reaches `main`.

## Expected successful result

For an accepted C solution to LeetCode 3471:

```
Arrays/Easy/03471-find-the-largest-almost-missing-integer.c
```

The agent should report:

```
✓ Problem verified
✓ Difficulty: Easy
✓ Topic: Arrays
✓ Language: C
✓ Solution added
✓ Source preserved unchanged
```

If pushed:

```
✓ Commit created
✓ Pushed to main
✓ README automation will update statistics
```
