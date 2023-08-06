from setuptools import setup
from pathlib import Path

requirements = Path('requirements.txt').read_text().split('\n')
readme = Path('README.md').read_text()

setup(name="FuseBase",
      version="0.0.3",
      description="Just some primitives for implementing a FUSE filesystem.",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://alexdelorenzo.dev",
      author="Alex DeLorenzo",
      license="AGPL-3.0",
      packages=['fusebase'],
      zip_safe=True,
      install_requires=requirements,
      keywords="fuse".split(' '),
      # entry_points={"console_scripts":
      #                   ["musicfs = musicfs.command:cmd"]},
      python_requires='~=3.7',
)
