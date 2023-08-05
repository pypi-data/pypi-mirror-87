
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


.. _beat-core-backend-api:

============
Backend API
============

As it is currently setup, user code at toolchain blocks running on the platform
consumes data stored on disk and produces data which is stored on disk so that
subsequent code running on the following blocks can operate on the same
principles. This approach allows users to potentially configure experiments
with a hybrid set of algorithms that execute on different backends. Each
backend can be implemented in a different programming language and contain any
number of (pre-installed) libraries users can call on their algorithms.

The requirements for BEAT when reading/writing data are:

  * Ability to manage large and complex data
  * Portability to allow the use of heterogeneous environments

Based on our experience and on these requirements, we investigated
the use of HDF5. Unfortunately, HDF5 is not convenient to handle
structures such as arrays of variable-size elements, for instance,
array of strings.
Therefore, we decided to rely on our own binary format.


This document describes the binary formats in BEAT and the API required by BEAT to handle multiple backend implementations. The
package `beat.env.python27`_ provides the *reference* Python backend
implementation based on `Python 2.7`_.


Binary Format
-------------

Our binary format does *not* contains information about the format of the data
itself, and it is hence necessary to know this format a priori. This means that
the format cannot be inferred from the content of a file.

We rely on the following fundamental C-style formats:

  * int8
  * int16
  * int32
  * int64
  * uint8
  * uint16
  * uint32
  * uint64
  * float32
  * float64
  * complex64 (first real value, and then imaginary value)
  * complex128 (first real value, and then imaginary value)
  * bool (written as a byte)
  * string

An element of such a basic format is written in the C-style way, using
little-endian byte ordering.

Besides, dataformats always consist of arrays or dictionary of such fundamental
formats or compound formats.

An array of elements is saved as followed. First, the shape of the array is
saved using an *uint64* value for each dimension. Next, the elements of the
arrays are saved in C-style order.

A dictionary of elements is saved as followed. First, the key are ordered
according to the lexicographic ordering. Then, the values associated to each of
these keys are saved following this ordering.

The platform is data-driven and always processes chunks of data.  Therefore,
data are always written by chunks, each chunk being preceded by a text-formated
header indicated the start- and end- indices followed by the size (in bytes) of
the chunck.

Considering the Python backend of the platform, this binary format has been
successfully implemented using the ``struct``  module.


Filesystem Organization
-----------------------

At the filesystem level, each backend shall be organized so it is fully
contained in a single-rooted directory tree. The backend installer should not
make assumptions about the directory structure of the target operating systems,
except, possibly, for the use of stock files. For example:

.. code-block:: sh

   $ ls /path/to/beat.env.python27
   -rw-r--r-- 1 beat beat  2829 Jul 20 19:57 LICENSE
   -rw-r--r-- 1 beat beat  7268 Jul 20 19:57 Makefile
   -rw-r--r-- 1 beat beat  1852 Jul 20 19:57 README.md
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 bin/
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 usr/
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 src/
   ...

There is a minimal set of required files in each environment:

1. ``Makefile``: A make file or equivalent script should be present to
   **fully** build the environment from scratch. This allows BEAT platform
   administrators to install the environment on a target machine.

2. ``bin/describe``: This is an executable that takes no arguments and
   describes the current environment, providing its name, version and a list of
   pre-installed libraries, toolboxes or any other information that may be
   relevant to users implementing algorithms for this backend. The output of
   the ``describe`` command should be a parseable JSON string. For example, our
   reference `beat.env.python27`_ environment returns the following for a call
   to ``bin/describe``:

   .. code-block:: json

      {
        "name": "Scientific Python 2.7",
        "version": "0.0.4",
        "os": [
          "Linux",
          "extatix03",
          "3.12.14-1-idiap-generic",
          "#20140313 SMP Thu Mar 13 15:12:40 CET 2014",
          "x86_64",
          ""
        ],
        "packages": {
          "beat.core": "0.9.4",
          "bob": "1.2.2",
          "matplotlib": "1.4.3",
          "numpy": "1.9.2",
          "oset": "0.1.3"
        }
      }

   Each pair of ``name`` and ``version`` for an environment must be unique so
   that platform users can uniquely select them.

