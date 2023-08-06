Changelog
=========

4.3.52 (2020-12-04)
-------------------

- Fix setup.py parsing.
  [bsuttor]


4.3.51 (2020-12-04)
-------------------

- WEB-3480: Fix strange error during upgrade step on some of our instance.
  [bsuttor]

- WEB-3449: Handle prevent actions in folderish migration
  [laulaz]

- WEB-3449: Make folderish migration more robust
  [laulaz]


4.3.50 (2020-09-17)
-------------------

- WEB-3347: Keep object position in parent folder after folderish migration
  [laulaz]

- WEB-3304: Set cpskin.diazotheme.newDream as default theme instead of classic.
  [boulch]

- Add upgrade / change setup to ensure that all folders are orderable
  We had bugs with news / events folders and previous / next navigation
  [laulaz]

- Remove include of permissions.zcml from plone.app.controlpanel, it's fixed on plone.restapi 6.13.2.
  [bsuttor]


4.3.49 (2020-06-11)
-------------------

- Include permissions.zcml from plone.app.controlpanel to fix plone.restapi permissions.
  [bsuttor]


4.3.48 (2020-05-30)
-------------------

- Avoid any bug with incomplete requests and eea facetednavigation CSS / JS
  conditions : WEB-2975
  [laulaz]


4.3.47 (2020-05-25)
-------------------

- Add collective.anysurfer dependency : WEB-3243
  [laulaz]


4.3.46 (2020-04-28)
-------------------

- WEB-3302: Add slick css resource
  [mpeeters]


4.3.45 (2020-04-02)
-------------------

- Add imio.prometheus dependency.
  [bsuttor]


4.3.44 (2020-01-17)
-------------------

- Add view to fix partially migrated content types to folderish : WEB-3156
  Fix view can be called from @@fix-folderishtypes
  [laulaz]

- Auto install collective.captchacontactinfo with gdpr link informations + upgrade steps
  [boulch]


4.3.43 (2019-07-09)
-------------------

- Improve CSS media queries sizes
  [laulaz]


4.3.42 (2019-04-25)
-------------------

- Add pas.plugins.imio dependency.
  [bsuttor]


4.3.41 (2019-04-10)
-------------------

- Interface should be provided during the migration to avoid some bugs.
  plone.app.contenttypes has been modified in that perspective : WEB-2993
  [laulaz]


4.3.40 (2019-04-02)
-------------------

- Fix missing interface on folderish contents. This has been fixed in latest
  versions of plone.app.contenttypes : WEB-2993
  [laulaz]


4.3.39 (2019-04-01)
-------------------

- Add migration view to convert content types to folderish : WEB-2975
  Migration can be called from @@migrate-folderishtypes
  [laulaz]


4.3.38 (2019-03-26)
-------------------

- Set autopublishing on installation and add upgrade step to set it.
  [bsuttor]


4.3.37 (2019-03-25)
-------------------

- Add needed subscriber for collective.autopulishing
  [laulaz]


4.3.36 (2019-03-25)
-------------------

- Add collective.autopulishing dependency.
  [bsuttor]


4.3.35 (2019-03-18)
-------------------

- Add cpskin.contenttypes package (not installed by default) : WEBOTT-10
  [laulaz]


4.3.34 (2019-03-12)
-------------------

- Add collective.behavior.targetblank dependency.
  [bsuttor]


4.3.33 (2018-08-30)
-------------------

- Do not install uninstall plone.restapi.
  [bsuttor]


4.3.32 (2018-08-29)
-------------------

- Do not install and uninstall plone.restapi from now.
  [bsuttor]


4.3.31 (2018-07-13)
-------------------

- Fix: call good handler to upgrade step.
  [bsuttor]


4.3.30 (2018-07-11)
-------------------

- Add upgradestep to install plone.restapi.
  [bsuttor]


4.3.29 (2018-07-10)
-------------------

- Add plone.restapi dependency.
  [bsuttor]

- Unpin old plone.api
  [laulaz]

- Update cookiecuttr message.
  [bsuttor]


4.3.28 (2018-04-23)
-------------------

- Upgrade step to clean resolveuid links.
  [bsuttor]

- Update fonts to https.
  [bsuttor]


4.3.27 (2018-01-31)
-------------------

- Fix variable name.
  [bsuttor]


4.3.26 (2018-01-31)
-------------------

- Upgrade step to completely remove collective.contentleadimage.
  [bsuttor]


4.3.25 (2018-01-23)
-------------------

- Sync SiteManager after changed it.
  [bsuttor]


4.3.24 (2018-01-23)
-------------------

- Fix latest upgrade step.
  [bsuttor]


4.3.23 (2018-01-23)
-------------------

- Upgrade step to completely remove collective.contentleadimage.
  [bsuttor]


4.3.22 (2017-12-13)
-------------------

- Add and install collective.limitfilesizepanel.
  [bsuttor]


4.3.21 (2017-12-12)
-------------------

- Add cpskin.agenda overrides.
  [bsuttor]


4.3.20 (2017-11-28)
-------------------

- Install cpskin contact workflow.
  [bsuttor]

- Do not set use_email_as_login as default.
  [bsuttor]


4.3.19 (2017-11-28)
-------------------

- Set use_email_as_login to True on install.
  [bsuttor]

