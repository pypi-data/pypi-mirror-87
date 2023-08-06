"""Nitrous Setup."""

import os
import sys

from setuptools import setup, find_packages


version = "0.8.4"
description = "Nitrous gives TurboGears 1 a boost"
long_description = """
Project Nitrous
===============

Project Nitrous is a port of TurboGears 1 to Python 3 and a modern
development stack.

It is intended to ease support for legacy projects in a post-Python 2
world. If you're starting a new project, Nitrous isn't for you: check
out one of these excellent Python Web Frameworks: Pyramid, Django, or
Flask.

Nitrous is maintained by BrightLink.
"""

author = "BrightLink"
email = "drocco@thebrightlink.com"
maintainer = "BrightLink"
maintainer_email = "drocco@thebrightlink.com"
url = "https://bitbucket.org/brightlinkinfrastructure/nitrous"
download_url = f"https://bitbucket.org/brightlinkinfrastructure/nitrous/get/v{version}.tar.gz"
dependency_links = [download_url]
copyright = "Copyright 2019 BrightLink and contributors"
license = "MIT"


# setup params
install_requires = [
    'attrs >= 19.0.0',
    'CherryPy >= 3.1.2',
    'ConfigObj >= 4.3.2',
    'FormEncode >= 1.3.0',
    'future >= 0.17.1',
    'Genshi >= 0.4.4',
    'simplejson >= 3.17.0',
    'TGScheduler >= 1.6.2',
]


setup(
    name='Nitrous',
    description=description,
    long_description=long_description,
    version=version,
    author=author,
    author_email=email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    url=url,
    download_url=download_url,
    dependency_links=dependency_links,
    license=license,
    zip_safe=False,
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points = """
    [console_scripts]
    tg-admin = turbogears.command:main

    [distutils.commands]
    docs = turbogears.docgen:GenSite

    [python.templating.engines]
    default-json = turbogears.view.json:DefaultJSONRendererPlugin
    default-text = turbogears.view.text:DefaultTextRendererPlugin

    [turbogears.command]
    sql = turbogears.command.base:SQL
    shell = turbogears.command.base:Shell
    toolbox = turbogears.command.base:ToolboxCommand
    i18n = turbogears.command.i18n:InternationalizationTool
    info = turbogears.command.info:InfoCommand
    kid2genshi = turbogears.command.kid2genshi:Kid2Genshi

    [turbogears.identity.provider]
    sqlalchemy= turbogears.identity.saprovider:SqlAlchemyIdentityProvider

    [turbogears.extensions]
    identity = turbogears.identity.visitor
    visit = turbogears.visit

    [turbogears.visit.manager]
    sqlalchemy = turbogears.visit.savisit:SqlAlchemyVisitManager

    [turbogears.toolboxcommand]
    widgets = turbogears.toolbox.base:WidgetBrowser
    shell = turbogears.toolbox.shell:WebConsole
    admi18n = turbogears.toolbox.admi18n:Internationalization
    designer = turbogears.toolbox.designer:Designer
    info = turbogears.toolbox.base:Info
    catwalk = turbogears.toolbox.catwalk:CatWalk

    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: TurboGears',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
