#!/bin/sh
# Prints the connected Bluetooth devices as one JSON array.
# Polled by eww.yuck every 5 seconds. Example:
#   [{"name":"WH-1000XM6","battery":42}]
# battery = -1 when the device doesn't report one.

# bluetoothctl waits forever if bluetoothd isn't running, hence the timeouts.
bt() { timeout 2 bluetoothctl "$@" 2>/dev/null; }

devices=
for mac in $(bt devices Connected | awk '$1 == "Device" {print $2}'); do
    info=$(bt info "$mac")
    # Alias = the name shown everywhere (the device's own name unless renamed). Escape " and \ for JSON.
    name=$(echo "$info" | sed -n 's/^\s*Alias: //p' | sed 's/[\\"]/\\&/g')
    # "Battery Percentage: 0x2a (42)": the number in brackets
    battery=$(echo "$info" | sed -n 's/^\s*Battery Percentage: .*(\([0-9]*\))/\1/p')
    devices="$devices${devices:+,}{\"name\":\"$name\",\"battery\":${battery:--1}}"
done

echo "[$devices]"
