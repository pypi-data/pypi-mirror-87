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


.. _zmq_architecture:

==================================
ZMQ Architecture for task handling
==================================

Introduction
------------

The ZMQ architecture implemented in beat.core is based on the `Majordomo
Protocol`_ as described in the `ZeroMQ book`_.

There are however some subtle differences:

- We have one client: the scheduler
- We have unique workers
- We currently don't have "system commands"

Due to these differences and their implementation, the protocol has been
renamed: "BEAT Computation Protocol" or BCP for short.

The system is based on these three components:

- The client
- The broker
- The worker(s)

In BEAT, the client will be the scheduler which will send the tasks to the
broker which will be responsible for forwarding them to the appropriate worker
requested by the scheduler.

Once the task has been completed, the worker will send back a message to the
scheduler through the broker.

The whole messaging system is asynchronous except when starting an actual task.
The worker will send back a confirmation as soon as the runner was properly
started.

Why this design ?
-----------------

The original design was a bit simpler:

- One scheduler
- Many workers

The scheduler was responsible for both task scheduling and worker communication
handling. One issue that arose from time to time was that with very low volume
of network activity, the connection between one or more workers and the
scheduler would get cut and nobody would notice. The result was that new tasks
would be sent but silently dropped and thus experiment would stay in a running
state while not doing anything. And if canceled, the state would stay in
canceling as again the command would be silently dropped.

Thus the rational behind choosing this new design was to avoid these connection
loss and therefore platform paralysis.

Now, the broker and the workers implement a bidirectional heartbeat. This has a
twofold benefit:

- The heartbeat itself should generate enough network activity to avoid the
  connection to be cut.
- If a worker goes missing, it will be detected by the broker that will act as
  configured to.

BCP Schema
----------

The figure below shows how the system is working.

::

                                 --------------
                                 |            |
                                 |   client   |
                                 |            |
                                 --------------
                                       |
                                 --------------
                                 |            |
                                 |   broker   |
                                 |            |
                                 --------------
                                   |  |  |  |
                                   |  |  |  |
           /----------------------/   |  |  \-----------------------\
           |                          |  |                          |
           |                  /-------/  \-------\                  |
           |                  |                  |                  |
    ---------------    ---------------    ---------------    ---------------
    |             |    |             |    |             |    |             |
    |   worker1   |    |   worker2   |    |   worker3   |    |   worker4   |
    |             |    |             |    |             |    |             |
    ---------------    ---------------    ---------------    ---------------

.. include:: links.rst
