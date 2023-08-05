--------------

**keyup** \| Automated IAM Access Key Rotation for Amazon Web Services
======================================================================

--------------

About this repository
---------------------

-  Purpose: keyup automates IAM user access key rotation in Amazon Web
   Services' Accounts
-  Version: 1.2.7
-  Repo: https://bitbucket.org/blakeca00/keyup

--------------

Contents
--------

-  `Purpose <#markdown-header-purpose>`__
-  `Getting Started <#markdown-header-getting-started>`__
-  `Documentation <#markdown-header-documentation>`__
-  `Help <#markdown-header-help>`__
-  `Installation <#markdown-header-installation>`__
-  `Author & Copyright <#markdown-header-author-copyright>`__
-  `License <#markdown-header-license>`__
-  `Disclaimer <#markdown-header-disclaimer>`__

`back to the top <#markdown-header-about-this-repository>`__

--------------

Purpose
-------

**Keyup**:

-  | is a safe, error-free mechanism to rotate (renew) access keys to
     Amazon Web Services as
   | frequently as you wish, with minimal effort and risk.

-  enables you to change your access keys when required by executing a
   single command from the cli.

-  | Alternatively, enter a keyup command in your crontab with the
     ``--auto`` parameter and renew access
   | keys on a daily schedule.

-  **keyup** requires only the profile name of your IAM user in your
   local `awscli
   configuration <https://docs.aws.amazon.com/cli/latest/reference/>`__:

.. code:: bash


        $ keyup  --profile johndoe  --operation up

`back to the top <#markdown-header-about-this-repository>`__

--------------

Getting Started
---------------

Before starting, suggested to read the following:

-  `Frequently Asked Questions
   (FAQ) <http://keyup.readthedocs.io/en/latest/FAQ.html>`__
-  `Installation <http://keyup.readthedocs.io/en/latest/installation.html>`__
-  `Use Cases <http://keyup.readthedocs.io/en/latest/usecases.html>`__

**keyup** is licensed under `General Public License
v3 <http://keyup.readthedocs.io/en/latest/license.html>`__

`back to the top <#markdown-header-about-this-repository>`__

--------------

Documentation
-------------

**Online Documentation**:

-  Complete html documentation available at http://keyup.readthedocs.io.

**Download Documentation**:

-  `pdf
   format <https://readthedocs.org/projects/keyup/downloads/pdf/latest/>`__
-  `Amazon
   Kindle <https://readthedocs.org/projects/keyup/downloads/epub/latest/>`__
   (epub) format

`back to the top <#markdown-header-about-this-repository>`__

--------------

Help
----

Diplay help menu

.. code:: bash


        $ keyup --help

.. figure:: ./assets/help-menu.png
   :alt: help

   help

`back to the top <#markdown-header-about-this-repository>`__

--------------

Installation
------------

--------------

Installation via pip
~~~~~~~~~~~~~~~~~~~~

**Linux** \| Installation via pip:

.. code:: bash


        $ pip3 install keyup --user

**Windows** (Powershell) \| Installation via pip:

.. code:: bash


        $ pip3 install keyup

`back to the top <#markdown-header-about-this-repository>`__

--------------

Installation via Source Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Source** \| Installation via source code on local machine:

To see make targets, run:

.. code:: bash


        $ make help

.. figure:: ./assets/make-help.png
   :alt: make-help

   make-help

To install locally in a virtualenv:

.. code:: bash


        $ make source-install

`back to the top <#markdown-header-about-this-repository>`__

--------------

Verify Installation (windows & Linux):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash


        $ keyup --version

.. figure:: ./assets/keyup-version.png
   :alt: keyup-version

   keyup-version

`back to the top <#markdown-header-about-this-repository>`__

--------------

Author & Copyright
------------------

All works contained herein copyrighted via below author unless work is
explicitly noted by an alternate author.

-  Copyright Blake Huber, All Rights Reserved.

`back to the top <#markdown-header-about-this-repository>`__

--------------

License
-------

-  Software contained in this repo is licensed under the `GNU General
   Public License Agreement
   (GPL-3) <https://bitbucket.org/blakeca00/keyup/src/master/LICENSE.txt>`__.

`back to the top <#markdown-header-about-this-repository>`__

--------------

Disclaimer
----------

*Code is provided "as is". No liability is assumed by either the code's
originating author nor this repo's owner for their use at AWS or any
other facility. Furthermore, running function code at AWS may incur
monetary charges; in some cases, charges may be substantial. Charges are
the sole responsibility of the account holder executing code obtained
from this library.*

Additional terms may be found in the complete `license
agreement <https://bitbucket.org/blakeca00/keyup/src/master/LICENSE.txt>`__.

`back to the top <#markdown-header-about-this-repository>`__

--------------
