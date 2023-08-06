==========
Lib module
==========

Tools for the other modules.

.. warning::
    These tools have been designed primarily for internal use throughout the
    library and often work only in very specific situations (e.g.
    :func:`~nngt.lib.find_idx_nearest` works only on sorted arrays), so make
    sure you read their doc carefully before using them.


Content
=======

.. autosummary::

    nngt.lib.InvalidArgument
    :members:
    nngt.lib.delta_distrib
    nngt.lib.find_idx_nearest
    nngt.lib.gaussian_distrib
    nngt.lib.is_integer
    nngt.lib.is_iterable
    nngt.lib.lin_correlated_distrib
    nngt.lib.log_correlated_distrib
    nngt.lib.lognormal_distrib
    nngt.lib.nonstring_container
    nngt.lib.uniform_distrib


Details
=======

.. module:: nngt.lib


.. autoclass:: InvalidArgument

.. autofunction:: delta_distrib

.. autofunction:: find_idx_nearest

.. autofunction:: gaussian_distrib

.. autofunction:: is_integer

.. autofunction:: is_iterable

.. autofunction:: lin_correlated_distrib

.. autofunction:: log_correlated_distrib

.. autofunction:: lognormal_distrib

.. autofunction:: nonstring_container

.. autofunction:: uniform_distrib

