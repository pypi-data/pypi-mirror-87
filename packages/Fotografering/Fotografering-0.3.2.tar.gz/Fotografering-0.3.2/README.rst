Fotografering
=============

Fotografering, linkify and beautify your photos with `Thumbr it`_ and `Dropbox`_.


In order to use it, you will need a Dropbox installation and a Thumbr.it account.

Installation
------------

::

    pip install fotografering


Usage
-----

First use: ::

    fotografering (master) » fotografering 27-06.jpg
    ==> No configuration file found.
    ==> Let's create it together!
    ==> You need to have Dropbox installed on this computer and Thumbit account
    Dropbox Path (/Users/toxinu/Dropbox): /Users/toxinu/Dropbox
    Dropbox Url (http://dl.dropbox.com/u/79447684): http://dl.dropbox.com/u/79447684
    Thumbit API Key: YOUR_KEY
    Thumbit Secret Key: YOUR_SECRET
    ==> Filter: barcelona
    ==> Frame: frame2
    Your image will be available in few seconds at: http://dl.dropbox.com/u/79447684/Images/27-06.jpg

A configuration file at ``$HOME/.fotografering.conf`` have been created.

You can choose your filter, frame you want and enable lightleak. Take a look at Thumbr it `demo`_.

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _Thumbr it: http://thumbr.it/
.. _Dropbox: https://www.dropbox.com/
.. _demo: http://thumbr.it/quick_start
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
