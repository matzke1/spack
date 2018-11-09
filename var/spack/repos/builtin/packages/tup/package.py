# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tup(Package):
    """Tup is a file-based build system."""

    homepage = "http://gittup.org/tup"
    git      = "https://github.com/gittup/tup.git"

    version('0.7.8', tag='v0.7.8')
    version('0.7.7', tag='v0.7.7')

    depends_on('pcre')
    patch('honor_c_compiler.patch')
    patch('avoid_git_commands.patch')

    def install(self, spec, prefix):
        import subprocess
        subprocess.check_call(['bash', '-c', """set -ex
            mv Tuprules.tup Tuprules.tup.orig
            (export |sed -e '/declare -x/ s/declare -x \\([_a-zA-Z0-9]\\+\\).*/export \\1/p' &&
             cat Tuprules.tup.orig) > Tuprules.tup
            ./bootstrap.sh
            mkdir -p {prefix}/bin
            cp tup {prefix}/bin/.
            mkdir -p {prefix}/man/man1
            cp tup.1 {prefix}/man/man1""".format(prefix=prefix)])
