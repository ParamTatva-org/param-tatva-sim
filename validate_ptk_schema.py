#!/usr/bin/env python
import sys, json
from jsonschema import Draft202012Validator

def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_ptk_schema.py ptk.v1.json ptk.v1.schema.json")
        sys.exit(2)
    data = json.load(open(sys.argv[1]))
    schema = json.load(open(sys.argv[2]))
    v = Draft202012Validator(schema)
    errs = list(v.iter_errors(data))
    if errs:
        for e in errs:
            print("ERROR:", e.message, "at path", list(e.path))
        sys.exit(1)
    print("PTK JSON matches schema ✔")

if __name__ == "__main__":
    main()
