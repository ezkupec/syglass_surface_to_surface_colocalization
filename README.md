script
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
- Change the `PROJECT_PATH`, `EXPERIMENT_NAME`, and `MESH_PATH` variables to represent your appropriate pathways
- With your syGlass project closed, run `surface_to_surface.py`. There will be printed progress updates as surfaces are processed, compared, and sorted.
- When the results are printed, launch your syGlass project and view the results.
