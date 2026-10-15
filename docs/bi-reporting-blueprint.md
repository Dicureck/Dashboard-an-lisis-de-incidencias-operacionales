# Cross-platform BI & reporting blueprint

The reproducible CSV exports can support a small, independently implemented dashboard in **Power BI** or **Tableau**. No PBIX, Tableau workbook, Crystal Reports binary, or SSRS RDL is claimed to be present here.

Recommended pages:

1. **Service pulse:** arrivals, resolution rate, open backlog, open overdue.
2. **SLA & severity:** median resolution time by severity, severity-target distributions, resolved-within-SLA by group (with denominator tooltip).
3. **Backlog analysis:** open tickets by age and category, overdue segmentation, fixed reporting cutoff.
4. **QA checks:** duplicate IDs, invalid timestamps, status conflicts, unknown categories and targets.

Power BI DAX, with columns imported as appropriate datatypes:

```DAX
Incident Count = COUNTROWS(Incidents)
Resolved = CALCULATE([Incident Count], Incidents[status] = "resolved")
Backlog = [Incident Count] - [Resolved]
Resolved % = DIVIDE([Resolved], [Incident Count])
```

A time-series report requires a date dimension and explicit choice between reporting date, opened date, and resolved date. Avoid misleading users by mixing these event dates in the same axis.

Crystal Reports and Report Builder can be applied to paginated outputs only after an independent synthetic report definition has been developed; those formats are tracked as future scope, not completed deliverables.
