#!/bin/bash

SCRIPT_DIR=$( dirname -- $(readlink /usr/bin/start_im_habit_bot))
docker compose -f $SCRIPT_DIR/docker-compose.yaml up -d
