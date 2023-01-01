#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Aldevar'
SITENAME = 'Aldevar - Le Blog'
SITEURL = 'https://blog.devarieux.net'
PATH = 'content'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'
RELATIVE_URLS = True
SITESUBTITLE = 'Yet Another Blog'
SITEIMAGE = '/images/avat180.png width=100 height=100'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feed/atom.xml'
CATEGORY_FEED_ATOM = 'feed/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'themes/m.css/pelican-theme'
THEME_STATIC_DIR = 'static'
DIRECT_TEMPLATES = ['index']

M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600','/static/m-dark.css']
M_THEME_COLOR = '#22272e'
M_SITE_LOGO_TEXT = 'ADX'
PLUGIN_PATHS = ['themes/m.css/plugins']
PLUGINS = ['m.htmlsanity', 'm.images']
M_LINKS_NAVBAR1 = [('About', '/pages/about/', 'about', []),
                   ('Twitter', 'https://twitter.com/landvarx', '', []),
                   ('LinkedIn', 'https://www.linkedin.com/in/alain-devarieux/', '', []),
                   ('Mastodon', 'https://noc.social/@Landvarx', '', [])]
#PYGMENTS_STYLE = 'monokai'


# Blogroll
#LINKS = (('Pelican', 'https://getpelican.com/'),
#         ('Python.org', 'https://www.python.org/'),
#         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
STATIC_PATHS = ['extra', 'images']
EXTRA_PATH_METADATA = {'extra/favicon.ico': {'path': 'favicon.ico'},}
ARTICLE_URL = "{date:%Y}/{date:%m}/{slug}.html"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{slug}.html"
#ARTICLE_SAVE_AS = "posts/{slug}/index.html"

## Alchemy Specific Variables
#ICONS = [
#            ('github', 'https://github.com/aldevar'),
#            ('twitter', 'https://twitter.com/landvarx'),
#            ('linkedin', 'https://www.linkedin.com/in/alain-devarieux'),
#            ('rss', '/feed/atom.xml'),
#            ]
#BOOTSTRAP_CSS = 'https://bootswatch.com/4/superhero/bootstrap.css'
#BOOTSTRAP_CSS = 'https://bootswatch.com/4/solar/bootstrap.css'
#BOOTSTRAP_CSS = 'https://bootswatch.com/4/slate/bootstrap.css'
#THEME_CSS_OVERRIDES = ['theme/css/oldstyle.css']
#HIDE_AUTHORS = True
