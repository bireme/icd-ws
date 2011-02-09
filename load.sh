#!/bin/bash
./cidtab2json.py | curl -d @- -X POST http://localhost:5984/icd/_bulk_docs -H"Content-Type: application/json"
