=========
copyright_tool
=========


.. image:: https://img.shields.io/pypi/v/copyright_tool.svg
        :target: https://pypi.python.org/pypi/copyright_tool


Use to automatically scan all tracked files in your git repository and add/update the
copyright.

Simply create files like `.copyright.hash.tpl` and `.copyright.slash.tpl` at the root of your folder that are commented
as dictated by the language:

.. code-block:: python

        ####################################
        Copyright {year} Pennatus
        ####################################


If you have a `.copyrigh.hash.tpl` then the tool will scan your tracked files and determine
all files that use a hash style comment `#`.  If you have a `.copyright.slash.tpl` then the
tool will scan your tracked files and determine all files that use a slash style comment `//`.

To exclude files, create a file called `.copyrightignore` at the root of your folder using
syntax similar to your `.gitignore` to specify files to exclude from the search process.

* Free software: MIT license


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
