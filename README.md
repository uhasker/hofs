# hofs

Hofs (**H**igher-**o**rder **f**unctions for the **f**ile **s**ystem) provides a useful functional interface for filesystem interactions.

This library is usable, but the API is currently not stable, a lot of features are still missing etc.

In summary - try it out, but don't use it for anything in production.

## Code examples

Let's say you need to get the total number of lines of all txt files in the current directory excluding the `.git` directory.
The `hofs` library allows you to write a simple function chain that accomplishes this is one line:

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

The `hofs` library is very general.
If you need to perform an operation that is currently not present, simply call the respective higher-order functions with your own callables.
For example here is how we could perform our task by explicitly calling the respective higher-order functions:

```python
import hofs as fs

fs.Dir(".").files.filter(lambda f: f.extension == "txt").map(lambda f: f.text_file().line_count).sum()
```

## Requirements

You need Python >= 3.9 for this library.

## Installation

You can install hofs using the pip package manager:

```shell
pip install hofs
```

## Documentation

See the [documentation](uhasker.github.io/hofs) for further information.
