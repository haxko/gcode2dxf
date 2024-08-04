
# gcode2dxf

This is a small python script that convers 3D-printer g-code to a DXF-file.
It works standalone or as a post-processor script for your favorite slicer.

## Why would you want that?
At haxko we use it in combination with an old engraving laser. If we want to use a vector graphic with it, the only really accepts DXF-files, but will then only trace paths and not fill them. For that reason we need to add "fill lines" to our vector files and a slicer is a tool that is good at it an most of our members are familiar with.

## Installation
- You will need Python to execute this script.
- Download and copy the gcode2dxf.py file to a place on your computer where you want to keep it.
- You will need "ezdxf" for it to run, so execute `pip install ezdxf` in your CMD or Terminal*

*for stand alone mode you can also install it in an venv, but not for a post-processor
### For stand alone mode
You are done, to use it just run `python gcode2dxf.py`.
A window will pop up and ask you to chose a G-Code file, after chosing it another window will pop up and ask you where you want to save your DXF.
### For use as a post-processor
This was successfully tested with PrusaSlicer and OrcaSlicer, so it should also work with Slic3r or Bambu Studio, but thats untested.

**Important for Linux users:** Don't use the FlatPak version of the slicer! The script needs ezdxf to run and you would need to get it installed inside the Sandbox of your FlatPak. Use the Appimage from GitHub (Prusa/Orca).
- In your slicer you might want to add a new "Printer Setting" (PrusaSlicer) or "Process" (OrcaSlicer) for your Dxf generation.
- PrusaSlicer: go to `Printer Settings tab > Output options > Post-processing scripts` add `python <path_to_folder>/gcode2dxf.py` (replace <path_to_folder> with the path to the folder containg the script)
- OrcaSlicer: `Prepare tab > Process > Others > Post-processing Scripts` add `python <path_to_folder>/gcode2dxf.py` (replace <path_to_folder> with the path to the folder containg the script)
- change the Filename format (above Post-processing scripts) to something like `[input_filename_base]_[printer_preset].dxf` so it gets saved with the .dxf extention and not .gcode as default
- On Linux you might have to do a `chmod 0777 gcode2dxf.py` for it to be executable by the slicer

## Slicer Settings
The settings will depend on what your setup is. In the SlicerSettings folder we have settings and 3mf-files that you can import into your slicer as a starting point.
For the post pocessor to work you will still have to follow the "For use as a post-processor" steps above once you imported the settings

Some important settings (already done for you, if you use our files):
- The travel speed has to be the fastest speed in your settings
- The gcode "flavour" should be `marlin (legacy)` (others might work but not tested)
- Try to keep the filesize low (deactivate saving a preview image in the g-code)
## Workflow
- Drag and drop (or import) a SVG vector file into your slicer (yes that works)
- It will ask you for the height. 0.05mm would be one layer, so set it to 0.05 if you want the lase to make one pass, or 0.1mm for two passes. Don't go crazy with the thickness.
- Chose your favourite first layer infill Pattern and number of Perimiters/Wall-loops to get your desired look.
- Hit slice.
- Check if you like it and the number of layers.
- Klick on "Export G-code" and choose where you want to have your DXF file, klick OK.
- Your done, use it for what ever you need it for.
   
   
   
![You can Donate if you want, info at haxko.space](images/Donate.svg)