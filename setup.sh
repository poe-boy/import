#!/bin/bash

docker-compose down

docker-compose up -d

sleep 10

docker exec postgres bash -c "chmod +x /database/wait-for-postgres.sh && /database/wait-for-postgres.sh localhost"

docker exec postgres bash -c "psql -U postgres -f /database/setup.sql"