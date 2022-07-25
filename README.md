
# syglass_surface_to_surface_colocalization
Contributors: Emma Kupec, Nathan Spencer

## Description
Compares the distance between surfaces and pairs them based on a distance threshold. Surfaces are recolored to 
red/green in a pair and blue when a surface is not paired.

## Dependencies
    pip install trimesh
    pip install syglass
    pip install numpy
    pip install pyvista
## Usage
- Open `surface_to_surface.py` in a text editor such as VS Code or a Python IDE
- Modify the script's constants. Change the `PROJECT_PATH` to the pathway in which your project resides. Change the `EXPERIMENT_NAME` so that it reflects the current experiment. The `DISTANCE_THRESHOLD` determines the distance apart two surfaces must be to be considered colocalized. The distance is measured in the project's units.
- With your syGlass project closed, run `surface_to_surface.py`. There will be printed progress updates as surfaces are processed, compared, and sorted.
- When the results are printed, launch your syGlass project and view the results.
