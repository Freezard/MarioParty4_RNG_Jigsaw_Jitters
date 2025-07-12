import time
import json
import multiprocessing
from generate_puzzle import generate_puzzle
from precompute import precompute_closest_points, precompute_movement_frames
from utils import get_absolute_path
from variables import PIECES, RADIUS, INSERT_COOLDOWN, INSERT_COOLDOWN_FINAL

def process_range(start_seed, end_seed, filename):
    results = []

    insertion_points = precompute_closest_points(PIECES, RADIUS)
    movement_cache = precompute_movement_frames(PIECES, insertion_points)

    for seed in range(start_seed, end_seed):
        pattern, rotations = generate_puzzle(PIECES, seed)

        total_frames = 0
        is_valid = True
        prev_piece = None

        for i, piece in enumerate(pattern):
            movement_frames, _ = movement_cache[(prev_piece, piece)]

            rotation = rotations[i]
            if rotation == 2:
                rotation_delay = 39
            elif rotation in (1, 3):
                rotation_delay = 18
            else:
                rotation_delay = 0

            frames_needed = max(movement_frames, rotation_delay)
            total_frames += frames_needed + (INSERT_COOLDOWN_FINAL if i == len(pattern) - 1 else INSERT_COOLDOWN)
            prev_piece = piece

            # Only write fast solutions to file
            if total_frames > 2520:
                is_valid = False
                break

        if is_valid:
            results.append({
              'seed': f"{seed:08X}",
              'pattern': pattern,
              'rot': rotations,
              'rot1': rotations.count(1) + rotations.count(3),
              'rot2': rotations.count(2),
              'frames': total_frames
          })

    # Sort by frames (descending)
    results.sort(key=lambda r: r["frames"], reverse=True)

    # Save to file
    file_path = get_absolute_path(filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in results:
            json_line = json.dumps(entry, separators=(',', ':'))
            f.write(json_line + '\n')

# This will generate and solve puzzles based on provided starting seeds.
# Going through billions of seeds will take a long time!
# Add more processes to search faster, but be aware of your CPU's limitations.
# The fastest solutions will be saved to file
if __name__ == '__main__':
    start = time.perf_counter()

    # Define processes
    p1 = multiprocessing.Process(target=process_range, args=(4_000_000_000, 4_075_000_000, 'results_part1.json'))
    p2 = multiprocessing.Process(target=process_range, args=(4_075_000_000, 4_150_000_000, 'results_part2.json'))

    # Start processes
    p1.start()
    p2.start()

    # Wait for processes to finish
    p1.join()
    p2.join()

    print(f'Execution time: {time.perf_counter() - start:.2f} seconds')
