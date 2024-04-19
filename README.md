NRTK EXPLORER
=============

NRTK Explorer is a web application for exploring image datasets. It provides
insights of a image dataset in [COCO][3] format and it evaluate image
transformation and perturbation resilience of object recognition DL models. It
is built using [trame][1] by the [kitware][2] team.

![nrtk explorer](https://github.com/Kitware/nrtk-explorer/blob/d3df0ecf748664d806f09ad11e2bbd71a0bca1dd/screenshot.png?raw=true)

Features
--------

- Explore image datasets in COCO format.
- Apply parametrized image degradation (such as blur) to the images.
- Benchmark dataset resilience with a differential PCA|UMAP analysis of the
  embeddings of the images and its transformation.
- Evaluate object detection DL models in both the source images and its
  transformations.
- When possible it will attempt to utilize the user GPU as much as possible to
  speedup its computations.

Installing
----------

Install it from pypi:

```bash
pip install nrtk_explorer
```

Or, download and install it manually with:

```bash
curl -OL https://github.com/Kitware/nrtk-explorer/archive/refs/heads/main.zip
```

Inside the application source code top directory, install it with:

```
pip install -e .
```

Run the application:

```
nrtk_explorer
```

CLI flags and options
---------------------

- `-h|--help` show the help for the command line options, it inherit trame
  command line options and flags.
- `--dataset` specify the directory containing a json file describing a COCO
  image dataset. You can specify multiple directory using a comma `,` as a
  separator.

Contribute to NRTK_EXPLORER
---------------------------

Run tests with:

```bash
pytest
```

[1]: https://trame.readthedocs.io/en/latest/
[2]: https://www.kitware.com/
[3]: https://cocodataset.org/
