.. _api:

API
===

Exceptions
----------

.. autoexception:: pyrpkg.errors.rpkgError
.. autoexception:: pyrpkg.errors.rpkgAuthError
.. autoexception:: pyrpkg.errors.UnknownTargetError
.. autoexception:: pyrpkg.errors.HashtypeMixingError
.. autoexception:: pyrpkg.errors.MalformedLineError
.. autoexception:: pyrpkg.errors.InvalidHashType
.. autoexception:: pyrpkg.errors.DownloadError
.. autoexception:: pyrpkg.errors.UploadError


cli
---

.. autoclass:: pyrpkg.cli.cliClient
   :members:
   :undoc-members:
   :private-members:


commands
--------

.. autoclass:: pyrpkg.__init__.NullHandler
   :members:
   :undoc-members:

.. autoclass:: pyrpkg.__init__.Commands
   :members:
   :undoc-members:
   :private-members:


Lookaside
---------

.. autoclass:: pyrpkg.lookaside.CGILookasideCache
   :members:
   :undoc-members:


Sources
-------

.. autoclass:: pyrpkg.sources.SourcesFile
   :members:
   :undoc-members:

.. autoclass:: pyrpkg.sources.SourceFileEntry
   :members:
   :undoc-members:

.. autoclass:: pyrpkg.sources.BSDSourceFileEntry
   :members:
   :undoc-members:


gitignore
---------

.. autoclass:: pyrpkg.gitignore.GitIgnore
   :members:
   :undoc-members:


Utilities
---------

.. autoclass:: pyrpkg.utils.cached_property
   :members:
   :undoc-members:

.. autofunction:: pyrpkg.utils.warn_deprecated
.. autofunction:: pyrpkg.utils._log_value
.. autofunction:: pyrpkg.utils.log_result