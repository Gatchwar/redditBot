#!/bin/bash

until python replybot.py; do
	echo "CRASH" >&2
	sleep 1
done