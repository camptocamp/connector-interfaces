.. :changelog:

.. Template:

.. 0.0.1 (2016-05-09)
.. ++++++++++++++++++

.. **Features and Improvements**

.. **Bugfixes**

.. **Build**

.. **Documentation**

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**
* Computation of membership status instead of onchange
* Change button's links on confirmation window

**Bugfixes**
* Fix Invoice status open with workflow

**Build**

**Documentation**

9.0.3 (2016-08-11)
++++++++++++++++++

**Features and Improvements**
* Hide button upgrade account if already advanced member

**Bugfixes**

* Fix membership status visibility. Shows now value and not technical key
* Fix Proposals button visibility ('show all' & 'Add)

9.0.2 (2016-08-11)
++++++++++++++++++

**Bugfixes**

* Fix issue of description field on proposal detail view which was making the view failing.
* Fix issue of limit of 6 own proposals displayed in overview
* Fix portal user access right to proposal details to the address in it.
* Fix an issue of view of /my/account due to the move to /my/home of membership status
* Fix button "Show More" not hidden for matches overview when less than 4 matches are displayed

9.0.1 (2016-08-10)
++++++++++++++++++

**Features and Improvements**

* #14554 + #14555 Add project proposals and matches on backend and website
  * An overview of my proposals is visible in /my/home
  * A list of proposal matches is visible in /my/home
  * The full list of my proposals is accessible at /my/proposals
  * A list of all proposal is accessible at /proposals or at /market
  * A form to create a new proposal is accessible at /my/proposals/add
  * The same form is used to edit proposals
* Improvement of membership on website
  * Add a workflow to become associate
* Member portal profile website form
* Add project expertise objects
* Fluxdock Theme

**Build**

* Setup project docker compose

**Documentation**

* Added Docker and Rancher documentation
* Added HISTORY.rst (this file) as Changelog
