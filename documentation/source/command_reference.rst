Command Reference
=================

vta
---
.. code-block:: none

   $ vta [-h] [--version] COMMAND ...

VTA is a suite of tools for analysing experimental results in the computer
vision field of visual tracking. VTA provides several tools for various tasks
common in conducting such research.

Optional Arguments
..................
.. program:: vta

.. option:: -h, --help

   Display a command's help, then exit.

.. option:: --version

   Print the version of VTA, then exit.

Commands
........
These are the commands available in VTA.

.. describe:: dataset

   Download a video data set, or part of a data set.

vta dataset
-----------
.. code-block:: none

   $ vta dataset [-h] [--list-subsets] [--root-directory DIR] [--force]
                   [--sequences SEQUENCE [SEQUENCE ...]]
                   DATASET [SUBSET [SUBSET ...]]

This command can be used to download common data sets used in visual tracking
research. It can also be used to download individual sequences from those data
sets.

Positional Arguments
....................
.. option:: DATASET {otb | vot}

   The data set to download, or from which to download sequences.

.. option:: SUBSETS {2013 | 2014 | 2015 | 2016 | 2017 | tb50 | tb100}

   An optional subset of the ``DATASET`` to download. If omitted, the full data
   set is downloaded. Note that not all subsets are available for all data sets.
   For example, ``tb50`` does not exist in the VOT data set. If incompatible
   data set and subsets are specified, an error will be printed and nothing will
   be downloaded. Use ``vta dataset --list-subsets DATASET`` to view subsets
   available for a particular data set.

Optional Arguments
..................
.. program:: dataset

.. option:: -h, --help

   Display a command's help, then exit.

.. option:: --list-subsets

   Show the subsets that are valid for the specified ``DATASET``.

.. option:: --root-directory DIR

   The root directory in which to download the data. A subdirectory will be
   created that matches the name of the ``DATASET``. For example, if you specify
   ``vta dataset otb --root- directory=~/data``, the directory *~/data/otb* will
   be created. The default is *~/Videos*.

.. option:: --force

   Download requested data even if it is already present.

.. option:: --sequences SEQUENCE [SEQUENCE ...]

   A space separated list of individual sequences to download from the
   ``DATASET``. If omitted, all sequences from the specified ``DATASET`` and
   ``SUBSETS`` are downloaded. If a sequence is not in the ``DATASET`` and
   ``SUBSETS``, an error is printed to the console, but downloading will
   continue. Sequences are case sensitive, and must match the name in the
   ``DATASET``.
