# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dia(Package):
    """Dia is a program for drawing structured diagrams."""
    homepage  = 'https://wiki.gnome.org/Apps/Dia'
    url       = 'https://ftp.gnome.org/pub/gnome/sources/dia/0.97/dia-0.97.3.tar.xz'

    version('0.97.3',    '0e744a0f6a6c4cb6a089e4d955392c3c')

    depends_on('intltool', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('gtkplus@2.6.0:')
    depends_on('libxslt')
    depends_on('python')
    depends_on('swig')
    depends_on('libsm')
    depends_on('libuuid')
    depends_on('libxinerama')
    depends_on('libxrender')
    depends_on('libxml2')
    depends_on('freetype')

    # TODO: Optional dependencies, not yet supported by Spack
    # depends_on('libart')
    # depends_on('py-pygtk', type=('build', 'run'))

    def url_for_version(self, version):
        """Handle Dia's version-based custom URLs."""
        return 'https://ftp.gnome.org/pub/gnome/sources/dia/%s/dia-%s.tar.xz' % (version.up_to(2), version)

    def install(self, spec, prefix):

        # configure, build, install:
        options = ['--prefix=%s' % prefix,
                   '--with-cairo',
                   '--with-xslt-prefix=%s' % spec['libxslt'].prefix,
                   '--with-python',
                   '--with-swig']

        configure(*options)
        make()
        make('install')
