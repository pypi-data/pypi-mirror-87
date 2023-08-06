"""Setup file
"""

import setuptools

import collapse

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='collapse',
                 version=collapse.__version__,
                 description='Collapse',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 python_requires='==3.7, ==3.8',
                 url=collapse.__github_url__,
                 author='James Kennington',
                 author_email='jwkennington@psu.edu',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'matplotlib',
                     'numpy',
                     'palettable',
                     'pytest',
                     'scipy',
                     'simpy',
                 ],
                 classifiers=[
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Python :: 3.8",
                     "Operating System :: MacOS",
                     "Operating System :: POSIX :: Linux",
                 ],
                 zip_safe=False,
                 include_package_data=True,
                 )
