from __future__ import annotations
from pathlib import Path

def write_json(report:dict, path: str | Path) -> None:
    path = Path(path)
    if path.parent.mkdir(parents=True,exist_ok=True):
       path.write_text(json.dump(report , ensure_ascii=False , indent= 2 ), encoding="utf-8")
   

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    rows = report["summary"]["rows"]
    columns_count = report["summary"]["columns"]
    cols = report["columns"]
    
    lines = []
    
    lines.append("# CSV Profile: data/sample.csv\n")
    lines.append("\n")
    
    lines.append("## Summary\n")
    lines.append(f"- Rows: {rows:,}\n")
    lines.append(f"- Columns: {columns_count:,}\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")
    lines.append("\n")
    
    lines.append("## Columns\n\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")

    for name, col in cols.items():
        missing_percent = (col["missing"] / rows * 100) if rows > 0 else 0
        lines.append(f"| {name} | {col['type']} | {missing_percent:.1f}% | {col['unique']} |\n")
    
    lines.append("\n")
    lines.append("## Column Details\n\n")
    
    for name, col in cols.items():
        lines.append(f"### {name}\n")
        lines.append(f"- **Type:** {col.get('type', 'unknown')}\n")
        lines.append(f"- **Missing:** {col.get('missing', 0)}\n")
        lines.append(f"- **Unique:** {col.get('unique', 0)}\n")
        
        if col["type"] == "number":
            lines.append(f"- **Min:** {col.get('min', 'N/A'):.2f}\n")
            lines.append(f"- **Max:** {col.get('max', 'N/A'):.2f}\n")
            lines.append(f"- **Mean:** {col.get('mean', 'N/A'):.2f}\n")
        
        if col["type"] == "text":
            top = col.get("top", [])
            if top:
                lines.append("- **Top values:**\n")
                for value, count in top:
                    lines.append(f"  - {value}: {count}\n")
        
        lines.append("\n")
        lines.append(f"# CSV Profiling Report\n")
        lines.append(f"Generated {datetime.now().isoformat(timespec='seconds')}\n")

        lines.extend([f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"for c in report["columns"]])
        lines.append("\n## Notes\n")
        lines.append("- Missing values are: '', 'na', 'n/a', 'null', 'none', 'nan' (case-insensitive)")


    path.write_text("".join(lines), encoding="utf-8")

def render_markdown(report: dict) -> str:
    rows = report["summary"]["rows"]
    columns_count = report["summary"]["columns"]
    cols = report["columns"]

    lines = []

    lines.append("# CSV Profiling Report\n\n")

    lines.append("## Summary\n")
    lines.append(f"- Rows: {rows:,}\n")
    lines.append(f"- Columns: {columns_count:,}\n")
    lines.append(f"- Rows (computed): **{report['n_rows']}**\n")
    lines.append(f"- Columns (computed): **{report['n_cols']}**\n\n")

    lines.append("## Columns\n\n")
    lines.append("| name | type | missing | missing_pct | unique |\n")
    lines.append("|---|---:|---:|---:|---:|\n")

    for name, col in cols.items():
        missing_pct = (col["missing"] / rows * 100) if rows > 0 else 0
        lines.append(
            f"| {name} | {col['type']} | {col['missing']} | {missing_pct:.1f}% | {col['unique']} |\n"
        )

    lines.append("\n")

    return "".join(lines)
