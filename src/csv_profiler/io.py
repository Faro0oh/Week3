from __future__ import annotations

from csv import DictReader
from pathlib import Path

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
        path = Path(path)
        try:    
          rows = []
          with open(path,"r",encoding="utf8") as file_handle:
            csv_reader = DictReader(file_handle)
            for row in csv_reader:
                rows.append(row)  

        except FileNotFoundError:
          raise FileNotFoundError(f"CSV not found: {path}")
        if not rows:
           raise ValueError("CSV has no data rows")

        return rows



       
