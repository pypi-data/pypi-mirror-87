from os.path import abspath
from os.path import dirname
from os.path import join
from re import MULTILINE
from re import search
from textwrap import dedent

from setuptools import find_packages
from setuptools import setup


here = abspath(dirname(__file__))

with open(join(here, "shukujitsu", "__init__.py"), encoding="utf-8") as fp:
    version = search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     fp.read(), MULTILINE).group(1)

with open(join(here, "README.md"), encoding="utf-8") as fp:
    long_description = fp.read()

setup(name="python-shukujitsu",
      version=version,
      packages=find_packages(),
      python_requires=">=3",
      install_requires=["python-dateutil"],
      include_package_data=True,
      author="Youhei Sakurai",
      author_email="sakurai.youhei@gmail.com",
      maintainer="Youhei Sakurai",
      maintainer_email="sakurai.youhei@gmail.com",
      url="https://github.com/sakurai-youhei/python-shukujitsu",
      license="MIT",
      description=long_description.splitlines()[1],
      long_description=long_description,
      long_description_content_type="text/markdown",
      platforms="any",
      entry_points=dict(console_scripts=["shukujitsu = "
                                         "shukujitsu.__main__:main"]),
      classifiers=dedent("""\
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Natural Language :: Japanese
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: 3.8
        Programming Language :: Python :: 3.9
      """).splitlines())
