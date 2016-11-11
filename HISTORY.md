.. :changelog:

<!--
Template:

## 9.0.1 (2016-05-09)

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**
-->

# Release History

## 9.0.10 (unreleased)

Added, but still in WIP: configuration for development with mailtrap

**Features and Improvements**

* Protect member detail if current user is not associated member RM#15405


**Bugfixes**

* Hide "Proposals" too in my home [RM#15915](https://redmine.iart.ch/issues/15915)
* Members slider appeareance (do not use "hidden") [RM#15336](https://redmine.iart.ch/issues/15336)
* Make sure you can drop content into <main /> element when page is new (addresses RM#15336)
* Fix subject for expertise proposal [RM#15668](https://redmine.iart.ch/issues/15668)
* Fix member detail padding [RM#16043](https://redmine.iart.ch/issues/16043)
* Remove logo placeholder if logo missing [RM#16042](https://redmine.iart.ch/issues/16042)


**Build**

**Documentation**


## 9.0.9 (2016-11-03)

Added, but still in WIP: configuration for development with mailtrap

**Features and Improvements**

* Adapt website to new registration process
* Access to backend only for right groups
* Replace confirmation email template
* Update translations
* Add subject to expertise proposal
* Modify email/login update process
* Adapt status messages colors
* /my/home: adjust column width
* Hide things & temporary styling
* Added lang German in songs
* added l10n_ch (for accounting) in base installation
* Added system parameters for website signup
* members aggregation

**Bugfixes**

* Hide menus that are not needed

**Build**

**Documentation**


## 9.0.8 (2016-09-26)

This release concerns `1b - Members II`. It is actually missing:

* Replace confirmation email template must override set_password email
* Update translations: all the translations where done TTW and where linked to old modules `website_fluxdock_signup` and `website_portal_profile` -> we must dump all of them and update references to specific_membership

**Features and Improvements**

* Add search field Industries, Expertises and Country in /members
* Merged `website_portal_profile` into `specific_membership`
* Merged `website_fluxdock_signup` into `specific_membership`
* Made account controller pluggable
* Port homepage to module
* Crop claim to 200 chars in members listing RM#15854
* Propose industry/expertise via email RM#15668
* Refactor signup (confirmation was completely broken)
* Update login if email is validated and publish partner RM#15638
* Publish partner only after 1st editing of profile RM#13670
* Change password button RM#15191
* Show status message when profile is updated (related to RM#15638)
* Show warning status message when login is updated
* Don't remove everything if there are wrong entries or missing mandatory fields RM##15644

**Bugfixes**

* Revert column enlargement on /my/home
* Change display of /my/home
* Fix an error on member details on field website
* Add subject to mailto link
* Change text for signup

**Build**

* Now it is hosted on Camptocamp's docker hub

**Documentation**


## 9.0.7 (2016-09-28)

**Features and Improvements**

* Display parent of industries and change order of industries ordered by parent / name in dropdown list
* Add a cancel button to cancel edition in /my/account

* Enlarge column of member profile in /my/home
* Center button "Edit profile" on /my/home

**Bugfixes**

* Fix placeholder in /my/account for url with http:/// instead of http://
* Set zip field as mandatory in /my/account
* Fix emptied fields in /my/account on error
* Allow to remove industries and expertises on /my/account
* Allow to remove industries and expertises on my proposal details
* Show existing image on profile
* Remove agreement and country from reset password page
* Change /my/home icon to a 300x200 px icon


## 9.0.6 (2016-09-14)

**Features and Improvements**

* Add tests to specific_membership
* Add 403 on edit proposals if you're not the owner
* Proposal publish button redirects to /my/home
* Add errore message in addition to highlight when a required field is not filled
* Add button to go back to home in proposal edit form
* Add demo data for proposals
* Define minimal style for pager

**Bugfixes**

* Fix search with special characters transformed in url with % characters that led to a server error
* Fix value disapearing when reloading form of proposal edition when an error is raised the following
  fields value were lost: country, teaser, description, industry and expertise
* Probosal publish button now validate fields and save them
* Fix unpublished proposal shown in matches overview
* Separate enterprise and industry tags by commas in /members, /members/<company> and on profile in /my/home
* Display pager on member list and set limit to 10


## 9.0.5 (2016-09-01)

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


## 9.0.4 (2016-08-18)

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

## 9.0.3 (2016-08-11)

**Features and Improvements**

* Hide button upgrade account if already advanced member

**Bugfixes**

* Fix membership status visibility. Shows now value and not technical key
* Fix Proposals button visibility ('show all' & 'Add)

9.0.2 (2016-08-11)
------------------

**Bugfixes**

* Fix issue of description field on proposal detail view which was making the view failing.
* Fix issue of limit of 6 own proposals displayed in overview
* Fix portal user access right to proposal details to the address in it.
* Fix an issue of view of /my/account due to the move to /my/home of membership status
* Fix button "Show More" not hidden for matches overview when less than 4 matches are displayed

## 9.0.1 (2016-08-10)

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
