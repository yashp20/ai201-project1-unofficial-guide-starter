# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

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
700 characters

**Overlap:**  
150 characters

**Reasoning:**  
My documents are mostly Reddit discussions and Rate My Professors review summaries. These documents are shorter and more opinion-based than long textbooks or official manuals, so the chunks should not be too large. A 700-character chunk is large enough to keep a complete student opinion together, including context about the course, professor, workload, grading, or exams. At the same time, it is small enough that retrieval can still find specific information, such as comments about CS 374 difficulty, CS 225 workload, or CS 128 support resources.

The 150-character overlap helps preserve context when an important idea appears near the edge of a chunk. For example, a student might start by describing a course workload and then mention quizzes or exams at the end of the paragraph. Overlap makes it more likely that the full idea is still available in at least one retrieved chunk.

If chunks are too small, the system might retrieve fragments that do not make sense by themselves. If chunks are too large, one chunk may mix unrelated topics like workload, professor personality, exams, and registration advice, which would make retrieval less precise.


---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->


**Embedding model:**  
I will use `all-MiniLM-L6-v2` from `sentence-transformers`.

**Top-k:**  
I will retrieve the top 5 chunks for each query.

**Production tradeoff reflection:**  
`all-MiniLM-L6-v2` is a good choice for this project because it runs locally, is free, and is fast enough for a small document collection. It should work well for semantic search over student review text because it can match similar meanings even when the query does not use the exact same words as the document.

For a production system, I would compare embedding models based on accuracy, latency, cost, context length, and how well they handle informal student language. Since Reddit and Rate My Professors comments often include slang, abbreviations, and course numbers, I would want an embedding model that performs well on short, noisy, opinion-based text. I would also consider multilingual support and whether the embedding model should run locally or through an API.

Retrieving too few chunks could miss the answer, especially if different students mention different parts of a course experience. Retrieving too many chunks could confuse the LLM by adding loosely related information. Top-k of 5 is a reasonable starting point because it gives enough context without overwhelming the generation step.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about CS 225 workload and preparation? | The system should mention that students recommend understanding data structures, practicing C++, starting MPs early, and expecting a meaningful weekly time commitment. |
| 2 | What do students say about CS 128 workload and support resources? | The system should mention CS 128 workload, grade data, weekly time expectations, office hours, Even More Practice, quiz reviews, and practice problems. It should also mention that some student reviews describe the course as frustrating or busy-work heavy. |
| 3 | What do students say about CS 374 difficulty and when to take it? | The system should mention that CS 374 is theory-heavy, depends on CS 173/proof maturity, can be a major time sink, and is easier with a strong group. |
| 4 | Which professors are described as helpful or good at teaching? | The system should mention professors such as Brad Solomon, Emily Fox, Wade Fagen-Ulmschneider, Margaret Fleck, Jeff Erickson, Alvarez, or Zilles only if those names appear in the retrieved documents. |
| 5 | What useful CS classes do students or alumni recommend for jobs? | The system should mention CS 425, CS 411, CS 440, and ECE 391 if the retrieval finds the alumni thread, and should note that CS 425 is described as useful but difficult/time-consuming. |


---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->


1. The documents are informal and noisy because they come from Reddit and Rate My Professors. Student comments may include slang, abbreviations, emotional opinions, missing context, or conflicting perspectives. This could make retrieval harder because the system may match the course number but miss the specific topic of the question.

2. Retrieval may return chunks about the right class but the wrong issue. For example, a query about CS 225 workload could retrieve a chunk about Brad Solomon’s teaching style because both mention CS 225. I will debug this by printing retrieved chunks and checking whether the returned text actually answers the question.

3. The LLM may try to answer from general knowledge instead of only using the retrieved documents. To prevent this, the generation prompt will explicitly say to answer only from retrieved chunks, cite source files, and refuse when the documents do not contain enough information.

4. Some information may be split across chunk boundaries. For example, one paragraph may mention a professor name at the start and workload details near the end. The 150-character overlap should reduce this problem, but I will inspect sample chunks to make sure they are readable and self-contained.


---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     ```mermaid
flowchart TD
    A[Raw .txt files in documents folder] --> B[Document Ingestion and Cleaning using Python]
    B --> C[Chunking with 700 character chunks and 150 character overlap]
    C --> D[Embeddings using sentence-transformers all-MiniLM-L6-v2]
    D --> E[ChromaDB Vector Store with source metadata]
    E --> F[Semantic Retrieval of top 5 chunks]
    F --> G[Groq LLM grounded response generation]
    G --> H[Answer with source citations]

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
