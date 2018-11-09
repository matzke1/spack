# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# -----------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
# -----------------------------------------------------------------------------

from spack import *


class Rose(Package):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url      = "https://github.com/rose-compiler/rose/archive/v0.9.7.tar.gz"
    git      = "https://github.com/rose-compiler/rose.git"

    version('master', branch='master')
    version('0.9.7', 'e14ce5250078df4b09f4f40559d46c75')

    variant('binanalysis', default=True,  description='Enable binary analysis support')
    variant('c',           default=True,  description='Enable c language support')
    variant('cxx',         default=True,  description='Enable c++ language support')
    variant('fortran',     default=False, description='Enable fortran language support')
    variant('java',        default=False, description='Enable java language support')
    variant('edgtarball',  default=False, description='Generate and install EDG binary tarball')

    # If non-empty, this is the build directory being used by the developer to develop ROSE.
    # In this case, most of Spack's actions are skipped, including the installation.
    variant('development', values=str, default='', description='Used only by ROSE developers')

    #patch('add_spack_compiler_recognition.patch')

    # This config was needed when compiling on Robb's laptop
    # running Linux Mint 19 and GCC-8.2.0 when using wt
    # ^python@3.6.1 ^glib@2.49.7 ^pango@1.40.3
    depends_on('autoconf@2.69',   type='build')   # really, only 2.69?
    depends_on('automake@1.15.1', type='build')   # really, ony 1.15.1?
    depends_on('boost@1.61.0:')
    depends_on('dlib',            when='+binanalysis')
    depends_on('java',            when='+java')
    #depends_on('libdwarf',        when='+binanalysis') # no robust support in ROSE
    #depends_on('libelf',          when='+binanalysis') # no robust support in ROSE
    depends_on('libgcrypt',       when='+binanalysis')
    depends_on('libtool@2.4.6',   type='build')   # really, only 2.4.6?
    depends_on('py-binwalk',      when='+binanalysis')
    #depends_on('tup',             type='build') # not installing on RHEL7.5 (needs fuse)
    #depends_on('wt',              when='+binanalysis') # problems building in spack
    depends_on('yaml-cpp',        when='+binanalysis')
    depends_on('z3')

    phases = ['autoreconf', 'configure', 'build', 'install']

    @property
    def build_dir(self):
        if self.spec.variants['development'].value == '':
            return join_path(self.stage.source_path, '_build-spack')
        else:
            return self.spec.variants['development'].value

    @property
    def languages(self):
        spec = self.spec
        langs = [
            'binaries' if '+binanalysis' in spec else '',
            'c' if '+c' in spec else '',
            'c++' if '+cxx' in spec else '',
            'java' if '+java' in spec else '',
            'fortran' if '+fortran' in spec else ''
        ]
        return list(filter(None, langs))

    def with_prefix_or_no(self, spec, package, arg='', suffix=''):
        if (arg == ''):
            retval = '--with-' + package + '='
        else:
            retval = arg + '='

        if (package in spec):
            retval += spec[package].prefix + suffix
        else:
            retval += 'no'
        return retval
    
    def configure_args(self):
        return [
            '--prefix={0}'.format(self.prefix),
            '--disable-boost-version-check',
            '--disable-gcc-version-check',
            '--enable-languages={0}'.format(','.join(self.languages)),
            '--with-alternate_backend_C_compiler={0}'.format(self.compiler.cc),
            '--with-alternate_backend_Cxx_compiler={0}'.format(self.compiler.cxx),
            '--with-ROSE_LONG_MAKE_CHECK_RULE=yes',
            self.with_prefix_or_no(self.spec, 'boost'),
            self.with_prefix_or_no(self.spec, 'libdwarf', arg='--with-dwarf'),
            '--with-cuda=no',
            self.with_prefix_or_no(self.spec, 'dlib', suffix='/include'),
            self.with_prefix_or_no(self.spec, 'libelf', arg='--with-elf'),
            self.with_prefix_or_no(self.spec, 'libgcrypt', arg='--with-gcrypt'),
            '--with-java=no',
            '--with-readline=no',
            '--with-magic=no',
            '--with-pch=no',
            '--with-pqxx=no',
            '--with-python=no',
            '--with-sqlite=no',
            self.with_prefix_or_no(self.spec, 'wt'),
            self.with_prefix_or_no(self.spec, 'yaml-cpp', arg='--with-yaml'),
            '--with-yices=no',
            self.with_prefix_or_no(self.spec, 'z3')
        ]

    def autoreconf(self, spec, prefix):
        if self.spec.variants['development'].value == '':
            bash = which('bash')
            bash('./build')

    def configure(self, spec, prefix):
        configure_path = join_path(self.stage.source_path, "configure")
        configure_script = which(configure_path)
        args = self.configure_args();

        with working_dir(self.build_dir, create=True):
            # Create a shell script for running configure so it can be used by ROSE developers
            with open('configure-rerun', 'w') as output:
                output.write('#!/bin/bash\n')
                output.write('if [ "$SPACK_PREFIX" = "" ]; then\n')
                output.write('    echo "$0: must be run in a Spack environment" >&2\n')
                output.write('    exit 1\n')
                output.write('fi\n')
                output.write(' '.join(map(lambda x: "'"+x+"'", ['exec', configure_path]+args)))
                output.write('\n')
            import os
            os.chmod('configure-rerun', 0777)

            # Save the ROSE spec in case we need it later
            with open('spack-spec', 'w') as output:
                output.write(self.spec.short_spec)
                output.write('\n')
                
            # Run the configure script only if we're not a ROSE developer
            if self.spec.variants['development'].value == '':
                configure_script(*args)

    def build(self, spec, prefix):
        if self.spec.variants['development'].value == '':
            with working_dir(self.build_dir):
                make('-C', 'src')
                if '+binanalysis' in spec:
                    make('-C', 'projects/BinaryAnalysisTools')

    def install(self, spec, prefix):
        if self.spec.variants['development'].value != '':
            # Prevent installation in development mode
            raise InstallError('installation not supported in ROSE development mode\n' +
                               '   Your build tree is now configured to develop ROSE.\n' +
                               '   The above error is normal and expected during development\n')
        else:
            with working_dir(self.build_dir):
                make('install-rose-library')

                if '+binanalysis' in spec:
                    make('-C', 'projects/BinaryAnalysisTools', 'install')

                if '+edgtarball' in spec:
                    make('-C', 'src/frontend/CxxFrontend', 'binary_edg_tarball')
                    mkdirp(join_path(prefix, "share"))
                    import subprocess
                    subprocess.check_call(['bash', '-c', """set -ex
                        cp -dp src/frontend/CxxFrontend/*.tar.gz {prefix}/share/.
                        """.format(prefix=prefix)])

