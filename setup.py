from setuptools import setup
from main import __printable_version__


setup(name='projects',
      version=__printable_version__,
      description='The intuitive project manager',
      long_description="projects is an easy to use project navigation tool and a Makefile-like scripting engine. It's main purpose is to provide a simpler scripting interface with a built in man page generator. You can define your commands with inline documentation in Projectfiles. You can have one Projectfile in every directory inside your project, projects will process them recursively.",
      test_suite='test',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Topic :: Utilities',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python'
      ],
      url='https://github.com/tiborsimon/projects',
      keywords='project management command line terminal projects tool utility script scripting engine manual man',
      author='Tibor Simon',
      author_email='tibor@tiborsimon.io',
      license='MIT',
      packages=['projects'],
      scripts=['bin/p'],
      include_package_data=True,
      zip_safe=False)
