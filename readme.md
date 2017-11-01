Include Files in Markdown with Pandoc
=====================================

Rationale
---------

[Pandoc](http://pandoc.org/) is a universal document converter. It
allows me to use
[markdown](https://daringfireball.net/projects/markdown/syntax) as my
primary text format.

Pandoc's functionality can be extended by means of
[filters](http://pandoc.org/scripting.html). This repo contains a filter
that can be used to add chunks of source code into text files.

Example
-------

As an example, consider the following piece of code in file `code.c`:

``` {.c include="code.c"}
/* Hello World Program */

#include<stdio.h>

main()
{
    /* print hello world */

    printf("Hello World");
}
```

Additionaly, consider the following piece of a blog about this awesome
code (stored in `blog.txt`):

    Hello World
    ===========

    Today, we'll discuss the following piece of awesome code:

    ```{.c include="code.c"}
    ```

We can actually include this code in our text as follows

    $ pandoc blog.txt --filter ./include_file.py -o blog.txt

This changes `blog.txt` into

    Hello World
    ===========

    Today, we'll discuss the following piece of awesome code:

    ``` {.c include="code.c"}
    /* Hello World Program */

    #include<stdio.h>

    main()
    {
        /* print hello world */

        printf("Hello World");
    }
    ```

In case `code.c` changes and `pandoc` runs again, updated code will be
included.

Include part of a file
----------------------

It is possible to select a part of the file by means of `start` and
`stop`. These represent line numbers:

    ``` {.c include="code.c" start="5" stop="11"}
    ```

It is also possible to select a number of lines:

    ``` {.c include="code.c" start="5" lines="6"}
    ```

After pandoc did its job, this gives us

    ``` {.c include="code.c" start="5" lines="6"}
    main()
    {
        /* print hello world */

        printf("Hello World");
    }
    ```

> The options `pars` (for number of paragraphs) and `match` (for pattern
> matching) are included in the source. These are, however, deprecated
> features. These options were intended to deal with code that might
> change in future. However, the `git` option is a much better way to
> guarantee that the intended code is included.

Dedent code
-----------

In case the selected code shares a common amount of indentation (for
example a function body without the enclosing braces), it is possible to
remove the indetation with the `dedent` option:

    ``` {.c include="code.c" start="7" stop="9" dedent="y"}
    ```

The resulting code is left aligned.

Including checked-in Code
-------------------------

One can use the `git` option to define the git version of the code to
include:

    ```{.c include="code.c" git="a23ed32"}
    ```

[GitPython](http://gitpython.readthedocs.io/en/stable/index.html) is
used to obtain the requester version from the git repository.

Temporarily Remove Code
-----------------------

Filter `clear_code.py` removes the code from the input file. Code is
only removed in case "include" is given and its value is the name of a
file.

    $ pandoc blog.txt --filter ./clear_code.py -o blog.txt

Later on, code can be added again with `include_file.py`.

Install
-------

Assuming you have [pandoc](http://pandoc.org/) and [python
2](https://www.python.org/) installed, I suggest you the following
options:

-   Copy `include_file.py` to the directory where your markdown
    files are. Make `include_file.py` executable.

-   Copy `include_file.py` to, for example, `~/bin`.

    Also in this case, you have to make the file executable.

Additionally the Python code makes use of
[`pandocfilters`](http://pandoc.org/scripting.html#but-i-dont-want-to-learn-haskell)
which can be installed as `pip install pandocfilters`.

Furthermore
[GitPython](http://gitpython.readthedocs.io/en/stable/index.html) is
used to support the `git` tag.
