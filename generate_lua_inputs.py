from solve_puzzle import closest_point_on_circle, simulate_total_frames
from utils import get_absolute_path
from variables import stick_vectors, slot_pos
from variables import RADIUS, INSERT_COOLDOWN, INSERT_COOLDOWN_FINAL

def can_insert(piece_x, piece_y, slot_x, slot_y, radius, pad=0.000015):
    dx = piece_x - slot_x
    dy = piece_y - slot_y
    return (dx * dx + dy * dy) < ((radius + pad) ** 2)

def format_time(frames):
    seconds = frames // 60
    remainder = frames % 60

    # Convert to displayed centiseconds.
    # Not completely accurate for Mario Party 4, but close enough
    centiseconds = round(remainder * 100 / 60)
    return f'{seconds}"{centiseconds:02}'

def rotation_frames(rotation_value):
    if rotation_value == 0:
        return 0
    elif rotation_value == 2:
        return 39
    else: # 1 or 3
        return 18

# ---- Main Simulation ----

piece_order = [20,18,9,15,24,29,21,3,5,6,10,0,11,4,14,22,28,26,19,27,12,13,25,16,8,7,23,17,2,1]
piece_rotations = [1,1,1,1,3,0,3,0,3,0,2,0,1,1,0,1,0,0,0,1,0,3,2,0,3,0,2,1,3,3]

start_x, start_y = 0, 0
total_frames = 0

all_inputs = [] # Stores one dict per piece

for i, piece in enumerate(piece_order):
    slot_x, slot_y = slot_pos[piece]
    target_x, target_y = closest_point_on_circle(start_x, start_y, slot_x, slot_y, RADIUS)
    movement_frames, best_input = simulate_total_frames(start_x, start_y, target_x, target_y, stick_vectors)
    rotation_delay = rotation_frames(piece_rotations[i])

    frames_needed = max(movement_frames, rotation_delay)
    total_frames += frames_needed + (INSERT_COOLDOWN_FINAL if i == len(piece_order) - 1 else INSERT_COOLDOWN)

    start_x, start_y = slot_x, slot_y

    # Save info to be used in the Lua script
    all_inputs.append([{
        "x": best_input[0],
        "y": best_input[1],
        "movement_frames": movement_frames,
        "frames_needed": frames_needed,
        "rotation": piece_rotations[i]
    }])

    print(f"Piece {i + 1}: {best_input} \t {frames_needed}")

currFrame = 0

# Generate Lua script. Not entirely accurate, needs manual adjustments
file_path = get_absolute_path('auto_solver_inputs.lua')

with open(file_path, "w", encoding="utf-8") as f:
    f.write("if currFrame < 0 then\n")
    for piece in all_inputs:
        for step in piece: # If all_inputs is flat (1 step per piece)
            rot = step['rotation']
            x, y = step['x'], step['y']
            move_frames = step['movement_frames']
            rot_frames = 0
            rot_button = ""

            if rot == 1:
                rot_frames = 18
                rot_button = "R"
            elif rot == 3:
                rot_frames = 18
                rot_button = "L"
            elif rot == 2:
                rot_frames = 39
                rot_button = "L"

            insert_frame = max(move_frames, rot_frames)

            if rot != 0:
                f.write(f"elseif currFrame < {currFrame + 1} then\n")
                f.write(f"    SetMainStickX({x})\n")
                f.write(f"    SetMainStickY({y})\n")
                f.write(f"    PressButton('{rot_button}')\n")

            f.write(f"elseif currFrame < {currFrame + insert_frame } then\n")
            f.write(f"    SetMainStickX({x})\n")
            f.write(f"    SetMainStickY({y})\n")
            f.write(f"elseif currFrame < {currFrame + insert_frame + 2} then\n")
            f.write("    PressButton('A')\n")
            f.write(f"elseif currFrame < {currFrame + insert_frame + INSERT_COOLDOWN} then\n")

            currFrame += insert_frame + INSERT_COOLDOWN

    f.write("end")

print(f"Total frames: {total_frames}")
print(f"Final time: {format_time(total_frames)}")
