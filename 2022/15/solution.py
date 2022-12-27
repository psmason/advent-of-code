#!/usr/bin/env python3

import fileinput
import re

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

_SENSOR_RE = re.compile("^Sensor at x=([\-0-9]+), y=([0-9]+):")
_BEACON_RE = re.compile("closest beacon is at x=([\-0-9]+), y=([0-9]+)$")

def get_sensors_and_beacons(lines):
    sensors = []
    beacons = []
    for line in lines:
        sensor_match = _SENSOR_RE.findall(line)
        sensor_x, sensor_y = sensor_match[0][0], sensor_match[0][1]
        sensors.append((int(sensor_x), int(sensor_y)))

        beacon_match = _BEACON_RE.findall(line)
        beacon_x, beacon_y = beacon_match[0][0], beacon_match[0][1]
        beacons.append((int(beacon_x), int(beacon_y)))
    return sensors, beacons

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_cols_without_beacon(row, sensors, beacons):
    cols_without_beacon = set()
    
    for i in range(len(sensors)):        
        sensor, beacon = sensors[i], beacons[i]
        d = manhattan_distance(sensor, beacon)
        # Sensors do not influence the requested row
        if row < sensor[1]-d:
            continue
        if sensor[1]+d < row:
            continue
        
        row_distance = abs(sensor[1]-row)
        for col_offset in range(d-row_distance+1):
            cols_without_beacon.add(sensor[0]-col_offset)
            cols_without_beacon.add(sensor[0]+col_offset)

    # remove known beacons
    for beacon in beacons:
        if beacon[1] == row and beacon[0] in cols_without_beacon:
            cols_without_beacon.remove(beacon[0])

    return cols_without_beacon

# Part 1
lines = get_input()
sensors, beacons = get_sensors_and_beacons(lines)
cols_without_beacon = find_cols_without_beacon(2*1000*1000, sensors, beacons)
print(len(cols_without_beacon))

# Part 2
def find_cols_without_beacon_v2(row, sensors, beacons):
    cols_maybe_with_beacon = set()

    # inclusive intervals
    intervals_without_beacon = []
    
    for i in range(len(sensors)):        
        sensor, beacon = sensors[i], beacons[i]
        d = manhattan_distance(sensor, beacon)
        row_distance = abs(sensor[1]-row)

        if row_distance < d:
            col_offset = d-row_distance
            intervals_without_beacon.append((sensor[0]-col_offset, sensor[0]+col_offset))

    # sorting by interval start
    intervals_without_beacon = sorted(intervals_without_beacon, key=lambda x: x[0])

    merged_result = []
    merged_result.append(intervals_without_beacon[0])
    
    for i in range(1, len(intervals_without_beacon)):
        merge_candidate = merged_result[-1]

        interval = intervals_without_beacon[i]
        if merge_candidate[1]+1 < interval[0]:
            # new merge candidate
            merged_result.append(interval)
        else:
            merge_candidate = (merge_candidate[0], max(merge_candidate[1], interval[1]))
            merged_result[-1] = merge_candidate

    return merged_result

def find_hidden_beacon(row, intervals_without_beacon, max_range):
    relevant_intervals = [interval for interval in intervals_without_beacon if interval[1] > 0 and interval[0] < max_range]
    if len(relevant_intervals) > 1:
        print(row, relevant_intervals)

lines = get_input()
sensors, beacons = get_sensors_and_beacons(lines)
for row in range(4*1000*1000):
    find_hidden_beacon(row, find_cols_without_beacon_v2(row, sensors, beacons), 4*1000*1000)

