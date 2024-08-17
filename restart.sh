#!/bin/bash

SCRIPT_DIR=$( dirname -- $(readlink /usr/bin/restart_im_habit_bot))
docker compose -f $SCRIPT_DIR/docker-compose.yaml restart
