# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dlib(CMakePackage):
    """Dlib is a modern C++ toolkit containing machine learning algorithms and tools for creating
       complex software in C++ to solve real world problems. It is used in both industry and
       academia in a wide range of domains including robotics, embedded devices, mobile phones,
       and large high performance computing environments. Dlib's open source licensing allows
       you to use it in any application, free of charge."""

    homepage = "http://dlib.net"
    url      = "http://dlib.net/files/dlib-19.10.tar.bz2"

    version('19.16', sha256='37308406c2b1459a70f21ec2fd7bdc922277659534c708323cb28d6e8e4764a8')
    version('19.15', sha256='5340eeaaea7dd6d93d55e7a7d2fdb1f854a77b75f66049354db53671a202c11d')
    version('19.14', sha256='b552e2f1c3a4fc3fc5e9a127e3cc3c6c1b0d7bd6eb7d886a5cca1db192def034')
    version('19.13', sha256='fe90b94677f837c8f0bcb0bb450b313a422a9171ac682583a75052c58f80ba54')
    version('19.12', sha256='e6a9a20e8350b237e0bc0a8dbc6cb75714f8358e86e7964b5ad8b551f6eb8fef')
    version('19.11', sha256='3acb7525d25f445b3f8bc33ebe46f056297cc97c635abf275e6c0e7ca09ef48b')
    version('19.10', sha256='a0470f978125eea13076aa9557bf0e4990a030ad8de972225dba46b45b3b3bd1')
    version('19.9',  sha256='ec6374745d24b53568ae4d171b2ad86d102ae238dbdb093b462d5c8ae48b65b9')
    version('19.8',  sha256='dbd31f7b97166e58f366c83fa5127e9fa44c492921558b61ce63a7d775be696b')
    version('19.7',  sha256='825dbe45e0d379a4e5584c2918b1e0cb37e9ed75657766fd7b2b4f3e05f892d6')
    version('19.6',  sha256='40292a4343499b18b881f69b26a56c1ecfe95cb9b9f964f37c1064c6fc415e2c')
    version('19.5',  sha256='6f115a095962a4015b5e748feb9e3ac2ee0925ba045dcfac77821acdcbf5f2a2')
    version('19.4',  sha256='003f0508fe605cf397ad678c6976e5ec7db8472faabf06508d16ead205571372')
    version('19.3',  sha256='9c65bb3172e2e84cd194ab77d6096fd5c0574d9c67fb5176f5f884b3d540de3d')
    version('19.2',  sha256='28be8f96681e0fd196a7666ad1e1fa6994e9494aef737dd7d6985a3f1620084a')
    version('19.1',  sha256='242f3b8fbc857621d36b5c3f0b32659a9c9e9adccba794cd82d230aa1adb575c')
    version('19.0',  sha256='b6913ff6b929b7e7e5c8273f5b687eb42e8062bed109ecd9750e9d053f8d9d28')
    version('18.18', sha256='99133ed152e24d37dafa2dd19deac14d2e13c1b8ba6e187476d60f4d376117ca')
    version('18.17', sha256='c1d9a473e9d8d0ddde09b663e701a299561ff90e5d2a5b1df764f6195c099505')
    version('18.16', sha256='7549ad2b2b073753f295c5e29487ec4fd897c249bc1019feaaa63af5fc8253d2')

    depends_on('libjpeg', when='@19.0:')
    depends_on('libpng', when='@19.0:')


    # Override because versions before 19.x didn't use CMake
    def cmake(self, spec, prefix):
        if spec.version >= Version('19.0'):
            CMakePackage.cmake(self, spec, prefix)

    def build(self, spec, prefix):
        if spec.version >= Version('19.0'):
            CMakePackage.build(self, spec, prefix)
        else:
            import subprocess
            subprocess.check_call(['bash', '-c', """set -ex
                {cxx} -shared -fPIC -o libdlib.so -DDLIB_NO_GUI_SUPPORT dlib/all/source.cpp
                {cxx} -o dlib.o -DDLIB_NO_GUI_SUPPORT -c dlib/all/source.cpp
                ar rcs libdlib.a dlib.o
                """.format(cxx=self.compiler.cxx)])

    def install(self, spec, prefix):
        if spec.version >= Version('19.0'):
            CMakePackage.install(self, spec, prefix)
        else:
            import subprocess
            subprocess.check_call(['bash', '-c', """set -ex
                mkdir -p {prefix}/include {prefix}/lib
                cp -pdr dlib {prefix}/include/dlib
                """.format(prefix=prefix)])
            install('libdlib.so', join_path(prefix, "lib/libdlib.so"))
            install('libdlib.a', join_path(prefix, "lib/libdlib.a"))
