Changelog
=========

0.2.12 (2020-12-04)
-------------------

- Return empty string if no data from provider.
  [bsuttor]


0.2.11 (2020-06-17)
-------------------

- Really unshort url #SUP-13464.
  [bsuttor]


0.2.10 (2020-06-15)
-------------------

- Fix UnicodeEncodeError in video title.
  [boulch]


0.2.9 (2020-06-12)
------------------

- override consumer get_embed (endpoints.py), to patch youtube and vimeo provider with their good cookieless url
  [boulch]
- Create our (cookieless) consumer, override oembed provider to use our consumer.
  [boulch]

0.2.8 (2019-08-30)
------------------

- Remove useless css class and fix faceted description printing
  [cboulanger]


0.2.7 (2019-08-29)
------------------

- Add new Rich Text Description field
- Print Detailed Description and hide "classic" description in Medialink page
- Print description below each medialink in collection view and can hide it thanks to ICpskinIndexViewSettings show_descriptions settings
  [cboulanger]


0.2.6 (2018-04-06)
------------------

- Add title and link to obj on faceted view.
  [bsuttor]


0.2.5 (2018-04-03)
------------------

- Add Faceted items OEmbeded view.
  [bsuttor]

- Use unittest instead of unittest2.
  [bsuttor]

- Add missing import for tests
  [laulaz]

0.2.4 (2016-06-24)
------------------

- Fixing tests, add plone.app.contenttypes dependency.
  [bsuttor]


0.2.3 (2016-05-17)
------------------

- Add support for dexterity collection.
  [bsuttor]

- Fixing tests because of a change from Vimeo.
  [bsuttor]

- Add IMIO Jenkins integration.
  [bsuttor]


0.2.2 (2014-08-26)
------------------

- Add batch navigation into collection view.
  [bsuttor]

- Fix error on manage-portlets view where a old version of portlet was use.
  [bsuttor]


0.2.1 (2014-08-20)
------------------

- Add a title to media_link portlet
  [bsuttor]


0.2 (2014-08-14)
----------------

- Fix error if collection_oembed_view is used with other type than media_link.
  [bsuttor]

- Add picto media-link
  [bsuttor]

- Add portlet
  [bsuttor]


0.1.3 (2014-06-10)
------------------

- Heritage from dexterity item
  [bsuttor]

- Remove IVersionnable behaviors.
  [bsuttor]


0.1.2 (2014-06-06)
------------------

- Remove old files and old dependency
  [bsuttor]


0.1.1 (2014-06-06)
------------------

- Remove unused dependecy plone.app.contenttypes.
  [bsuttor]


0.1 (2014-06-06)
----------------

- Package created using mr.bob
  [bsuttor]
