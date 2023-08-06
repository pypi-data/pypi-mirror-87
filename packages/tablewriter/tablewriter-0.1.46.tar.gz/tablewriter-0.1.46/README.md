---
permalink: /docs/index.html
---

**The complete documentation is available at https://cottephi.github.io/tablewriter/**

# TableWriter

## Instalation

`pip install tablewriter`

## Description

Class used to produce a ready-to-compile .tex file containing a table from a pandas or dask DataFrame object.
Can also compile the .tex to produce a .pdf.

Handles using additional latex packages through the *packages* argument. The given DataFrame is copied so any
modification of the  said DataFrame after instensiation of the TableWriter object has no effect on the
TableWriter object, and vice-versa.
You should not however modify the DataFrame contained in the TableWriter object, you should just create the
TableWriter once you are sure that your DataFrame is ready.

TableWriter uses pandas.DataFrame.to_latex and adds some more options to produce the .tex and the .pdf. Any
option that must be given to the to_latex method can be given to TableWriter through the *to_latex_args*
argument.

Note that the content of the DataFrame will be converted to string. If the DataFrame contains one the following
characters ("$", "_", "^", "%", "&"), a '\' is put before them.
Mathmode using '$' is handled.

## Usage

```python
from tablewriter import TableWriter
import pandas as pd
df = pd.DataFrame(columns=["$x$", "$x^2$"],
                  index=["$A_{00}$", "$A_{01}$"], data=[[2, 4], [3, 9]])
table = TableWriter(df, path="ouput")
table.compile()
```

TableWriter will use os.system('pdflatex ...') to create the pdf, so you need a working installation of it.
In order not to flood the stdout with pdflatex ouput, which is quite verbose, it is silenced by default. If the
compilation fails TableWriter will return 'ValueError: Failed to compile pdf'. In that case, you can try to
recompile if using

```python
table.compile(silenced=False)
```

To have the full output and try to understand what went wrong.

By default, all files produced by LaTeX are deleted except the .tex and the .pdf. You can change this default
behavior :

```python
# To keep all files :
table.compile(clean=False)
# Or on the contrary, to remove also .tex :
table.compile(clean_tex=True)
```

You can also do a compilation that will reuse the .tex file if it already exists:

```python
table.compile(recreate=False)
```

Here is a more complete example of table generation :

```python
from tablewriter import TableWriter
import pandas as pd
df = pd.DataFrame(columns=["$x$", "$x^2$"], index=["$A_{00}$", "$A_{01}$"],  
                  data=[["2", "$2^2$"], ["3", "$3^2$"]])
table = TableWriter(
    path_output="tests/data/ouput",
    data=df,
    to_latex_args={"column_format": "lrr"},
    label="tab::example",
    caption="TableWriter example",
    hide_numbering=True,
)
table.compile()
```
