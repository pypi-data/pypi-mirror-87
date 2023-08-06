
remote-fs
=========

A tool to manage mounting your remote filesystems using smbfs and ssfs.

Install
-------

``pip install remote-fs``

Usage
-----

.. code-block::

   Usage: remote-fs [OPTIONS] COMMAND [ARGS]...

   Options:
     --smbfs  mounts via mount_smbfs (darwin only)
     --sshfs  mounts via sshfs
     --help   Show this message and exit.

   Commands:
     ls
     mount
     unmount

ls
^^

Can list ``configs`` for saved configs and ``mounts`` for currently mounted configs.

.. code-block::

   Usage: remote-fs ls [OPTIONS] RESOURCE

   Options:
     --help  Show this message and exit.

mount
^^^^^

When ``--sshfs`` is set, the default value for the ``--option`` param is ``reconnect,ServerAliveInterval=15,ServerAliveCountMax=3``.

.. code-block::

   Usage: remote-fs mount [OPTIONS] MOUNT_POINT

   Options:
     --load
     --name TEXT
     --remote TEXT      full hostname string, e.g. user@hostname:dir
     --hostname TEXT
     --user TEXT
     --dir TEXT
     -o, --option TEXT
     --help             Show this message and exit.

unmount
^^^^^^^

Runs ``umount`` using the mount point in the passed config.

.. code-block::

   Usage: remote-fs unmount [OPTIONS] NAME

   Options:
     --help  Show this message and exit.
