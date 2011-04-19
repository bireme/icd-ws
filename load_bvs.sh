#!/bin/bash
./cidtab2json.py | curl -d @- -X POST http://bvs.couchone.com/icd/_bulk_docs -H"Content-Type: application/json"