3. ``bin/execute``: This is an executable that is called by the BEAT
   infrastructure to execute user code. The executable must be able to receive
   2 arguments that correspond to a I/O server address and  (temporary)
   directory containing the following files:

   .. code-block:: sh

      $ ls -1 /tmp/beat.A976xy1/
      configuration.json  #the configuration for the algorithm in JSON format
      prefix              #the prefix with algorithm/libraries/formats required

   Optional flags may be provided for administrative purposes, but will not be
   using for running user code. For example, the reference implementation of
   ``bin/execute`` responds this way when passed the ``-h`` optional flag:

   .. code-block:: sh

      $ /path/to/beat.env.python27/bin/execute -h
      Executes a single algorithm.

      usage:
        execute [--debug] <addr> <dir>
        execute (--help)


      arguments:
        <addr>  Address of the server for I/O requests
        <dir>   Directory containing all configuration required to run the user
                algorithm


      options:
        -h, --help   Shows this help message and exit
        -d, --debug  Runs executor in debugging mode


   You should **strongly** consider implemeting similar functionality on your
   backend to ease debugging in case of problems.


Further to those files, it is prudent to include:

1. ``README.rst``: a file containing installation and management instructions.
   It should preferrably be written using a markup language such as MarkDown
   (``.md`` extension) or reStructuredText (``.rst`` extension). By reading
   this file, it should be possible for a remote party with a working knowledge
   of the target operating system, to completely install the environment
   without external help.

   The README should also include contact points and, if possible, a
   bug-tracking link where users can submit bug/update requests.

2. ``LICENSE``: a file that describes the usage license for the backend.


Message Passing
---------------

The BEAT infrastructure communicates with the ``bin/execute`` process via `Zero
Message Queue`_ or ZMQ for short. ZMQ_ provides a portable bidirectional
communication layer between the BEAT infrastructure and the target backend,
with many `language bindings`_, including `python bindings`_.

The user process, which manages the data readout of a given algorithm, sends
commands back to the infrastructure for requesting data when needed.

.. code-block:: text

   "command"
   "argument1"
   "..."
   "argumentn"

Where ``command`` is the command name to be executed and ``argument*`` are the
corresponding arguments, sent using separate ``zmq.send()`` calls using the
multipart sending technique (as with ``zmq.SNDMORE``). In order to simplify
representation, we denote multi-message commands in a single line. So, the
command above will be represented in this document such as:

.. code-block:: text

   "command" "argument1" "..." "argumentn"

Commands may also exchange binary data. In such a case, we represent it in this
manual using ``<binary>``. The binary data format is the one defined by our
``BaseFormat`` class at the package ``beat.backend.python``.

The next diagram represents some possible states between the BEAT
infrastructure and the ``execute`` process in case of a successful execution:


.. _beat-core-backend-msc:
.. figure:: ./img/execute.*

   Message Sequence Chart between BEAT agents and user containers/algorithms


In the remainder of this section, we describe the various commands, which are
supported by this communication protocol.


Command: information (ifo)
~~~~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure to return information about the remote
data sources queried. The format of this command is:

.. code-block:: text

   "ifo name\n"

The infrastructure will answer by writing the following into the input pipe.

.. code-block:: text

   "X"
   "Start0"
   "End0"
   ...
   "StartX-1"
   "EndX-1"

where `X` is the length of the data source and the `StartX` and `EndX` are the
start and end indexes available through that data source.


Command: get data (get)
~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure to return the data at the given index.
The format of this command is:

.. code-block:: text

   "get X"

where X is the index of the data in the data source.

The infrastructure will answer by writing the following into the input pipe.

.. code-block:: text

   "StartX"
   "EndX"
   "data"

where `StartX` and `EndX` and the start and end indexes in the data sources and
`data` is the packed data that the data sources provides.


Command: done (don)
~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command notifies the infrastructure that the execution of the user process
has completed (i.e. it will not read or write any further data).

.. code-block:: text

   "done float"

Where ``float`` is a valid floating point number that represents the time
wasted waiting for I/O on the user process. This number composes the statistics
for processes.

Once the UP has sent this command, the infrastructure will retrieve the
statistics (I/O, CPU and memory) and it will acknowlegde the UP, once this is
done with:

.. code-block:: text

   "ack"

At this point, the UP is expected to gracefully terminate.


Command: error (err)
~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command notifies the infrastructure that the execution of the user process
has err and will not request any further data. A message explaining the error
condition is attached.

.. code-block:: text

   "err type message"

Once the UP has sent this command, the infrastructure will retrieve the
statistics (I/O, CPU and memory) and it will acknowlegde the UP, once this is
done with:

.. code-block:: text

   "ack"

At this point, the UP is expected to gracefully terminate. The value for
``type`` maybe set to ``usr``, indicating the error occurred inside the user
code or anything else, indicating it was a system error (and must be reported
to system administrators). In this case, the user only gets a generic message
indicating a problem with the infrastructure was detected and that system
administrators were informed.


.. include:: links.rst
