# Data Visualization Project

This is a library that help to visualize 3D images of data points.

## Installation

We can install directly from git URL:
```bash
pip install git+git://github.com/Xysss7/data_visualisation_project
```

Or browse to the directory where this file lives, and run:
```bash
pip install .
```
That command will download any dependencies we have

## Usage
Example
In the jupyter lab:

cell[1]:
```python
import datavisualization as dv

vertices = [0, 0, 0,
            1, 0, 0,
            1, 1, 0,
            0, 1, 0]
faces = [0, 1, 2,
         0, 2, 3]
point_data = [0.0, 1.0, 2.3, .5]
dv.passdata(vertices, faces, point_data)
```

cell[2]:
```python
dv.visualize(vertices, faces, point_data)
```

You will get 3D image visualized you data points.
