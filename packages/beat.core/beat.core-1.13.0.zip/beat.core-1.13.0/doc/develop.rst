.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.backend.python module of the BEAT platform.  ..
..                                                                            ..
.. Redistribution and use in source and binary forms, with or without
.. modification, are permitted provided that the following conditions are met:

.. 1. Redistributions of source code must retain the above copyright notice, this
.. list of conditions and the following disclaimer.

.. 2. Redistributions in binary form must reproduce the above copyright notice,
.. this list of conditions and the following disclaimer in the documentation
.. and/or other materials provided with the distribution.

.. 3. Neither the name of the copyright holder nor the names of its contributors
.. may be used to endorse or promote products derived from this software without
.. specific prior written permission.

.. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
.. ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
.. WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
.. DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
.. FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
.. DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
.. SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
.. CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
.. OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
.. OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


.. _beat-core-local-development:

===================
 Local Development
===================

Go through the following sequence of commands:


.. code-block:: sh

   $ git checkout https://gitlab.idiap.ch/bob/bob.admin
   $ #install miniconda (version 4.4 or above required)
   $ conda activate base
   $ cd beat.backend.python #cd into this package's sources
   $ ../bob.admin/conda/conda-bootstrap.py --overwrite --python=3.6 beat-core-dev
   $ conda activate beat-core-dev
   $ #n.b.: docker must be installed on your system (see next section)
   $ buildout -c develop.cfg

These commands should download and install all non-installed dependencies and
get you a fully operational test and development environment.


Docker
------

This package depends on Docker_ and may use it to run user algorithms in a
container with the required software stack. You must install the Docker_ engine
and make sure the user running tests has access to it.

In particular, this package controls memory and CPU utilisation of the
containers it launches. You must make sure to enable those functionalities on
your installation.


Docker Setup
============

Make sure you have the ``docker`` command available on your system. For certain
operating systems, it is necessary to install ``docker`` via an external
virtual machine (a.k.a. the *docker machine*). Follow the instructions at `the docker website`_ before trying to
execute algorithms or experiments.

We use specific docker images to run user algorithms. Download the following
base images before you try to run tests or experiments on your computer::

  $ docker pull beatenv/beat.env.db.examples:1.4.1r0
  $ docker pull beatenv/beat.env.python:2.1.0r7
  $ docker pull beatenv/beat.env.cxxdev:2.0.0r4
  $ docker pull beatenv/beat.env.cxx:2.0.0r4

Optionally, you can also download other images to be able to re-run experiments
downloaded from the BEAT platform (not required for unit testing). These docker
images corresponds to the python environment available on the platform. Keep in
mind that at the moment you cannot use different environments to run each block
when you are using BEAT locally unless using the Docker executor. These images
can be found on the `beatenv docker hub repository`_.


Before pulling these images, you should check the registry as there might have
been new release (i.e. rX versions).

To run an experiment using docker you should specify the docker image when defining the experiment, then use the `--docker` flag when using `beat.cmdline`::

  $ beat experiment run --docker <experiment name>

You can find more information about running experiments locally using different executors in the "Experiments" section of "beat.cmdline" in `BEAT documentation`_.


Custom image development
------------------------

Scientific development evolving quickly, the platform provided runtime environments
may not contain everything you need for your algorithms to run. In that case, you
can prepare your own environment using the following git repository.

  $ git clone https://gitlab.idiap.ch/beat/beat.env.example

The examples provided there will allow you to build docker images suitable both
for algorithm execution and if needed database handling.

Instructions are provided in the repository.


Documentation
-------------

To build the documentation, just do:

.. code-block:: sh

   $ ./bin/sphinx-build doc sphinx



Testing
-------

After installation, it is possible to run our suite of unit tests. To do so,
use ``nose``:

.. code-block:: sh

   $ ./bin/nosetests -sv


.. note::

  Some of the tests for our command-line toolkit require a running BEAT
  platform web-server, with a compatible ``beat.core`` installed (preferably
  the same).  By default, these tests will be skipped. If you want to run
  them, you must setup a development web server and set the environment
  variable ``BEAT_CORE_TEST_PLATFORM`` to point to that address. For example::

   $ export BEAT_CORE_TEST_PLATFORM="http://example.com/platform/"
   $ ./bin/nosetests -sv

  .. warning::

    Do **NOT** run tests against a production web server.


If you want to skip slow tests (at least those pulling stuff from our servers)
or executing lengthy operations, just do::

  $ ./bin/nosetests -sv -a '!slow'


To measure the test coverage, do the following::

  $ ./bin/nosetests -sv --with-coverage --cover-package=beat.core


Our documentation is also interspersed with test units. You can run them using
sphinx::

    $ ./bin/sphinx -b doctest doc sphinx

Other Bits
==========

Profiling
---------

In order to profile the test code, try the following::

  $ ./bin/python -mcProfile -oprof.data ./bin/nosetests -sv ...

This will dump the profiling data at ``prof.data``. You can dump its contents
in different ways using another command::

  $ ./bin/python -mpstats prof.data

This will allow you to dump and print the profiling statistics as you may find
fit.


.. include:: links.rst
