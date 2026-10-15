import argparse
from pathlib import Path
from .core import generate_incidents,analyze,by_category
from .report import render_dashboard

def main(argv=None):
    p=argparse.ArgumentParser(description="Synthetic service incident intelligence demo")
    p.add_argument("command",choices=["demo"]);p.add_argument("--out-dir",default="build/demo")
    p.add_argument("--seed",type=int,default=2026);p.add_argument("--rows",type=int,default=320)
    args=p.parse_args(argv)
    folder=Path(args.out_dir);folder.mkdir(parents=True,exist_ok=True)
    incidents=generate_incidents(n=args.rows,seed=args.seed)
    analyzed=analyze(incidents);summary=by_category(analyzed)
    incidents.to_csv(folder/"synthetic_incidents.csv",index=False)
    summary.to_csv(folder/"category_kpis.csv",index=False)
    render_dashboard(summary,folder/"dashboard.html")
    print(f"Generated {len(incidents)} fictional incidents in {folder}")

if __name__=="__main__":main()
