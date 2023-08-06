from setuptools import find_packages, setup
from snakehouse import build, Multibuild
import typing as tp
import os
from satella.files import find_files


def find_pyx(*path) -> tp.List[str]:
    return list(find_files(os.path.join(*path), r'(.*)\.pyx', scan_subdirectories=True))


setup(packages=find_packages(include=['line_intersect_2d']),
      ext_modules=build([Multibuild('line_intersect_2d', find_pyx('line_intersect_2d')), ],
                        compiler_directives={
                            'language_level': '3',
                        }),
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      zip_safe=False
      )
