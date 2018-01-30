# Release History

Latest (Unreleased)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**


9.5.0 (2018-01-30)
++++++++++++++++++

**Features and Improvements**

* Install module `web_environment_ribbon`

**Bugfixes**

* Upgrade `mail_digest` to pull recent imp/fix BSFLU-52
* Lint fixes based on new checks on MQT

**Build**

* Sync from odoo-template
* Fix travis build w/ support for SNI to requests to avoid SSL  certificate mismatches.

  This fixes SSL errors when creating minions python requests lib 
  lacks support for NSI thus fall back on the wrong domain name 
  thus certifactes mismatches and minion were not created.

* Upgrade docker-compose to 1.17.1
* Remove unused PO file to reduce docker image size
* Update odoo-cloud-platform (BIZ-1093)

9.4 (2017-05-23)
++++++++++++++++

**Bugfixes**

* Fix some translations


9.4b3 (2017-05-23)
++++++++++++++++++

**Features and Improvements**

* Notification settings: hide required fields markers
* Notifications: hide item w/ unpublished refs
* Notifications: hide label and model name
* Invert colors for publish/unpublish buttons
* Change notification link color and fix listing of matches
* Force translation of startdate/enddate error msg
* Include site name in mail digest subject
* Homepage: hide only login buttons when logged in
* Update translation for reset pwd view


**Bugfixes**

* Run upgrade of emails (missing in previous release)
* Fix email message lang default with fallback
* /my/membership only `confirm` button is blue
* User menu dropdown: make sure german text not cut


**Build**

**Documentation**


9.4.0b2 (2017-05-19)
++++++++++++++++++

**Bugfixes**

* `cms_notifications` did not included static lib for font-awesome


9.4.0b1 (2017-05-19)
++++++++++++++++++++

**Features and Improvements**

* Better UX for notification settings RM#17108
* Update matches notification when partner updates profile RM#17059
* Trigger notification matche process for existing proposals RM#17059
* Mail digest use company email address as "from"
* Update partner logo image description RM#17099
* Update mail_digest: use company email from
* Trigger notification match process for existing proposals RM#17059
* Support email address with special characters in reset pwd link RM#17107
* Remove "profile will be published automatically" RM#17060
* Remove "change pwd" button from profile form RM#16094
* Reference: add missing fields in backend view RM#16749
* Reference image not mandatory, update placeholder image RM#16978
* Proposal: add missing fields to backend form RM#16748
* Move mgmt buttons above member detail image RM#17122
* Membership upgrade confirmation update design RM#17105
* Make all submit buttons blue RM#17110
* Improve my/home membership status messages RM#17103
* Hide login/signup snippet if user is logged in RM#17096
* Detail views: remove "add new" button RM#17114
* Be defensive when proposals gets unpublished RM#17172
* Add html help text to expertise in partner form RM#17099
* Adapt payment views RM#17104


**Bugfixes**

* Fix add validation for proposal form end date>start date RM#17058
* Fix no result bg color for select2 widget RM#17099
* Fix log for proposal match cron
* Fix links color in matches emails RM#17109

**Build**

* Use odoo project image 2.2.0

  * use redis-sentinel
  * add before/start entrypoints


**Documentation**


9.3.7 (2017-05-09)
++++++++++++++++++

**Build**

* Use odoo project image 2.1.1 to include security fix

  Odoo Security Advisory                   ODOO-SA-2017-05-05-1

  Title: Remote Code Execution via Ghostscript vulnerability

  Affects: Odoo servers with an (unpatched) Ghostscript installation
  Component: Core
  Credits: Nils Hamerlinck
  OVE ID: OVE-20170505-0003
  References:
    https://bugs.ghostscript.com/show_bug.cgi?id=697799
    https://security-tracker.debian.org/tracker/CVE-2017-8291
    https://www.ubuntu.com/usn/usn-3272-1/
    https://bugzilla.suse.com/show_bug.cgi?id=1036453


9.3.6 (2017-05-02)
++++++++++++++++++

**Bugfixes**

* Merge all upgrade steps between 9.2.3 and 9.3.6.

  From production perspective all the versions between 9.2.3 and 9.3.6
  are just transition versions and could be considered as alphas and betas.
  Here we merge all their upgrade steps into 9.3.6 so that we run one single upgrade
  but preservince the history in a way.


9.3.5 (2017-05-02)
++++++++++++++++++

**Bugfixes**

* [fix] send matches email using partner lang
* [fix] notification settings link in emails

  Make sure we redirect always to login + auto redirect to notificationi panel.


