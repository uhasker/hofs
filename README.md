# hofs

Hofs (**H**igher-**o**rder **f**unctions for the **f**ile **s**ystem) provides a useful functional interface for filesystem interactions.

Here is how you could get the total number of lines of all txt files in the current directory:

```python
import hofs as fs

fs.Dir(".").files.filter_ext("txt").t().map_lc().sum()
```

The library is very flexible, allowing you to write both short and long forms for most properties:

```python
import hofs as fs

# Short form (for when you quickly need to prototype something)
fs.Dir(".").files.filter_ext("txt").t().map_lc().sum()

# Long form (for when you need to use the library in a codebase)
fs.Dir(".").files.filter_extension("txt").text_file_iterator().map_line_count().sum()
```

You can also pass your own functions to the higher-order functions:

```python
import hofs as fs

# Short form (for when you quickly need to prototype something)
fs.Dir(".").files.filter(lambda f: f.ext == "txt").map(lambda f: f.t().lc).sum()

# Long form (for when you need to use the library in a codebase)
fs.Dir(".").files.filter(lambda f: f.extension == "txt").map(lambda f: f.text_file().line_count).sum()
```

## Requirements

You need Python >= 3.9 for this library.

## Installation

You can install hofs using the pip package manager:

```shell
pip install hofs
```
