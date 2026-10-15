# Incident KPI contracts

Dataset grain: **one incident record**. Reference reporting timestamp: **2026-04-01 00:00**. All timestamps are naive UTC-like demo times without real timezone associations. A production model must normalize timezone-aware times.

| KPI | Calculation | Important interpretation |
|:--|:--|:--|
| Total incidents | Number of unique incident records | No tickets excluded by status |
| Resolved (%) | Resolved records / all incidents × 100 | Represents closure rate, not SLA performance |
| Backlog | Unresolved records | Must be surfaced separately |
| Open overdue | Open records with elapsed time greater than severity target | Snapshot-based |
| Resolved-within-SLA (%) | Resolved within severity target / all resolved × 100 | **Conditional on resolution**; does not conceal backlog because backlog is shown separately |
| Median resolution time | Median of (resolved_at − opened_at), resolved only | No imputed times for open tickets |

Severity targets are synthetic: critical 4h, high 12h, medium 36h, low 72h. These are fictional demonstration policies, not real SLAs. Metrics do not imply the services represented are actual organizations.
