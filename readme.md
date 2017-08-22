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

As an example, consider the following piece of code in file `hello.c`:

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

Better Control
--------------

It is possible to select a number of lines:

    ```{.c include="code.c" start="5" lines="6"}
    ```

After pandoc did its job, this gives us

    ``` {.c include="code.c" start="5" lines="6"}
    main()
    {
        /* print hello world */

        printf("Hello World");
    }
    ```

Besides number of lines, it is also possible to state the number of
"paragraphs", which is the number of white space delineated lines.

For `code.c`, this is a bit silly, but it works:

    ```{.c include="code.c" start="5" pars="2"}
    ```

Pandoc gives us

    ``` {.c include="code.c" start="5" pars="2"}
    main()
    {
        /* print hello world */

        printf("Hello World");
    }
    ```

Instead of starting with line number `start` it is possible to use a
[regular expression](https://docs.python.org/2/library/re.html):

    ```{.c include="code.c" match="include" pars="2"}
    ```

This results in

    ``` {.c include="code.c" match="include" pars="2"}
    #include<stdio.h>

    main()
    {
        /* print hello world */
    ```

Future plans
------------

-   Support to select pieces of indented code.

    This is already partially implementen but I am not satisfied yet.

-   Support for git refs.

    This makes it possible to refer to previous versions of files.

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
