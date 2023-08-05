
[//]: # (start:toc)
Table of Contents
=================
- [renderme](#renderme)
- [Usage](#usage)
    - [Examples:](#examples)

[//]: # (end)

# renderme

Render markdown templates.

# Usage
[//]: # (start:shell`python -m rendermd.command_line --help`)
```
usage: rendermd [-h] [-p PATTERNS] [--no-recursive]

Render markdown templates. This command recursively search the current
directly and find all markdown files by matching given patterns (default to
"**/README.md").

optional arguments:
  -h, --help            show this help message and exit
  -p PATTERNS, --pattern PATTERNS
                        Comma separated list of markdown files to populate
  --no-recursive        Do not search for files recursively
```

[//]: # (end)



## Examples:

- `[//]: # (start:toc)` and `[//]: # (end)` will produce table of contents.
- `[//]: # (start:shell`echo abc`)` and `[//] # (end)` will produce `abc` (the output of the shell command `echo abc`.
- More examples can be found in [test_toc_generator.py](./tests/test_toc_generator.py) and [test_shell_generator.py](./tests/test_shell_generator.py)
