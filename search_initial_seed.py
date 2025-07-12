from datetime import datetime, timezone

start_date = datetime(2025, 6, 27, 5, 20, 29, tzinfo=timezone.utc)
unix_start = int(start_date.timestamp())

STEP = 40500000
TARGET = 49802222 # 02F7EBEE
CAP = 4294967296 # FFFFFFFF
DIRECTION = 1
current = 13040598 # 00C6FBD6 -> D8E0474E

print(f"Start date: {start_date.strftime('%Y-%m-%d %H:%M:%S')}, "
      f"Start seed: {current:08X}, Target: {TARGET:08X}")

# Will loop forever, so needs to be stopped manually
while True:
    after = (current ^ 0xD826BC98) & 0xFFFFFFFF

    if after == TARGET:
        end_date = datetime.fromtimestamp(unix_start, tz=timezone.utc)
        print(f"Found target {after:08X} at date {end_date.strftime("%Y-%m-%d %H:%M:%S")}")

    if DIRECTION == -1 and current - STEP < 0:
        current = CAP + (current - STEP)
    elif DIRECTION == 1 and current + STEP > CAP:
        current = 0 + (current + STEP) - CAP
    else:
        current = current + STEP * DIRECTION
    unix_start += DIRECTION
