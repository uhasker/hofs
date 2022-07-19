Basics
======

Hofs provides a useful functional interface for filesystem interactions.

Basic concepts
--------------

There are currently four classes for representing "file-like objects" - ``FileLike``, ``Dir``, ``File`` and ``TextFile``.

A ``FileLike`` object is anything that has the ``path`` and the ``name`` properties.
The ``path`` property is the *maximally expanded* path of the ``FileLike`` objects.
This means that ``path`` is absolute and all environment variables, special characters (like tilde) are expanded.
The ``name`` property is the name of the ``FileLike`` object (e.g. the file name).

Both ``Dir`` and ``File`` are ``FileLike`` objects (i.e. ``Dir`` and ``File`` inherit from ``FileLike``).
An object of type ``Dir`` represents a directory, while an object of type ``File`` represents a regular file.
These objects implement additional methods which are useful for when dealing with files or directories.
Text files are represented by ``TextFile`` (which inherits from ``File``).
Objects of this type have additional methods useful for dealing with text files specifically (such as ``word_count``).

Iterators
---------

The ``hofs`` library provides iterators of file-like objects.
The ``FileIterator`` and ``TextFileIterator`` are iterators which iterate over files & implement various useful functions.

The most common way to get a ``FileIterator`` is via the ``files`` property of a ``Dir`` object::

    import hofs as fs
    files = fs.Dir(".").files

You can then call various useful function on the ``FileIterator`` object::

    files.len()

See the documentation of ``FileIterator`` object for more.

You can get a ``TextFileIterator`` from a ``FileIterator`` by calling ``text_file_iterator`` on it::

    text_files = fs.Dir(".").text_file_iterator()

See the documentation of ``TextFileIterator`` object for more.
