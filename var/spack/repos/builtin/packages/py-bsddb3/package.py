# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBsddb3(PythonPackage):
    """This module provides a nearly complete wrapping of the Oracle/Sleepycat
       C API for the Database Environment, Database, Cursor, Log Cursor,
       Sequence and Transaction objects, and each of these is exposed
       as a Python type in the bsddb3.db module."""

    homepage = "https://pypi.python.org/pypi/bsddb3/6.2.5"
    url      = "https://pypi.io/packages/source/b/bsddb3/bsddb3-6.2.5.tar.gz"

    version('6.2.5', '610267c189964c905a931990e1ba438c')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')
    depends_on('berkeley-db')

    # For testing... see here for an example that uses BerkeleyDB
    # http://code.activestate.com/recipes/189060-using-berkeley-db-database/
