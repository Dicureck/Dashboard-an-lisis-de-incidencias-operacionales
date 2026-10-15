import pandas as pd
import pytest
from operational_incident_intelligence.core import AS_OF,generate_incidents,analyze,by_category
from operational_incident_intelligence.report import render_dashboard

def test_generator_deterministic():
    pd.testing.assert_frame_equal(generate_incidents(60,1),generate_incidents(60,1))

def test_unique_ids():
    assert generate_incidents(400).incident_id.is_unique

def test_invalid_n():
    with pytest.raises(ValueError):generate_incidents(0)

def test_cutoff_and_monotonic_resolution():
    e=analyze(generate_incidents())
    assert e.resolution_hours.dropna().ge(0).all()
    assert e.open_age_hours.dropna().ge(0).all()

def test_status_backlog_conservation():
    s=by_category(analyze(generate_incidents()))
    assert int(s.incidents.sum())==int(s.resolved.sum()+s.backlog.sum())

def test_no_resolved_incident_is_overdue_open():
    e=analyze(generate_incidents())
    assert not (e.is_resolved & e.is_open_overdue).any()

def test_duplicate_identifiers_rejected():
    d=generate_incidents(2);d.loc[1,"incident_id"]=d.loc[0,"incident_id"]
    with pytest.raises(ValueError,match="Duplicate"):analyze(d)

def test_mismatched_status_rejected():
    d=generate_incidents(2);d.loc[0,"status"]="resolved";d.loc[0,"resolved_at"]=""
    with pytest.raises(ValueError,match="Status"):analyze(d)

def test_sla_contract_rejected():
    d=generate_incidents(5);d.loc[0,"target_hours"]=1000
    with pytest.raises(ValueError,match="SLA"):analyze(d)

def test_preview_labels_synthetic(tmp_path):
    f=tmp_path/"demo.html";render_dashboard(by_category(analyze(generate_incidents(80))),f)
    assert "All incidents and metrics are fictional" in f.read_text()