- Update smtp mail url.
  [bsuttor]

- Remove collective.directory auto install
  [bsuttor]

- Add auto install of collective.contact.core.
  [bsuttor]

- Allow organization type only to organization (no more position).
  [bsuttor]


4.3.18 (2017-03-29)
-------------------

- Set default image_max_width to 1920.
  [bsuttor]


4.3.17 (2017-02-01)
-------------------

- Set a cpskin workflow version.
  [bsuttor]


4.3.16 (2017-02-01)
-------------------

- Add upgrade step to add cpskin_collective_contact_workflow.
  [bsuttor]


4.3.15 (2016-12-06)
-------------------

- Fix upgrade step which set mailhost.
  [bsuttor]


4.3.14 (2016-12-05)
-------------------

- Configure mail_host to use smtp_queue.
  [bsuttor]


4.3.13 (2016-11-25)
-------------------

- Add collective.sendinblue to dependency.
  [bsuttor]


4.3.12 (2016-11-16)
-------------------

- Set default_enabled syndication settings to true.
  [bsuttor]

- Resort css to prevent IE menu error.
  [bsuttor]


4.3.11 (2016-09-23)
-------------------

- Include collective.preventactions into zcml.
  [bsuttor]


4.3.10 (2016-09-22)
-------------------

- Add collective.preventactions
  [bsuttor]

- Added first robot screenshot.
  [sgeulette]

- Use cpskin.demo in tests
  [sgeulette]

4.3.9 (2016-08-24)
------------------

- Install collective.autoscaling on profile installation.
  [bsuttor]


4.3.8 (2016-07-26)
------------------

- Add collective.autoscaling.
  [bsuttor]


4.3.7 (2016-07-07)
------------------

- Add collective.excelexport
  [bsuttor]


4.3.6 (2016-06-01)
------------------

- Enable sitemap and DC metadata
  [jfroche]

- Add cpskin.agenda
  [bsuttor]


4.3.5 (2016-05-18)
------------------

- Add cpskin.caching
  [jfroche]

- Add timezone for plone.app.event
  [bsuttor]

- Do not purge image scales.
  [bsuttor]

- Add IUseKeywordHomepage behavior for folder.
  [bsuttor]


4.3.4 (2016-04-21)
------------------

- Add carousel image size and reset other images scales.
  [bsuttor]


4.3.3 (2016-04-07)
------------------

- Add allowed scales for image cropping.
  [bsuttor]

- Set new images allowed scales.
  [bsuttor]

- Set mailhost to frontend1.
  [bsuttor]


4.3.2 (2016-03-22)
------------------

- Add cpskin core overrides.
  [bsuttor]

- Add standard tags for dexterity contents.
  [bsuttor]


4.3.1 (2016-02-26)
------------------

- Add plone.app.imagecropping and support image cropping for all content types
  [laulaz]


4.3.0 (2016-02-19)
------------------

- Order a-la-une folder to top.
  [bsuttor]

- Add default js order registry.
  [bsuttor]

- Add default css order registry.
  [bsuttor]


4.2.4 (2016-02-17)
------------------

- Fix registry for not deleted all css.
  [bsuttor]

4.2.3 (2016-02-17)
------------------

- Clean up registries with an upgrade steps.
  [bsuttor]

- Add dependency to imio.migrator
  [bsuttor]

- Add a-la-une folder during installation
  [bsuttor]


4.2.2 (2016-01-08)
------------------

- Fix typo error 'Ma commue'
  [bsuttor]

- Add include of plone.app.event in zcml for fixing tests
  [bsuttor]

- Add collective.cookiecuttr dependency into setup.py
  [bsuttor]


4.2.1 (2015-11-24)
------------------

- Add collective.cookiecuttr upgrade step
  [bsuttor]

- Add collective.cookiecuttr
  [bsuttor]

- Pin cpskin.minisite
  [schminitz]


4.2.0 (2015-07-17)
------------------

- Add collective.monitor package
  [bsuttor]

- Add upgrade step which install collective.atomrss.
  [bsuttor]

- Add upgrade step for removing cleanly multilingualbehavior and multilingual if needed.
  [bsuttor]


4.1.8 (2015-03-12)
------------------

- Add collective.atomrss plugin
  [bsuttor]


4.1.7 (2015-03-06)
------------------

- Add upgrade steps for deleting old multilingualbehavior
  [bsuttor]


4.1.6 (2015-02-02)
------------------

- Add auto installed products : Products.PloneFormGen, Products.PloneGazette, Solgema.fullcalendar.
  [bsuttor]

- Set cpskin.diazotheme.classic as default theme.
  [bsuttor]


4.1.5 (2014-10-30)
------------------

- Add collective.jekyll dependency.


4.1.4 (2014-10-22)
------------------

- Add zcml include for cpskin.diazotheme.classic


4.1.3 (2014-10-22)
------------------

- Add cpskin.diazotheme.classic.


4.1.2 (2014-10-07)
------------------

- Remove MenuTools viewlet (affinitic #6023)

- Define allowed sizes for imaging properties
  [bsuttor]


4.1.1 (2014-10-02)
------------------

- Add Products.PasswordStrength.


4.1 (2014-08-21)
----------------

- Nothing changed yet.


4.0 (2014-07-02)
----------------

- Initial release
