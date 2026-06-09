# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My project focuses on unofficial student knowledge about UIUC computer science courses and professors. This knowledge is valuable because students often want to know what classes are actually like before registering, including workload, difficulty, professor quality, exam style, grading, attendance expectations, and how much time assignments take. Official course catalogs list course topics and prerequisites, but they do not usually explain the real student experience, so students rely on Reddit threads, Rate My Professors reviews, and peer advice.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit CS 225 what to expect thread | Student discussion about CS 225 preparation, workload, C++ knowledge, relation to CS 128, and expected weekly time commitment | documents/cs255_reviews.txt |
| 2 | Reddit CS 128 faculty workload response | Faculty response about CS 128 workload, grade data, quiz concerns, and support resources like office hours and practice sessions | documents/cs128_reviews.txt |
| 3 | Reddit CS 357 Silva experience thread | Student discussion about CS 357 with Silva, workload, quizzes, homework, MPs, linear algebra preparation, and difficulty | documents/cs375_reviews.txt |
| 4 | Reddit CS 374 incoming sophomore thread | Student and faculty discussion about taking CS 374 early, math maturity, CS 173 background, workload, interview prep, and group work | documents/cs374_reviews.txt |
| 5 | Rate My Professors Brad Solomon CS 225 reviews | Student reviews about Brad Solomon's CS 225 lectures, difficulty, homework, quizzes, extra credit, and feedback | documents/professor_1_reviews.txt |
| 6 | Rate My Professors Emily Fox CS 374 reviews | Student reviews about Emily Fox's CS 374 teaching, homework difficulty, tests, lectures, Discord support, and course difficulty | documents/professor_2_reviews.txt |
| 7 | Rate My Professors Michael Nowak CS 128 reviews | Student reviews about Michael Nowak's CS 128 workload, lessons, grading, quizzes, support structure, and difficulty | documents/professor_3_reviews.txt |
| 8 | Reddit favorite UIUC professors thread | Student discussion about favorite UIUC professors, including Wade Fagen-Ulmschneider, Margaret Fleck, Jeff Erickson, Alvarez, and Zilles | documents/reddit_best_cs_professors.txt |
| 9 | Reddit useful CS classes alumni thread | Alumni and student discussion about useful UIUC CS classes for jobs, including CS 425, CS 411, CS 440, and ECE 391 | documents/reddit_course_advice.txt |
| 10 | Reddit CS major workload thread | Prospective student discussion about UIUC CS workload, prior programming experience, machine problems, office hours, LeetCode, ACM, and course assistant opportunities | documents/reddit_cs_workload.txt |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
