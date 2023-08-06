zippyshare_generator
=======================

Generator Links


Installing
-------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install zippyshare

zippyshare supports Python 2 and newer.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple generate link:

.. code-block:: batch

    $ zippyshare.py -d /root/Downloads "https://www110.zippyshare.com/v/0CtTucxG/file.html" -n "myMovies.mp4"


And it will download automaticaly with "Internet Download Manager (IDM) for Windows or build in download manager

You can use on python interpreter

.. code-block:: python

    >>> from zippyshare import zippyshare
	>>> generator = zippyshare()
    >>> url_download = generator.generate("https://www110.zippyshare.com/v/0CtTucxG/file.html")
	>>> generator.download(url_download, ".", "myMovies.mp4", False)
    >>> #it will download it automatically

For more options use '-h' or '--help'

.. code-block:: python

    $ zippyshare.py --help

    or

    $ zippyshare --help


Support
---------

*   Download With 'wget' (linux/windows) or 'Internet Download Manager (IDM) (Windows) (pip install idm)'
*   Python 2.7 + (only)
*   Windows, Linux


Links
-------	

*   License: `BSD <https://bitbucket.org/licface/zippyshare/src/default/LICENSE.rst>`_
*   Code: https://bitbucket.org/licface/zippyshare
*   Issue tracker: https://bitbucket.org/licface/zippyshare/issues