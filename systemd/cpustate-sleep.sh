#!/bin/bash
# Placed in /usr/lib/systemd/system-sleep/cpustate
# Called by systemd-sleep on suspend/resume events
# $1 = pre (going to sleep) or post (waking up)

if [[ "$1" == "post" ]]; then
    /usr/bin/cpustate daemon
fi