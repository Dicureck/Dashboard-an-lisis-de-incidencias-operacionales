# Engineering notes

- Generated records use a fixed cutoff to make age/backlog reproducible across machines.
- Open incidents have no invented resolution time.
- Resolved-within-SLA counts only resolved incidents and must always be shown alongside overdue open backlog.
- Tests enforce time ordering, one-row-per-incident grain and severity-target consistency.
- Static offline HTML avoids links to external servers, client IP, tracking services or runtime dependencies.
- Roadmaps for Tableau / Crystal / Report Builder are examples for future independent artifacts, not published binaries.
