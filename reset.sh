#!/bin/bash

docker cp database postgres:/poeboy

docker exec postgres bash  -c "psql -U postgres -f /poeboy/setup.sql"
