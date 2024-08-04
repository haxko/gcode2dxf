# License...



import sys
import ezdxf
import tkinter as tk
from tkinter import filedialog
import re

# If the script gets a Filepath as argument it acts like a post processor, 
# and save the result to the same location. If not, it will show an open and save dialoge
postprocessormode = True
try: 
    gfile_input = sys.argv[1]
except:
    postprocessormode = False
    root = tk.Tk()
    root.withdraw()
    gfile_input = filedialog.askopenfilename(filetypes=(('gcode','*.gcode'),('all files','*.*')))

dfile_output = re.sub('.gcode$', '.dxf', gfile_input)

# Open gcode file
with open(gfile_input, "r") as gcode:
    lines = gcode.readlines()

path_segments = []
current_segment = []

# Some regular expressions to capture the corresponding data 
xy_pattern = r"G1\s+X(-?\d*\.?\d+)\s+Y(-?\d*\.?\d+)"
z_pattern = r"Z(-?\d*\.?\d+)"
e_pattern = r"E(-?\d*\.?\d+)"
f_pattern = r"F(\d+)"

def start_new_segment(x, y):
    if current_segment:
        path_segments.append(current_segment)
    return [[x, y]]

current_z = 0

# First pass: determine the maximum F value (travel speed)
max_f = 0
for line in lines:
    f_match = re.search(f_pattern, line)
    if f_match:
        f_value = int(f_match.group(1))
        max_f = max(max_f, f_value)
travel_f = f"F{str(max_f)}"

for i, line in enumerate(lines):
    # Skip comment lines
    if line.startswith(";"):
        continue

    # Moving Z (z-hob or layer change) indicates a new semgment,
    # so do travel moves (move with travel_f),
    # as well as moves without extrusion and retractions
    match = re.search(xy_pattern, line)
    if match:
        x, y = map(float, match.groups())
        # Check for Z movement
        z_match = re.search(z_pattern, line)
        if z_match:
            new_z = float(z_match.group(1))
            if new_z != current_z:
                current_segment = start_new_segment(x, y)
                current_z = new_z
                continue
        # Check for travel moves
        if travel_f in line or (i > 0 and travel_f in lines[i-1]):
            current_segment = start_new_segment(x, y)
        # Check for extrusion
        elif re.search(e_pattern, line):
            current_segment.append([x, y])
        else:
            # This might be a travel move without explicit F30000
            current_segment = start_new_segment(x, y)
    
    # Check for retraction moves
    elif "G1 E-" in line:
        if current_segment:
            path_segments.append(current_segment)
            current_segment = []

# Add the last segment if it's not empty
if current_segment:
    path_segments.append(current_segment)

# Setup dxf file
doc = ezdxf.new()
msp = doc.modelspace()

# Create dxf with separate polylines for each path segment
for segment in path_segments:
    # Only create a polyline if there's more than one point
    if len(segment) > 1:
        msp.add_lwpolyline(segment)

# Show save as dialog if not postprocessormode
if not postprocessormode:
    dfile_output = filedialog.asksaveasfilename(filetypes=(('dxf','*.dxf'),('all','*.*')))
# Save the file
doc.saveas(dfile_output)
