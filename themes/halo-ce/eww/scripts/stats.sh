#!/bin/sh
# Prints one JSON line with the values eww has no built-in variable for.
# Polled by eww.yuck every 2 seconds.

# CPU temperature: the "coretemp" sensor's temp1 is the whole-CPU (package) value.
# hwmon numbers can change between boots, so find the folder by name.
hw=$(grep -l '^coretemp$' /sys/class/hwmon/hwmon*/name | head -1)
cpu_temp=$(( $(cat "${hw%name}temp1_input") / 1000 ))

# NVIDIA GPU: temperature and usage in one call ("42, 9").
gpu=$(nvidia-smi --query-gpu=temperature.gpu,utilization.gpu --format=csv,noheader,nounits 2>/dev/null)
gpu_temp=${gpu%%,*}; gpu_temp=${gpu_temp:-0}
gpu_util=${gpu##*, }; gpu_util=${gpu_util:-0}

# Uptime as "02D 14H 32M". Also kept in seconds for the rate math below.
read -r up _ < /proc/uptime
uptime=$(echo "$up" | awk '{s=int($1); printf "%02dD %02dH %02dM", s/86400, s%86400/3600, s%3600/60}')

# Fn+Q power mode: low-power / balanced / performance
mode=$(cat /sys/firmware/acpi/platform_profile)

# Battery. It only reports power draw while discharging (value is in microwatts).
bat=/sys/class/power_supply/BAT0
capacity=$(cat $bat/capacity)
status=$(cat $bat/status)                       # Charging / Discharging / Full / Not charging
if [ "$status" = Discharging ]; then
    power=$(awk '{printf "%.1f W", $1/1000000}' $bat/power_now)
else
    power="AC"
fi

# Speeds = (counter now - counter last time) / seconds between the two polls.
# Counters: /proc/diskstats field 6 = sectors read, field 10 = sectors written (512 bytes each);
#           /proc/net/dev = bytes received / sent, summed over all interfaces except lo.
# The previous sample lives in RAM ($XDG_RUNTIME_DIR is a tmpfs), so nothing touches the disk.
nvme=$(awk '$3 == "nvme0n1" {print $6}' /proc/diskstats)
hdd=$(awk '$3 == "sda" {print $6, $10}' /proc/diskstats)       # read, written
net=$(awk 'NR > 2 && $1 != "lo:" {rx += $2; tx += $10} END {print rx, tx}' /proc/net/dev)
now="$up $nvme $hdd $net"

state=${XDG_RUNTIME_DIR:-/tmp}/eww-rates
last=$(cat "$state" 2>/dev/null || echo "$now")
echo "$now" > "$state"

# Fields per sample: 1 uptime, 2 nvme read, 3 hdd read, 4 hdd written, 5 rx, 6 tx.
# Prints: nvme read MB/s, hdd read MB/s, hdd write MB/s, rx KB/s, tx KB/s
rates=$(echo "$last $now" | awk '{
    dt = $7 - $1; if (dt <= 0) dt = 1
    printf "%.1f %.1f %.1f %.0f %.0f", ($8-$2)*512/dt/1e6, ($9-$3)*512/dt/1e6, ($10-$4)*512/dt/1e6, ($11-$5)/dt/1e3, ($12-$6)/dt/1e3
}')
set -- $rates

printf '{"cpu_temp":%s,"gpu_temp":%s,"gpu_util":%s,"uptime":"%s","mode":"%s","power":"%s","bat":%s,"bat_status":"%s","nvme_read":%s,"hdd_read":%s,"hdd_write":%s,"rx":%s,"tx":%s}\n' \
    "$cpu_temp" "$gpu_temp" "$gpu_util" "$uptime" "$mode" "$power" "$capacity" "$status" "$1" "$2" "$3" "$4" "$5"
