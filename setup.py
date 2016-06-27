from setuptools import setup
from main import __version__


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='projects',
      version=__version__,
      description='The extensible project manager',
      long_description=readme(),
      test_suite='test',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Topic :: Utilities',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Unix',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/tiborsimon/projects',
      keywords='project management command line terminal projects tool utility',
      author='Tibor Simon',
      author_email='tibor@tiborsimon.io',
      license='MIT',
      packages=['projects'],
      scripts=['bin/p'],
      include_package_data=True,
      zip_safe=False)
