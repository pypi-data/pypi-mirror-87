# welleng
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/pro-well-plan/pwptemp/blob/master/LICENSE.md)
[![PyPI version](https://badge.fury.io/py/welleng.svg)](https://badge.fury.io/py/welleng)
[![Downloads](https://static.pepy.tech/personalized-badge/welleng?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/welleng)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

[welleng] aspires to be a collection of useful tools for Wells/Drilling Engineers, kicking off with a range of well trajectory analysis tools.

  - Generate survey listings and interpolation with minimum curvature
  - Calculate well bore uncertainty data (currently utilizing the ISCWSA MWD Rev4 model)
  - Calculate well bore clearance and Separation Factors (SF)
    - standard ISCWSA method
    - new mesh based method using the [Flexible Collision Library]

## New Features!

  - **Fast visualization of well trajectory meshes:** addition of the `visual` module for quick and simple viewing and QAQC of well meshes.
  - **Mesh Based Collision Detection:** the current method for determining the Separation Factor between wells is constrained by the frequency and location of survey stations or necessitates interpolation of survey stations in order to determine if Anti-Collision Rules have been violated. Meshing the well bore inherrently interpolates between survey stations and as such is a more reliable method for identifying potential well bore collisions, especially wth more sparse data sets.
  - More coming soon!

## Tech

[welleng] uses a number of open source projects to work properly:

* [trimesh] - awesome library for loading and using triangular meshes
* [numpy] - the fundamental package for scientific computing with Python
* [scipy] - a Python-based ecosystem of open-source software for mathematics, science, and engineering
* [vedo] - a python module for scientific visualization, analysis of 3D objects and point clouds based on VTK.

## Installation

[welleng] requires [trimesh], [numpy] and [scipy] to run. Other libraries are optional depending on usage and to get [python-fcl] running on which [trimesh] is built may require some additional installations. Other than that, it should be an easy pip install to get up and running with welleng and the minimum dependencies.

```
pip install welleng
```
For developers, the repository can be cloned and locally installed by in your GitHub directory via your preferred Python env.
```
git clone https://github.com/jonnymaserati/welleng.git
cd welleng
pip install -e .
```
Make sure you include that `.` in the final line (it's not a typo) and this ensures that any changes to your development version are immediately implemented on save.

## Quick Start

Here's an example using `welleng` to construct a couple of simple well trajectories with `numpy`, creating survey listings for the wells with well bore uncertainty data, using these surveys to create well bore meshes and finally printing the results and plotting the meshes with the closest lines and SF data.

```
import welleng as we
import numpy as np
from tabulate import tabulate

# construct simple well paths
print("Constructing wells...")
md = np.linspace(0,3000,100) # 30 meter intervals to 3000 mTD
inc = np.concatenate((
    np.zeros(30), # vertical section
    np.linspace(0,90,60), # build section to 60 degrees
    np.full(10,90) # hold section at 60 degrees
))
azi1 = np.full(100,60) # constant azimuth at 60 degrees
azi2 = np.full(100,225) # constant azimuth at 225 degrees

# make a survey object and calculate the uncertainty covariances
print("Making surveys...")
survey_reference = we.survey.Survey(
    md,
    inc,
    azi1,
    error_model='ISCWSA_MWD'
)

# make another survey with offset surface location and along another azimuth
survey_offset = we.survey.Survey(
    md,
    inc,
    azi2,
    start_nev=[100,200,0],
    error_model='ISCWSA_MWD'
)

# generate mesh objects of the well paths
print("Generating well meshes...")
mesh_reference = we.mesh.WellMesh(
    survey_reference
)
mesh_offset = we.mesh.WellMesh(
    survey_offset
)

# determine clearances
print("Setting up clearance models...")
c = we.clearance.Clearance(
    survey_reference,
    survey_offset
)

print("Calculating ISCWSA clearance...")
clearance_ISCWSA = we.clearance.ISCWSA(c)

print("Calculating mesh clearance...")
clearance_mesh = we.clearance.MeshClearance(c, sigma=2.445)

# tabulate the Separation Factor results and print them
results = [
    [md, sf0, sf1]
    for md, sf0, sf1
    in zip(c.reference.md, clearance_ISCWSA.SF, clearance_mesh.SF)
]

print("RESULTS\n-------")
print(tabulate(results, headers=['md', 'SF_ISCWSA', 'SF_MESH']))

# get closest lines between wells
lines = we.visual.get_lines(clearance_mesh)

# plot the result
we.visual.plot(
    [mesh_reference.mesh, mesh_offset.mesh], # list of meshes
    names=['reference', 'offset'], # list of names
    colors=['red', 'blue'], # list of colors
    lines=lines
)

print("Done!")
```
This results in a quick, interactive visualization of the well meshes that's great for QAQC.

![image](https://user-images.githubusercontent.com/41046859/100718537-c3b12700-33bb-11eb-856e-cf1bd77d3cbf.png)

For more examples, check out the [examples].

## Todos

 - Generate a scene of offset wells to enable fast screening of collision risks (e.g. hundreds of wells in seconds)
 - Well trajectory planning - construct your own trajectories using a range of methods (and of course, including some novel ones)
 - More error models
 - WebApp for those that just want answers
 - Viewer - a 3D viewer to quickly visualize the data and calculated results - **DONE!**

It's possible to generate data for visualizing well trajectories with [welleng], as can be seen with the rendered scenes below, but it can me made more simple and intuitive.
ISCWSA Standard Set of Well Paths | Equinor's Volve Wells
---|---
![image](https://user-images.githubusercontent.com/41046859/97724026-b78c2e00-1acc-11eb-845d-1220219843a5.png) | ![image](https://media-exp1.licdn.com/dms/image/C5612AQEBKagFH_qlqQ/article-inline_image-shrink_1500_2232/0?e=1609977600&v=beta&t=S3C3C_frvUCgKm46Gtat2-Lor7ELGRALcyXbkwZyldM)
---
The ISCWSA standard set of well paths for evaluating clearance scenarios and Equinor's [volve] wells rendered in [blender]. See the [examples] for the code used to generate the [volve] scene, extracting the data from the [volve] EDM.xml file.

License
----

LGPL v3

Please note the terms of the license. Although this software endeavors to be accurate, it should not be used as is for real wells. If you want a production version or wish to develop this software for a particular application, then please get in touch with [jonnycorcutt], but the intent of this library is to assist development.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [jonnycorcutt]: <mailto:jonnycorcutt@gmail.com>
   [welleng]: <https://github.com/jonnymaserati/welleng>
   [Flexible Collision Library]: <https://github.com/flexible-collision-library/fcl>
   [trimesh]: <https://github.com/mikedh/trimesh>
   [python-fcl]: <https://github.com/BerkeleyAutomation/python-fcl>
   [vedo]: <https://github.com/marcomusy/vedo>
   [numpy]: <https://numpy.org/>
   [scipy]: <https://www.scipy.org/>
   [examples]: <https://github.com/jonnymaserati/welleng/tree/main/examples>
   [blender]: <https://www.blender.org/>
   [volve]: <https://www.equinor.com/en/how-and-why/digitalisation-in-our-dna/volve-field-data-village-download.html>
