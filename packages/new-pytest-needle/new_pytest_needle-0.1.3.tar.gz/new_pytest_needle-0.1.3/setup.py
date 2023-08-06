"""new_pytest_needle

.. codeauthor:: P.Serega

"""

import setuptools
from new_pytest_needle.__init__ import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='new_pytest_needle',
                 version=__version__,
                 author='P.Serega',
                 author_email='serjojo1@gmail.com',
                 description='VT pytest + selenium',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=u'https://github.com/Gadzillion/new_pytest_needle',
                 license='MIT',
                 keywords=['pytest-needle', 'imagemagick', 'VT'],
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'Pillow',
                     'pytest',
                     'pytest-selenium',
                     'selenium',
                     'allure-pytest'
                 ],
                 python_requires=">=3.6",
                 classifiers=[
                     'Development Status :: 1 - Planning',
                     'Framework :: Pytest',
                     'Intended Audience :: Science/Research',
                     "Natural Language :: English",
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: POSIX :: Linux',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Software Development :: Quality Assurance',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Utilities'
                 ])
