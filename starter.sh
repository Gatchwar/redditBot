#!/bin/bash

until python magictcg_bot.py; do
	echo "CRASH" >&2
	sleep 1
done