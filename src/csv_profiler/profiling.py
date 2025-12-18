from __future__ import annotations
from pathlib import Path
from statistics import mean

def is_missing(value):
    if value is None:
        return True
    missing_list = ["", "na", "n/a", "null", "none", "nan"]
    return str(value).strip().lower() in missing_list


def try_float(value):
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    usable = []
    for v in values:
        if not is_missing(v):
            usable.append(v)
    
    if not usable:
        return "text"
    
    for v in usable:
        if try_float(v) is None:
            return "text"
    
    return "number"

def profile_rows(rows:list[dict[str, str]]) -> dic:
    n_rows = len(rows)
    n_colums = list(rows[0].keys)
    list_columns =[]

    for col in n_colums :

        for v in rows :
            v.get(col,'')
    
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    inferred = infer_type(values)
    unique = len(set(usable))  
    
    profile = {"name" : col,
               "type": inferred,
               "missing" :missing ,
               "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
               "unique":unique}

    if inferred =="number":
        nums = [try_float(v) for v in usable]
        nums = [x for x in nums if x is not None]
        if nums :
            profile.update({"min":min(nums) ,
                            "max":max(nums),
                            "mean": mean(nums) , 
                            "sum": sum(nums)/len(nums)
                            })
        list_columns.append(profile)
        return {"n_rows": n_rows,
                "n_colums" : n_colums,
                "list_columns":list_columns
                }    

