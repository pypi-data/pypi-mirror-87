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


.. _beat-core-introduction:

==============
 Introduction
==============

A typical BEAT experiment is composed of several building blocks. Datasets that provide data to the system, algorithms that handles the functions introduced by user, analyzers that is in charge of interpreting the output result and producing the appropriate results and figures, and toolchains that determines the data flow between the blocks from datasets to the final results. In addition, each block accepts specific data formats and the data is synchronized between blocks neatly without users need to interfere. These basic functionalities that are introduced in the "Getting Started with BEAT" section in `BEAT documentation`_ are all defined and managed by ``beat.core``. For example, as it is explained in the "Algorithms" section of "Getting Started with BEAT" in `BEAT documentation`_, algorithm objects should be derived from the class
``Algorithm`` when using Python or in case of C++, they should be derived from ``IAlgorithmLagacy``, ``IAlgorithmSequential``, or ``IAlgorithmAutonomous`` depending of the algorithm type. All these parent classes are defined in ``beat.core`` package.

The rest of this document includes information about the backend api used to handle data through the BEAT ecosystem. For developers and advanced user there is information for local development of the package.


.. include:: links.rst
