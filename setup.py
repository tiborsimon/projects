from setuptools import find_packages, setup

setup(
    name='projects',
    version='1.0.4',
    description='The intuitive project manager',
    long_description=("projects is an easy to use project navigation tool "
                      "and a Makefile-like scripting engine. It's main purpose "
                      "is to provide a simpler scripting interface with a built "
                      "in man page generator. You can define your commands with "
                      "inline documentation in Projectfiles. You can have one "
                      "Projectfile in every directory inside your project, "
                      "projects will process them recursively."),
    author='Tibor Simon',
    author_email='tibor@tiborsimon.io',
    url='https://github.com/tiborsimon/projects',
    license='MIT',
    test_suite='test',
    keywords='project management command line terminal projects tool utility script scripting engine manual man',
    packages=find_packages(),
    scripts=['bin/p'],
    install_requires=[
          'mock>=2.0.0',
          'urwid',
          'pyyaml',
          'termcolor',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'Environment :: Console',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
    ],
)
