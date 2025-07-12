from solve_puzzle import closest_point_on_circle, simulate_total_frames
from variables import stick_vectors, slot_pos, START_POS

def precompute_closest_points(pieces, radius):
    insertion_points = {}

    # Regular piece-to-piece entries
    for i in range(pieces):
        for j in range(pieces):
            if i != j:
                insertion_points[(i, j)] = closest_point_on_circle(*slot_pos[i], *slot_pos[j], radius)

    # From starting pos to each slot
    for j in range(pieces):
        insertion_points[(None, j)] = closest_point_on_circle(*START_POS, *slot_pos[j], radius)

    return insertion_points

def precompute_movement_frames(pieces, insertion_points):
    movement_cache = {}

    # Regular piece-to-piece entries
    for i in range(pieces):
        for j in range(pieces):
            if i != j:
                target_x, target_y = insertion_points[(i, j)]
                frames = simulate_total_frames(*slot_pos[i], target_x, target_y, stick_vectors)
                movement_cache[(i, j)] = frames

    # From starting pos to each slot
    for j in range(pieces):
        target_x, target_y = insertion_points[(None, j)]
        frames = simulate_total_frames(*START_POS, target_x, target_y, stick_vectors)
        movement_cache[(None, j)] = frames

    return movement_cache
