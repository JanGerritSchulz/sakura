import os
from setuptools import setup, find_packages

with open('README.md') as f:
    long_desc = f.read()

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_requires = []
with open(requirements_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        install_requires.append(line)

setup(name="sakura",
      version='0.1.0',
      description="A plotting package for CMS DQM files with special functionality for SimDoublets",
      long_description_content_type="text/markdown",
      author="J. G. Schulz",
      url="https://github.com/JanGerritSchulz/sakura",
      long_description=long_desc,
      entry_points={'console_scripts':
                    ['makeCutPlots = simplotter.makeCutPlots:main',
                     'makeGeneralPlots = simplotter.makeGeneralPlots:main',
                     'compareROOT = rootcomparer.compareROOTfiles:main']},
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          "Operating System :: OS Independent",
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
      ],
      python_requires='>=3.9',
      install_requires=install_requires,
      )