# -*- coding: utf-8 -*-

import sys
import locale


def dependencyError(package, required, current=None):
    err = u'fskintra kræver %s version %s' % (package, required)
    if current:
        err += u'\n%s version %s er installeret' % (package, current)
    sys.exit(u'''%s
Se evt. her for hjælp:
    https://svalgaard.github.io/fskintra/install#krav''' % err)


#
# Check that we have Python 2.7.x
#
if sys.version_info[0] != 2 or sys.version_info[1] < 7:
    dependencyError('Python', '2.7.x', sys.version.split()[0])

#
# Beautiful Soup ?
#
try:
    import bs4
    if bs4.__version__ < '4.5':
        dependencyError('BeautifulSoup', '4.5.x', bs4.__version__)
except ImportError:
    dependencyError('BeautifulSoup', '4.5.x')

#
# lxml in a version suitable for BeautifulSoup4
#
try:
    b = bs4.BeautifulSoup('<i>test</i>', 'lxml')
except bs4.FeatureNotFound:
    dependencyError(u'lxml', u'i en version der kan køre sammen med '
                    u'BeautifulSoup 4')

#
# Mechanize
#
try:
    import mechanize
    if mechanize.__version__ < (0, 3):
        dependencyError('Mechanize', '0.3.x',
                        '.'.join(map(str, mechanize.__version__[:3])))
except ImportError:
    dependencyError('Mechanize', '0.3.x')

#
# Check that a Danish locale is available
# o.w. fail nicely
#
for loc in ['da_DK.utf-8', 'da_DK.iso8859-1', 'da_DK.iso8859-15', 'da_DK']:
    try:
        locale.setlocale(locale.LC_TIME, loc)
    except locale.Error:
        continue  # Try the next locale
    break  # Found a valid Danish locale
else:
    sys.exit(u'''
fskintra kræver at Python kan forstå datoformater på dansk (dansk locale).
Se evt. her for hjælp:
    https://svalgaard.github.io/fskintra/troubleshooting#dansk-locale
'''.lstrip())