9.3.4 (2017-04-28)
++++++++++++++++++

**Bugfixes**

* [fix] brute force "Digest" translation
* [add] missing translations to personal menu
* Include transl fixes from `mail_digest` and `cms_notifications`
* update translations and email templates
* [fix] partner form: do not wipe address fields if no value


9.3.3 (2017-04-27)
++++++++++++++++++

**Bugfixes**

* [fix] enforce `user_id` on partner created via website

  When creating users via website the partner is not always associated to the user.
  We now enforce this on signup.


9.3.2 (2017-04-26)
++++++++++++++++++

**Bugfixes**

* [fix] apply notification defaults to user template too

    When creating user trough backend interface
    having defaults defined at field level is enough.
    But when creating users via website interface
    most of the defaults for involved fields
    are taken from the user template by `auth_signup` module.

* Fix a bug in `mail_digest` that prevented multiple digest email creation


9.3.1 (2017-04-21)
++++++++++++++++++

**Bugfixes**

* Fix missing upgrade song call for emails in migration.yml


9.3.0 (2017-04-21)
++++++++++++++++++

**Features and Improvements**

* [RM#16516](https://redmine.iart.ch/issues/16516) [add] matches notifications
* Includes new modules: mail_digest + cms_notifications
* [RM#16936](https://redmine.iart.ch/issues/16936) [add] defaults and translations for notifications
* [RM#16939](https://redmine.iart.ch/issues/16939) Profile and reference publish improvements RM#
* [RM#16939](https://redmine.iart.ch/issues/16939) restore `redirect after 1st reference puslished`
* [add] customize email template
* improve mail servers setup
* [add] /members menu item and update transl
* [RM#16738](https://redmine.iart.ch/issues/16738) [upd] do not publish member profile automatically
* update pending merges: cms_delete_content has been merged

**Bugfixes**

* [RM#16796](https://redmine.iart.ch/issues/16796) [fix] link spacing in labels
* [RM#16797](https://redmine.iart.ch/issues/16797) [fix] port login template from prod, update transl
* [RM#16797](https://redmine.iart.ch/issues/16797) [fix] redirect after sumbit/cancel in partner form
* [fix] regression in form image widget
* [fix] demo users import: do not send email
* disable footer_custom too
* [RM#16801](https://redmine.iart.ch/issues/16801) update template names
* [RM#16795](https://redmine.iart.ch/issues/16795) [fix] disable default automatic footer
* [RM#16892](https://redmine.iart.ch/issues/16892) adjust traslations
* [RM#16672](https://redmine.iart.ch/issues/16672) [fix] footer copy translation and spacing


## 9.2.4b5 (2017-03-16)

**Features and Improvements**

* [RM#16738](https://redmine.iart.ch/issues/16738) publish imp for partner
    + fix parter/user relations
* [RM#16412](https://redmine.iart.ch/issues/16412) references aggregation: random
  Includes partial refactoring of mosaic JS.
* [RM#16672](https://redmine.iart.ch/issues/16672) Same footer for email and website
* [RM#16401](https://redmine.iart.ch/issues/16401) [imp] force logout on email change
* [RM#16392](https://redmine.iart.ch/issues/16392) update pre-sorted countries order
* Update `cms_delete_content`: delete confirmation now happens in modal
* [upd] cyon.ch mailserver configuration


**Bugfixes**

* [fix] partner form: `zip` code is required


## 9.2.4b4 (2017-03-08 - INT)

**Features and Improvements**

* Use final version logo: no beta anymore


**Bugfixes**

* [fix] partner form: must publish on save
* [fix] typo: redirect to /members not /market if profile is not published


## 9.2.4b3 (2017-03-08 - INT)

**Bugfixes**

* [fix] user need sudo to edit its partner
* [fix] industry OR expertise in members search form too


**Features and Improvements**

* disable public profile link when not published


## 9.2.4b2 (2017-03-07 - INT)

**Features and Improvements**

* [RM#16671](https://redmine.iart.ch/issues/16671) update wording, translations, view names and typos
* [RM#16672](https://redmine.iart.ch/issues/16672) Email templates + footer: copyright 2017 / translation
* [RM#16100](https://redmine.iart.ch/issues/16100) [add] links to profile progress tooltips
* [RM#16410](https://redmine.iart.ch/issues/16410) Restrict teaser on 200 characters (use new textarea widget in cms_form)


## 9.2.4b1 (2017-03-06 - INT)

**Features and Improvements**

* Cleanup POT/PO files for all custom modules
* [RM#16610](https://redmine.iart.ch/issues/16610) Adapt invoice
* [RM#16525](https://redmine.iart.ch/issues/16525) Associate Membership - adapt product price, name and make it not updatable
* [RM#16623](https://redmine.iart.ch/issues/16623) filter industry / expertise: OR not AND condition
* [RM#16260](https://redmine.iart.ch/issues/16260) Update /my/account design (includes: migrate partner forms to cms_form)
* [RM#16622](https://redmine.iart.ch/issues/16622) info message on unpublish
* [RM#16392](https://redmine.iart.ch/issues/16392) countries pre-sorted
* [RM#16394](https://redmine.iart.ch/issues/16394) phone numbers, international code suggestions

## 9.2.3 (2017-02-14)

**Features and Improvements**

* [fix] [RM#16537](https://redmine.iart.ch/issues/16537) Server error on end date validation

  Add validation handling to cms_form + improved tests.


## 9.2.2 (2017-02-09)

**Features and Improvements**

* Compress HTML
* [add] use cms form search as base search form
* [imp] replace proposal/reference search form
* [add] "my" filter to search form + refactoring and cleanup of all "/my" stuff
* [add] form descriptions
* [add] [RM#16492](https://redmine.iart.ch/issues/16492) form help texts
* [imp] [RM#16287](https://redmine.iart.ch/issues/16287) cleanup custom template names
* [imp] get rid of old /my/* urls
* [upd] [RM#16416](https://redmine.iart.ch/issues/16416) box order in my home
* [add] [RM#16404](https://redmine.iart.ch/issues/16404) view profile button
* [RM#16517](https://redmine.iart.ch/issues/16517) proposal view remove company phone/email
* [RM#16522](https://redmine.iart.ch/issues/16522) proposal "website description" -> "description"
* [RM#16491](https://redmine.iart.ch/issues/16491) Port changes from prod
* [imp] [RM#16520](https://redmine.iart.ch/issues/16520) adapt progress bar status manually
* [add] demo users
* [add] redirect after 1st reference published
* [add] popover for publish button tooltip
* upgrade cms
* upgrade OCB
* update odoo version
* update backend menu entries
* force secure pwd on test (integration and prod already have it)


**Bugfixes**

* [fix] [RM#16512](https://redmine.iart.ch/issues/16512) members slider: show only published
* [fix] [RM#16511](https://redmine.iart.ch/issues/16511) proposal view: show details for owner
* [fix] [RM#16403](https://redmine.iart.ch/issues/16403) References in member profile not clickable
* [fix] [RM#16128](https://redmine.iart.ch/issues/16128) autocomplete for m2m fields
* [fix] [RM#16502](https://redmine.iart.ch/issues/16502) delete issue w/ attachment fields (breaking reference deletion)
* [fix] [RM#16399](https://redmine.iart.ch/issues/16399) change market icon
* [fix] [RM#16521](https://redmine.iart.ch/issues/16521) add some spaces
* [fix] proposal test and backend menu
* [fix] required field error color
* [fix] superadmin bypasses backend permission check
* [fix] proposal view for anon, adapt padding for cta links


## 9.2.1 (2017-01-24)

**Features and Improvements**

* Go cloud!

## 9.2.0 (2017-01-12)

**Features and Improvements**

* Use new module `cms_status_message` (remove custom implementation in theme_fluxdocs)'
* Use new module `cms_form` (replace reference form and proposal form)'
* Use new module `cms_delete_content` to drop custom delete/confirm controllers
* Publish "Market" features
* Cleanup and adjust views according to reference work
* Various miscellaneous Improvements:

    * [RM#16130](https://redmine.iart.ch/issues/16130) Text Membership Upgrade email confirm
    * [RM#16198](https://redmine.iart.ch/issues/16198) /proposals/add: miscellaneous
    * [RM#16199](https://redmine.iart.ch/issues/16199) /market, /members --> same layout, both responsive
    * [RM#16309](https://redmine.iart.ch/issues/16309) Update payment views
    * [add] member detail redirect to /my/membership if coming from there
    * [RM#16360](https://redmine.iart.ch/issues/16360) port views updates and transl from test
    * [add] owner address in proposal detail
    * [RM#16346](https://redmine.iart.ch/issues/16346) [imp] payment info details + translations
    * remove hide link from proposal listing
    * [RM#16363](https://redmine.iart.ch/issues/16363) drop custom listing no result for proposal
    * update template names to include "fluxdock"
    * [add] proposal translations
    * [add] customize invoice report
    * update payment views RM#16309
    * update emails + fix importer for translations
    * update membership actions RM#16310

**Bugfixes**

* Fix responsive for search form


## 9.1.2 (2017-01-05)

**Bugfixes**

* [fix] ordering of JS widget for expertises


## 9.1.1 (2016-12-23)

**Bugfixes**

* [fix] image upload size up to 15MB + fix size error display


## 9.1.0 (2016-12-23)

**Features and Improvements**

* [add] New reset password template RM#13346
* [imp] Update signup email template RM#16127
* [add] New email logo, remove old stuff
* [add] Email translations and manipulation for import
* [imp] Mosaic now works with bare items too
        (hide it in member detail if no result)


**Bugfixes**

* [fix] border color on white bg


## 9.1.0b3 (2016-12-21)

**Bugfixes**

* [fix] be defensive when listing country for members
* [fix] set max width for partner profile logo
* [fix] use reference icon in reference listing/search
* [fix] reference description field type and display


## 9.1.0b2 (2016-12-20)

**Bugfixes**

* [fix] status message do not overlap with content


## 9.1.0b1 (2016-12-20)

**Features and Improvements**

* [imp] do not play slider with only 1 image
* [add] ext website URL to reference model, form and view
* [add] placeholder for reference image
* Unify my * templates names (membership status, market overview, etc) and hide each one with `base.group_tester`

**Bugfixes**

* [fix] do not use links for profile progress labels
* [fix] do not display "THROUGH COLLABORATION TO INNOVATION" if token is valued in reset pwd view


## 9.1.0a8 (2016-12-19)

**Features and Improvements**

* [RM#15653](https://redmine.iart.ch/issues/15653) Adapt texts and translations from test instance
* [RM#16098](https://redmine.iart.ch/issues/16098) update member detail design
* [RM#15639](https://redmine.iart.ch/issues/15639) [add] c2c logo to footer
* unify custom modules names
* adapt mosaic a bit for responsive


## 9.1.0a7 (2016-12-15)

**Bugfixes**

* [fix] [RM#16241](https://redmine.iart.ch/issues/16241) refactor account detail form handler and fix profile update too
* [fix] profile state update, force only explicitely
* [fix] button overlay color
* [fix] some exceptions in button coloring


## 9.1.0a6 (2016-12-15)

**Features and Improvements**

* [add] [SNIPPETS LIST](odoo/local-src/theme_fluxdocs/SNIPPETS_LIST.md)
* [imp] [RM#16122](https://redmine.iart.ch/issues/16122) add auto-play carousel for project references
* [imp] [RM#16231](https://redmine.iart.ch/issues/16231) reference mosaic

    * violet overlay instead of sepia effect
    * add title to overlay
    * expand width to 2560px max (.container-xxlg)
    * adapt homepage snippet

        * update intro text + add "more" link

* [imp] reference slider max width (.container-xxlg)

  Let's be consistend with mosaic max size and wait for more design instructions.

* [add] redirect to home in login button snippet
* [add] show owner partner in linked partners RM#16098


**Bugfixes**

* [fix] [RM#16133](https://redmine.iart.ch/issues/16133) IE11 some member logos are not displayed

    * upgraded both `OCB` and `server-tools` repos to latest version
      that include some fixing for detecting images mimetypes
    * add option `attachment` to reference image field in order to preserve filename and mimetype

* [fix] [RM#16098](https://redmine.iart.ch/issues/16098) linked members not visible for anon users
* [fix] wrap mgmt actions with container fluid to have proper padding on mobile
* [fix] link colors RM#16240
* [fix] domain for m2m widget on linked_partner_ids to exclude owner
* [fix] m2m reset with no value in reference form
* [fix] RM#16098 linked members not visible for anon users
* [fix] RM#16133 IE11 some member logos are not displayed


## 9.1.0a5 (2016-12-12)

**Features and Improvements**

* [add] [RM#16122](https://redmine.iart.ch/issues/16122) carousel for project references in member detail view
* [add] profile progress: add completed message and disappear after one day


**Bugfixes**

* [fix] [RM#16132](https://redmine.iart.ch/issues/16132) styled select options visibility on FF
* [fix] [RM#16232](https://redmine.iart.ch/issues/16232) select2 input size


## 9.1.0a4 (2016-12-08)

**Features and Improvements**

* [add] make mosaic snippet work with references (was prototyped with res.partner)
* [add] tooltip to profile progress bar
* [add] "add new" button to mgmt actions
* [add] reference form status message


**Bugfixes**

* [fix] member partners ACL (allow display of members to portal users)
* [fix] reference form load country value (not matching current value)
* [fix] remove ref mosaic from account detail
* [fix] partner public URL -> always /members/slug
* [fix] make sure we find a user for a partner to show references
* [fix] be defensive when no user is found for a partner when loading references
* [fix] member detail: move projects after address

*Theme fixes*

* [fix] responsive for account detail form
* [fix] responsive for login/signup/reset pwd forms
* [fix] responsive for container fluid (missing padding)
* [fix] styles for reference detail data
* [fix] styles for alerts
* [fix] buttons and inputs styles


## 9.1.0a3 (2016-12-06)

**Features and Improvements**

* [add] references
* [add] new widget for publishing/unpublishing items


## 9.1.0a2 (2016-12-06)

**Features and Improvements**

* [RM#16093](https://redmine.iart.ch/issues/16093) [imp] redirect to /my/home after password reset too
* [RM#16142](https://redmine.iart.ch/issues/16142) [imp] prevent change email to use existing email within users


## 9.1.0a1 (2016-11-02)

WIP including fixes for 0.10 and new stuff for 1.0. Alpha versions are the WIP for this.
We'll probably include stuff that has already been done and referenced on Redmine as 1.1.0.

**Features and Improvements**

<!-- * [RM#](https://redmine.iart.ch/issues/) -->

* [RM#16095](https://redmine.iart.ch/issues/16095) [add] profile progress bar (waiting for glue w/ references and profile upgrade)
* [RM#16142](https://redmine.iart.ch/issues/16142) [imp] update email/login send reset pwd email to verify
* [imp] start splitting less files by meaningful utilities and components
* [RM#16166](https://redmine.iart.ch/issues/16166) [imp] unify markup for main content wrappers + results listing (still WIP)


**Bugfixes**

* [RM#16131](https://redmine.iart.ch/issues/16131) [fix] expertise/industries load on IE11 + fix css for s2 input field
* [fix] regression that brakes membership wizard (addresses [RM#15409](https://redmine.iart.ch/issues/15409))
* [fix] show all active membership states in /members (addresses [RM#15409](https://redmine.iart.ch/issues/15409))
* [fix] control of real form submission (account+membership) + protect membership buy controller w/ POST + CSRF
* Cleanup, improve and fix all my/home templates and reorganize them, flake8
* [RM#16132](https://redmine.iart.ch/issues/16132) [fix] country select visibility
* [fix] search by country
* [fix] make market view debuggable


## 9.0.10 (2016-11-17)

**Features and Improvements**

* [RM#15405](https://redmine.iart.ch/issues/15405) Protect member detail if current user is not associated member
* [RM#16042](https://redmine.iart.ch/issues/16042) Remove logo placeholder if logo missing
* [RM#16040](https://redmine.iart.ch/issues/16040) Insert new placeholder for logos in member aggregation
* [RM#16023](https://redmine.iart.ch/issues/16023) Update members aggregation snippet text

    NOTE: after upgrade go to translations and "synchronize terms" to update current translations.

* [RM#15403](https://redmine.iart.ch/issues/15403) Send email after confirmation of membership upgrade (invoice attached)


**Bugfixes**

* [RM#15915](https://redmine.iart.ch/issues/15915) Hide "Proposals" too in my home
* [RM#15336](https://redmine.iart.ch/issues/15336) Members slider appeareance (do not use "hidden")
* Make sure you can drop content into <main /> element when page is new (addresses RM#15336)
* [RM#15668](https://redmine.iart.ch/issues/15668) Fix subject for expertise proposal
* [RM#16043](https://redmine.iart.ch/issues/16043) Fix member detail padding
* [RM#16021](https://redmine.iart.ch/issues/16021) /login: Same Text is displayed twice

    NOTE: before upgrading - to be sure that no override has been done TTW - go to views management and delete:

    * `specific_membership.fluxdock_login`
    * `specific_membership.login`

* [RM#16020](https://redmine.iart.ch/issues/16020) member filters: reduce vertical spacing
* [RM#16105](https://redmine.iart.ch/issues/16105) member filters: css select issue
* [RM#16105](https://redmine.iart.ch/issues/16105) member filters: broken filter for anonymous users
* [RM#16027](https://redmine.iart.ch/issues/16027) Newsletter Snippet: remove "http:" in form action
* [RM#15732](https://redmine.iart.ch/issues/15732) /my/home: remove grey lines


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

* RM#14554 + RM#14555 Add project proposals and matches on backend and website
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
