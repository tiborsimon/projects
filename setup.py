from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='projects',
      version='0.1.1',
      description='The extensible project manager',
      long_description=readme(),
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
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
      test_suite='test',
      scripts=['bin/p', 'bin/pw'],
      include_package_data=True,
      zip_safe=False)
