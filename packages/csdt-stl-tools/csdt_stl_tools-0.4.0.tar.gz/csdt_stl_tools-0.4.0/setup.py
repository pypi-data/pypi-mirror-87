from setuptools import setup, Extension
import numpy as np

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

SRC_DIR = "csdt_stl_tools"
PACKAGES = [SRC_DIR]

ext_1 = Extension(SRC_DIR + ".cwrapped",
                  [SRC_DIR + "/cwrapped.c"],
                  libraries=[],
                  include_dirs=[np.get_include()])
EXTENSIONS = [ext_1]

setup(name='csdt_stl_tools',
      version='0.4.0',
      install_requires=['numpy', 'scipy', 'matplotlib'],
      description="Generate STL files from numpy arrays and text (based on thearn/stl_tools)",
      long_description=readme(),
      long_description_content_type="text/markdown",
      author='Andrew Hunn',
      author_email='ahunn@umich.edu',
      url='https://github.com/CSDTs/csdt_stl_tools',
      license='Apache 2.0',
      packages=['csdt_stl_tools'],
      include_package_data=True,
      ext_modules=EXTENSIONS,
      entry_points={
          'console_scripts':
          ['image2stl=csdt_stl_tools.image2stl:image2stl']
      }
      )
