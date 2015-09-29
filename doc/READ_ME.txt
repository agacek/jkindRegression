How this documenation was made...

Used the Sphinx doc tool, retrieved from PIP by navigating to the Python
installation's Script folder and running:
easy_install -U Sphinx

Manually created the "/doc" folder within the project as the destination for the 
configuration and documentation files.

Back in the Python's Script folder ran:
sphinx-quickstart
This creates the files to build the documentation. Of interest are the conf.py
and the index.rst.

Can manually add modules, classes and functions to search for but instead used
Sphinx's auto api tool to create the *.rst files.

From the Python's Script folder ran the sphinx-apidoc tool.
Use sphinx-apidoc -h for the arguments.
Typical usage:
sphinx-apidoc [options] -o <output_path> <module_path> [exclude_path, ...]

I ran:
sphinx-apidoc -l -P -f -e -o c:/temp/out c:/temp/jkindRegression/jktest

This gave documentation for the jktest package. Copied the generated *.rst 
files from c:/temp/out to c:/temp/jkindRegression/doc and then updated the
original index.rst to point to all the new *.rst files.

Then from the c:/temp/jkindRegression/doc folder ran:
make html

Then go find ./jkindRegression/doc/_build/html/index.html
