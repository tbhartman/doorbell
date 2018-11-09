Introduction
==============

*You have a visitor.*

|project_name| provides a `visitor pattern`_ implementation.  This implies two
basic classes, a :class:`~doorbell.Visitor` and a subject that is visited,
the :class:`~doorbell.Visitee`.

Implementations of :class:`~doorbell.Visitee` are mainly left to the user,
while |project_name| seeks to provide a number of :class:`~doorbell.Visitor`
classes for various purposes.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`

.. _visitor pattern: https://en.wikipedia.org/wiki/Design_Patterns#Behavioral
