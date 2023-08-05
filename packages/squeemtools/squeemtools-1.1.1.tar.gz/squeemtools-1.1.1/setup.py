from setuptools import setup, find_packages
setup(
  name = 'squeemtools',
  packages = find_packages(),
  version = '1.1.1',
  license='MIT',
  description = 'Packages of misceallaneous use. Combination of all things created/used for projects.',
  author = 'Ben van Oostendorp',
  author_email = 'ben.vano@digipen.edu',
  url = 'https://github.com/Squeemos/SqueemTools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Squeemos/SqueemTools/archive/SqueemTools_1.1.1.tar.gz',    # I explain this later on
  keywords = ['GRAPHING', 'FUZZY C MEANS','GLM', 'ID3'],
  install_requires=[
          'matplotlib',
          'numpy',
          'pandas',
          'numdifftools',
          'scipy',
          'xarray',
          'sklearn',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)