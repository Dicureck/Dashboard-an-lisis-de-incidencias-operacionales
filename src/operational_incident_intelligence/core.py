"""Synthetic service incident stream with explicit SLA/backlog rules."""
from __future__ import annotations
from datetime import datetime, timedelta
from random import Random
import pandas as pd

CATEGORIES=("Network","Delivery","Platform","Support")
SEVERITY_TARGET_HOURS={"critical":4,"high":12,"medium":36,"low":72}
AS_OF=datetime(2026,4,1,0,0,0)


def generate_incidents(n:int=320,seed:int=2026)->pd.DataFrame:
    if n<1:raise ValueError("n must be positive")
    rng=Random(seed); rows=[]
    for i in range(n):
        severity=rng.choices(list(SEVERITY_TARGET_HOURS),weights=[8,21,49,22])[0]
        opened=AS_OF-timedelta(days=rng.randint(1,70),hours=rng.randint(0,23))
        target=SEVERITY_TARGET_HOURS[severity]
        closed=rng.random()>=.16
        resolution=round(max(0.3,rng.uniform(.4,2.1)*target),2) if closed else None
        resolved=opened+timedelta(hours=resolution) if closed else None
        # A simulated resolved event cannot occur after the reporting date.
        if resolved and resolved>AS_OF:
            resolved=None;resolution=None;closed=False
        rows.append({"incident_id":f"INC-{i+1:05d}","category":CATEGORIES[i%len(CATEGORIES)],
                     "severity":severity,"opened_at":opened.isoformat(timespec="seconds"),
                     "resolved_at":resolved.isoformat(timespec="seconds") if resolved else "",
                     "status":"resolved" if closed else "open",
                     "team":f"TEAM-{i%5+1}","target_hours":target})
    return pd.DataFrame(rows)


def analyze(df:pd.DataFrame,as_of:datetime=AS_OF)->pd.DataFrame:
    expected={"incident_id","category","severity","opened_at","resolved_at","status","target_hours"}
    if not expected.issubset(df.columns):raise ValueError("Required columns missing")
    if df.empty:raise ValueError("Empty incidents")
    if df.incident_id.duplicated().any():raise ValueError("Duplicate IDs")
    if not df.category.isin(CATEGORIES).all() or not df.severity.isin(SEVERITY_TARGET_HOURS).all():raise ValueError("Unknown category or severity")
    if not df.status.isin(["open","resolved"]).all():raise ValueError("Unknown status")
    if (df.apply(lambda r: r.target_hours!=SEVERITY_TARGET_HOURS[r.severity],axis=1)).any():raise ValueError("SLA target mismatch")
    result=df.copy()
    opened=pd.to_datetime(result.opened_at,errors="raise",utc=False)
    resolved=pd.to_datetime(result.resolved_at.replace("",pd.NA),errors="coerce",utc=False)
    if (opened>as_of).any():raise ValueError("Opened after reporting cutoff")
    if (result.status.eq("resolved") != resolved.notna()).any():raise ValueError("Status/timestamp mismatch")
    if (resolved.notna() & (resolved<opened)).any():raise ValueError("Resolved before opened")
    if (resolved.notna() & (resolved>as_of)).any():raise ValueError("Resolved after reporting cutoff")
    result["is_resolved"]=result.status.eq("resolved")
    result["resolution_hours"]=(resolved-opened).dt.total_seconds()/3600
    result["open_age_hours"]=(as_of-opened).dt.total_seconds().div(3600).where(~result.is_resolved)
    result["resolved_within_sla"]=(result.is_resolved & result.resolution_hours.le(result.target_hours))
    result["is_open_overdue"]=(~result.is_resolved & result.open_age_hours.gt(result.target_hours))
    return result


def by_category(enriched:pd.DataFrame)->pd.DataFrame:
    if enriched.empty:raise ValueError("Empty dataset")
    required={"category","is_resolved","resolved_within_sla","is_open_overdue","resolution_hours"}
    if not required.issubset(enriched.columns):raise ValueError("Call analyze() first")
    grouped=enriched.groupby("category",as_index=False,sort=True).agg(
        incidents=("is_resolved","size"),resolved=("is_resolved","sum"),
        within_sla=("resolved_within_sla","sum"),open_overdue=("is_open_overdue","sum"),
        median_resolution_hours=("resolution_hours","median"))
    grouped["backlog"]=grouped.incidents-grouped.resolved
    grouped["resolved_pct"]=(100*grouped.resolved/grouped.incidents).round(2)
    grouped["resolved_sla_pct"]=(100*grouped.within_sla/grouped.resolved).where(grouped.resolved.ne(0)).round(2)
    return grouped.round(2)
