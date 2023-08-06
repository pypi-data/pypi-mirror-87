# -*- coding: utf-8 -*-
#
# BackLinks plugin for Trac
#
# Author: Trapanator trap@trapanator.com
# Website: http://www.trapanator.com/blog/archives/category/trac
# License: GPL 3.0
#

import re
from StringIO import StringIO

from trac.wiki.macros import WikiMacroBase
from trac.wiki.model import WikiPage


class BackLinksListMacro(WikiMacroBase):
    """
    Inserts a list of all wiki pages with links to the page where this
    macro is used with a cleaner look.

    Accepts a page name as a parameter: if provided, pages that link to the
    provided page name are listed instead.
    """

    def expand_macro(self, formatter, name, args):

        caller_page = WikiPage(self.env, formatter.context.resource).name
        backlinks_page = args or caller_page
        db = self.env.get_db_cnx()

        backlinked_pages = \
            _get_backlinked_pages(db, caller_page, backlinks_page)

        if not backlinked_pages:
            return ''
        last_page = backlinked_pages.pop()
        buf = StringIO()
        for page in backlinked_pages:
            buf.write('<a href="%s">' % formatter.req.href.wiki(page))
            buf.write(page)
            buf.write('</a>, ')
        buf.write('<a href="%s">' % formatter.req.href.wiki(last_page))
        buf.write(last_page)
        buf.write('</a>')

        return buf.getvalue()


class BackLinksMacro(WikiMacroBase):
    """
    Inserts a list of all wiki pages with links to the page where this
    macro is used.

    Accepts a page name as a parameter: if provided, pages that link to the
    provided page name are listed instead.
    """

    def expand_macro(self, formatter, name, args):

        caller_page = WikiPage(self.env, formatter.context.resource).name
        backlinks_page = args or caller_page
        db = self.env.get_db_cnx()

        backlinked_pages = \
            _get_backlinked_pages(db, caller_page, backlinks_page)

        buf = StringIO()
        buf.write('<hr style="width: 10%; padding: 0; margin: 2em 0 1em 0;"/>')
        buf.write('Pages linking to %s:\n' % backlinks_page)
        buf.write('<ul>')
        for page in backlinked_pages:
            buf.write('<li><a href="%s">' % formatter.req.href.wiki(page))
            buf.write(page)
            buf.write('</a></li>\n')
        buf.write('</ul>')

        return buf.getvalue()


class BackLinksMenuMacro(WikiMacroBase):
    """
    Inserts a menu with a list of all wiki pages with links to the page where
    this macro is used.

    Accepts a page name as a parameter: if provided, pages that link to the
    provided page name are listed instead.
    """

    def expand_macro(self, formatter, name, args):

        caller_page = WikiPage(self.env, formatter.context.resource).name
        backlinks_page = args or caller_page
        db = self.env.get_db_cnx()

        backlinked_pages = \
            _get_backlinked_pages(db, caller_page, backlinks_page)

        buf = StringIO()
        buf.write('<div class="wiki-toc">')
        buf.write('Pages linking to %s:<br />\n' % backlinks_page)
        for page in backlinked_pages:
            buf.write('<a href="%s">' % formatter.req.href.wiki(page))
            buf.write(page)
            buf.write('</a><br />\n')
        buf.write('</div>')

        return buf.getvalue()


def _get_backlinked_pages(db, caller_page, backlinks_page):

    cursor = db.cursor()
    cursor.execute("""SELECT w1.name, w1.text FROM wiki AS w1,
        (SELECT name, MAX(version) AS version FROM wiki GROUP BY name) AS w2
        WHERE w1.version = w2.version AND w1.name = w2.name AND
        (w1.text %s)""" % db.like(),
        ('%' + db.like_escape(backlinks_page) + '%',))

    pattern = re.compile(r'\b%s\b' % re.escape(backlinks_page), re.UNICODE)
    backlinked_pages = []
    for page, text in cursor:
        if page != backlinks_page and page != caller_page \
                and pattern.search(text):
            backlinked_pages.append(page)

    return backlinked_pages
