#!/bin/bash
./cidtab2json.py | curl -d @- -X POST http://localhost:5900/cid10/_bulk_docs -H"Content-Type: application/json"
