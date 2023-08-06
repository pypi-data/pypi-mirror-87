# coding: utf-8
"""Setup script for IVA NN applications service."""

from setuptools import find_packages, setup

setup(name='iva_applications',
      version='7.1.2',
      author='IVA Technologies',
      author_email='engineering@iva-tech.ru',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=[
            'matplotlib',
            'Pillow',
            'scikit-build',
            'opencv-python',
            'scipy==1.4.1',
            'numpy',
            'scikit-image',
            'tensorflow==2.2.0',
            'keras==2.2.4',
            'pydrive'
      ])
