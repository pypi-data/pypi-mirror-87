===============================
ckill - Cleanly kills a process
===============================

Utility that allows to safely and cleanly terminate a multiprocess application
that implements a shutdown, clean-up, or exit routine when a SIGTERM is
received.

ckill sends a SIGTERM signal to the main process, waits for it to die, and if
it doesn't after some timeout, SIGKILL all its subprocesses in the process tree
from higher (recent) to lower (former) PID value.

In this way, ckill allows the process to terminate correctly, but if it
malfunctions when terminating, or if it takes too much time (determined by the
user) all its subprocesses are killed and then the main process itself, leaving
no zombie processes behind.

.. image:: http://turnoff.us/image/en/dont-sigkill-2.png
   :scale: 50%
   :alt: DON'T SIGKILL 2
   :target: http://turnoff.us/geek/dont-sigkill-2/


If you're developing a Python multiprocess application, see also
https://github.com/kuralabs/multiexit


Install
=======

.. code-block:: sh

    pip3 install ckill

Optionally, install the following package to enable color log output.

.. code-block:: sh

    pip3 install colorlog


Usage
=====

.. code-block:: text

    usage: ckill [-h] [-v] [--version] [--no-color] [--timeout-s TIMEOUT_S] PID

    Cleanly kills a process

    positional arguments:
      PID                   PID of process to kill

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase verbosity level
      --version             show program's version number and exit
      --no-color            Do not colorize the log output
      --timeout-s TIMEOUT_S
                            Maximum time to wait for the process to die, in seconds.


Repository
==========

    https://github.com/kuralabs/ckill


Changelog
=========

1.0.1 (2020-12-01)
------------------

Fix
~~~

- Fix bad psutil API call.


1.0.0 (2020-10-15)
------------------

New
~~~

- Initial release.


License
=======

.. code-block:: text

   Copyright (C) 2020 KuraLabs S.R.L

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
