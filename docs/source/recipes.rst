Examples
========

You will need to import hofs first::

    import hofs as fs

Simple functions
----------------

Check whether a certain "file-like object", file or directory exists::

    fs.dir_exists(name)
    fs.file_exists(name)
    fs.file_like_exists(name)

Get the absolute path::

    fs.path_is_absolute(path)
    fs.path_is_relative(path)

Maximally expand paths::

    fs.expand_path(path)
    fs.expand_paths([path1, path2])

Example chains
--------------

Note that ``fs.Dir`` is recursive, i.e. it descends into all subdirectories.

Get the number of "file-like" objects (i.e. files & directories) in a directory::

    fs.Dir(dir).file_likes.len()

Get the number of files in a directory::

    fs.Dir(dir).files.len()

Get the number of directories in a directory::

    fs.Dir(dir).dirs.len()

Get the five biggest files in a directory::

    fs.Dir(dir).files.top_n(5)

Get the five biggest files in a directory together with their size::

    fs.Dir(dir).files.map(lambda f: (f, f.size)).top_n(5)

Get the five biggest files in a directory together with their size in MIB::

    fs.Dir(dir).files.map(lambda f: (f, f.size.size(fs.FileSizeUnit.MIB))).top_n(5)

Get the five biggest files excluding .git::

    fs.Dir(dir).files.exclude(".git").map(lambda f: (f, f.size)).top_n(5)
