
import setuptools

with open("README.md", "r") as readme_file:
    README = readme_file.read()

setuptools.setup(
    name='sideex-webservice-client',
    version='0.9.2-1',
    author='SideeX Team',
    author_email='feedback@sideex.io',
    description='SideeX WebService Client API for Python handles the transfer of test suites to a self-hosted SideeX WebService server and returns the test reports.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SideeX/sideex-webservice-client-api-python",
    packages=setuptools.find_packages(),
    classifiers=[  # Optional
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      'License :: OSI Approved :: MIT License',

      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3',
)