#!/bin/bash
./cidtab2json.py | curl -d @- -X POST http://localhost:5984/cid10/_bulk_docs -H"Content-Type: application/json"
