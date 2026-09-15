# Business Questions

This document lists the questions the analysis is meant to answer. Each business
question later gets mapped, in [data-requirements.md](data-requirements.md), to the
specific data needed to answer it. The list below extends the original set with a few
additions that came up while thinking through what "improve the process without
weakening control" actually requires answering.

Throughout this project, none of these questions are answered as proof of causation.
Findings are described using language such as *associated with*, *related to*, *higher
rate*, *lower rate*, *suggests*, or *may indicate*, never *causes* or *is responsible
for*. A synthetic dataset with simulated relationships cannot support causal claims, and
even with real data, a descriptive analysis like this one would not be able to on its
own.

## Portfolio-level questions

1. What is the overall approval rate?
2. What is the overall rejection rate?
3. What share of applications goes through manual review?
4. What is the average and median processing time?
5. What does the tail of the processing time distribution look like (p90), and which
   applications sit there?

## Process questions

6. Which types of applications take the longest to process?
7. Which steps of the process are associated with the longest delays?
8. Which factors are associated with an application being sent to manual review rather
   than decided automatically?
9. Which missing pieces of information are the most frequent, and are they associated
   with longer processing times?
10. Is the number of verification errors on a file associated with a longer processing
    time?

## Decision questions

11. Which factors are associated with an application being approved versus rejected?
12. Do applications with previous defaults show a different approval pattern than
    applications without?
13. Does the debt-to-income ratio show an association with the decision outcome?

## Segment questions

14. Which customer segments or channels show a higher share of manual review?
15. Which customer segments or channels show longer processing times?

## Improvement questions

16. Which checks or tasks in the current process look like candidates for further
    automation, based on how often they are performed and how often they lead to no
    change in outcome?
17. Where does the process most need a human decision-maker rather than a rule?

Question 16 and 17 deliberately sit next to each other: the goal is never to find "what
can be removed," but to separate what looks safe to streamline from what exists because
a person needs to weigh a judgment call.
