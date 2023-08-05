========
pwclient
========

.. _pwclient_1.3.0:

1.3.0
=====

.. _pwclient_1.3.0_New Features:

New Features
------------

.. releasenotes/notes/check-get-4f010b2c4fdcd55c.yaml @ b'feea0eff925a124869c798d283cd400946db3ce8'

- Add a new ``pwclient check-get`` command to query the checks run against
  a specific patch.


.. _pwclient_1.2.0:

1.2.0
=====

.. _pwclient_1.2.0_New Features:

New Features
------------

.. releasenotes/notes/git-am--m-flag-190f3a7e17cec6f4.yaml @ b'1a021954aa5d8a6fa84d1683395bec59a4bac974'

- The ``pwclient git-am`` command can now passthrough the ``-m`` flag to
  ``-m``.


.. _pwclient_1.1.1:

1.1.1
=====

.. _pwclient_1.1.1_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/drop-pypy-support-17f1f95b9394b257.yaml @ b'c48755ad5ed20415ba8974e41c0d6c140ce84687'

- PyPy is no longer officially supported.


.. _pwclient_1.1.0:

1.1.0
=====

.. _pwclient_1.1.0_New Features:

New Features
------------

.. releasenotes/notes/add-long-opts-4611e7cce3993f08.yaml @ b'f45667782281fbf63b5ef0d20052c2b42bf48664'

- Most options now have a long opt equivalent. For example:
  
     $ pwclient update --archived yes 123


.. _pwclient_1.1.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/issue-1-c7e4c3e4e57c1c22.yaml @ b'e6eb261584382373bb08ee7ee95753ba97b27b59'

- The ``pwclient view`` command will now decode received mboxes on Python
  2.7.


.. _pwclient_1.0.0:

1.0.0
=====

.. _pwclient_1.0.0_Prelude:

Prelude
-------

.. releasenotes/notes/initial-release-eb74a7ae0ce3b1fb.yaml @ b'23fd64ad3a266189974ac7625cc03415c30e474d'

Initial release of *pwclient* package.

