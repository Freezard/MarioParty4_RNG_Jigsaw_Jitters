import math

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def closest_point_on_circle(start_x, start_y, slot_x, slot_y, radius, pad=0.00015):
    dx, dy = start_x - slot_x, start_y - slot_y
    dist = math.hypot(dx, dy)

    if dist == 0:
        return slot_x, slot_y
    scale = (radius - pad) / dist

    return slot_x + dx * scale, slot_y + dy * scale

best_frames = float('inf')

def simulate_total_frames(start_x, start_y, target_x, target_y, vectors):
    # Step 1: Compute direction to target
    gx = target_x - start_x
    gy = target_y - start_y
    gmag = math.hypot(gx, gy)
    gx /= gmag
    gy /= gmag

    # Step 2: Find best stick vector aligned to direction
    best_score = float('-inf')
    best_dx = best_dy = 0
    best_input = (128, 128)

    for (sx, sy), (dx, dy) in vectors:
        dmag = math.hypot(dx, dy)
        if dmag == 0:
            continue
        score = (dx / dmag) * gx + (dy / dmag) * gy
        if score > best_score:
            best_score = score
            best_dx = dx
            best_dy = dy
            best_input = (sx, sy)

    # Step 3: Move with that stick vector until insertion
    x, y = start_x, start_y
    frames = 0
    prev_dist = distance(x, y, target_x, target_y)

    while True:
        x += best_dx
        y += best_dy
        frames += 1

        new_dist = distance(x, y, target_x, target_y)

        if new_dist > prev_dist:
            break

        prev_dist = new_dist

        if frames > 300:
            break

    return frames, best_input
