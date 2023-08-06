from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='cockroach-core',
      version='0.0.2',
      description='',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='',
      url='http://gitlab.com/cockroach-poker/cockroach-core',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          ],
      packages=['cockroachcore'],
      scripts=[],
      python_requires='>=3.6',
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose', 'nosy'],
      include_package_data=True,
      zip_safe=False)
