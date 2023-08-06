import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()
  setuptools.setup(
    name="hangul-korean",
    version="1.0rc1",
    author="Yongkyoon No 노용균",
    author_email="yno@linguist.cnu.ac.kr",
    description="Word segmentation for the Korean Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noyongkyoon/hangul",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
      '': ['data/word2idx0.json', 'models/*.hdf5']
    },
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Natural Language :: Korean",
      "Topic :: Scientific/Engineering :: Information Analysis",
      "Topic :: Text Processing :: Linguistic",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
      "Operating System :: OS Independent",
    ],
    keywords='Korean tokenization word_segmentation',
    install_requires=[
      "pandas",
      "tensorflow",
      "tensorflow_addons"
    ],
    python_requires='>=3.8',
  )
