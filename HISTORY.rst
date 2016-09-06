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
* Add tests to specific_membership
* Add 403 on edit proposals if you're not the owner
* Proposal publish button redirects to /my/home
* Add errore message in addition to highlight when a required field is not filled

**Bugfixes**

* Fix search with special characters transformed in url with % characters that led to a server error
* Fix value disapearing when reloading form of proposal edition when an error is raised the following
  fields value were lost: country, teaser, description, industry and expertise
* Probosal publish button now validate fields and save them
* Fix unpublished proposal shown in matches overview

**Build**

**Documentation**


9.0.5 (2016-09-01)
++++++++++++++++++

**Features and Improvements**

* Add membership end date on account view
* Project proposal change order date to create_date
* Proposal details access rights:
  * Adds buttons to sign up, login or subscribe to become an associate
  * Hide fields for non associate members

**Bugfixes**

* Fix search by country on proposal list
* Fix search by expertise and industry on proposal list for visitors
* Fix previous, next buttons on proposals matches stick to proposal matches
* Fix installation of demo data

**Build**

* Activation of oerpscenario


9.0.4 (2016-08-18)
++++++++++++++++++

**Features and Improvements**

* Computation of membership status instead of onchange
* Change button's links on confirmation window
* Proposal details:
    * Add country and location on proposal detail
    * Add button to return to list depending on the context
      * In all proposal, return to /market
      * In my proposal, return to /my/proposals
      * In matching proposal, return to /my
    * Implement Publish button
    * Implement Delete buttons adding a new page for confirmation
    * Add start and end dates with check on start < stop
    * Add previous and next buttons looping on elements on the previous list
* Refactor list of matches computation and add tests
* Make proposal titles in list clickable
* Add pager on list pages /market and /my/proposals
* Implemantation of search on proposals by name, expertise, industry, country and location.
* Multiple layout improvements

**Bugfixes**

* Fix Invoice status open with workflow
* Proposal details:
  * Fix display of company name
  * Fix location field which was not saved
  * Fix addition of industry in industries field which weren't saved
* Remove duplicate Industries on proposal list
* Give access to public on /market

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
