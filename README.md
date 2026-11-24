### Summary ###
Following the paper:

Gao Y, Bouix S. Statistical Shape Analysis using 3D Poisson
Equation---A Quantitatively Validated Approach. Medical Image
Analysis. 2016 Jan 15.

this repository contains code to perform statistical analysis on 3D
shapes with arbitrary topology. It contains an iterative 3D Poisson
equation solver using ITK (VNL) sparse system.

### What is this repository for? ###

* Statistical shape analysis

### How do I get set up? ###

This repository is a [3D Slicer](https://www.slicer.org) extension and provides
the **PoissonShapeAnalysis** CLI module in the **Shape Analysis** category. It
only depends on 3D Slicer (and the ITK/VTK libraries bundled with it).

* Install it from 3D Slicer's Extension Manager (once the extension is published), or
* Build it against a Slicer build tree following the
  [Slicer extension build instructions](https://slicer.readthedocs.io/en/latest/developer_guide/extensions.html#build-an-extension).

### Docker

The standalone command-line version is also available on Docker: https://hub.docker.com/r/gaoyi/spom/

```bash
docker pull gaoyi/spom
```

### How to use ###

Given two groups of 3D shapes, the module performs a statistical analysis and
outputs the mean shape of all the input shapes; the regions where the two
groups differ significantly are highlighted on the mean shape.

**In 3D Slicer:**

1. Save each shape as a binary volumetric image (NIfTI, NRRD, MHA/MHD, etc.),
   one shape per file.
2. Put all volumes of group 1 into one folder and all volumes of group 2 into
   another folder. Files inside each folder are read in name-sorted order;
   hidden files and sub-folders are ignored.
3. Open the **SPoM Shape Analysis** module (category **Shape Analysis**). The
   underlying **PoissonShapeAnalysis** CLI module is also available; the
   scripted module additionally configures the p-value display.
4. Set the **Group 1 folder** and **Group 2 folder** to the two folders above.
5. Enable **Perform shape registration first** if the shapes are not already
   registered.
6. Set the output **Mean shape volume** and **Mean shape model**, then click
   **Apply**. The output model's **pValue** scalar is activated and displayed
   with a hot-to-cold table: 0 is red, values approaching 0.05 are blue, and
   values at or above 0.05 are neutral grey. The scalar range mode is set to
   Manual with a display range of 0 to 0.05.

**From the command line:**

```bash
./PoissonShapeAnalysis --shapeNameList1 /path/to/group1 \
                       --shapeNameList2 /path/to/group2 \
                       --meanImageName meanShape.nrrd \
                       --meanVTKName meanShape.vtp \
                       [--doRegistration]
```

`--shapeNameList1`/`--shapeNameList2` (short flags `-a`/`-b`) each take a folder
containing one group's shape volumes. `--doRegistration` is a switch and is
disabled by default.

### Who do I talk to? ###

* Yi Gao (gaoyi@gatech.edu)

### Usage agreement ###

In scientific publications (journal publications, conference papers,
technical reports, presentations at conferences and meetings) that use
this code, you should cite the following paper:

Gao Y, Bouix S. Statistical Shape Analysis using 3D Poisson
Equation---A Quantitatively Validated Approach. Medical Image
Analysis. 2016 Jan 15.

### To do ###

