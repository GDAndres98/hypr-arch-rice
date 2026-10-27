#!/bin/sh
# Lock screen: the red "eye" lamp. hyprlock runs this every second (cmd[update:1000]) and shows the output.
# Lit on even seconds, dark on odd ones. It's a script because hyprlock reads $ in its config as its own variables.
if [ $(( $(date +%s) % 2 )) -eq 0 ]; then
    echo "<span foreground='#ff2a2a'>●</span>"
else
    echo "<span foreground='#3c3d40'>●</span>"
fi
