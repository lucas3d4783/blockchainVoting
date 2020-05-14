#!/bin/bash

for i in $(seq 10);
do
curl -X POST -H 'Content-Type: application/json' -d '{"exemplo": 1, "testando": "uma inserção qualquer"}' http://127.0.0.1:8001/blocos
done

