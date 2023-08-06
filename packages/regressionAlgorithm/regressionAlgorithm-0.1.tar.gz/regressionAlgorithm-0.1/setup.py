from setuptools import setup

def readme():
  with open('README.md') as f:
    README = f.read()
    return README

setup(
  name = 'regressionAlgorithm',
  packages = ['regressionAlgorithm'],
  version = '0.1',
  license='MIT',
  description = 'Linear Regression Algorithm',
  long_description_content_type="text/markdown",
  long_description=readme(),
  author = 'Rizki Maulana',
  author_email = 'rizkimaulana348@gmail.com',
  url = 'https://github.com/rizki4106/regressionAlgorithm',
  download_url = 'https://github.com/rizki4106/regressionAlgorithm/v_01.tar.gz',
  keywords = ['linear-regression', 'machine-learning', 'supervise-learning'],
  install_requires=[
          'numpy==1.19.3',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)