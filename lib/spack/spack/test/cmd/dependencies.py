# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import pytest

from llnl.util.tty.color import color_when

import spack.store
from spack.main import SpackCommand

dependencies = SpackCommand('dependencies')

mpis = ['mpich', 'mpich2', 'multi-provider-mpi', 'zmpi']
mpi_deps = ['fake']


def test_immediate_dependencies(mock_packages):
    out = dependencies('mpileaks')
    actual = set(re.split(r'\s+', out.strip()))
    expected = set(['callpath'] + mpis)
    assert expected == actual


def test_transitive_dependencies(mock_packages):
    out = dependencies('--transitive', 'mpileaks')
    actual = set(re.split(r'\s+', out.strip()))
    expected = set(
        ['callpath', 'dyninst', 'libdwarf', 'libelf'] + mpis + mpi_deps)
    assert expected == actual


@pytest.mark.db
def test_immediate_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies('--installed', 'mpileaks^mpich')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['mpich', 'callpath^mpich']])

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies('--installed', '--transitive', 'mpileaks^zmpi')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['zmpi', 'callpath^zmpi', 'fake',
                              'dyninst', 'libdwarf', 'libelf']])

    assert expected == hashes
