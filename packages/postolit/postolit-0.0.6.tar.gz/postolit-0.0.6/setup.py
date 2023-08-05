import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["opencv-python<=4.4.0.46"]

setup(name='postolit',
      version='0.0.6',
      author="prof. Anatoly Postolit",
      author_email='anat_post@mail.ru',
      description='Postoperative Library for Image Transformation',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/APostolit",
      packages=setuptools.find_packages(),
      # packages=['postolit'],
      install_requires=requirements,
      license='LICENSE',
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.7',
      )
