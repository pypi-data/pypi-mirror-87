===========================
 sphinxnotes-peopledomain
===========================

Sphinx domain for describing people.

If you use sphinx as blog, you can use this domain to manange your friends link.

Installation
============

::

    pip install sphinxnotes-peopledomain


Configuration
=============

Add ``'sphinxnotes.peopledomain'`` to the ``extensions`` list in ``conf.py``::

    extensions = [ 'sphinxnotes.peopledomain' ]


Usage
=====

For now, this package provides a domain named ``ppl``.

To create a description of your friend, use ``friend`` directive::

    .. ppl:friend:: SilverRainZ
       :homepage: https://silverrainz.me

       Human.

Then you can use role ``:ppl:friend:`SilverRainZ``` to refer him.
It will be rendered as "@SilverRainZ" with the appropriate link.

Changelog
=========

0.1
  Provide the "ppl" domain, "friend" directive and "friend" role.
0.2
  - Reanme the namespace from "sphinxcontrib" to "sphinxnotes"
  - Fix the import error of ``make_id``
