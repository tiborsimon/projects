#PROJECTS - the extensible project manager

[![Gitter](https://img.shields.io/gitter/room/tiborsimon/projects.svg?maxAge=2592000)](https://gitter.im/tiborsimon/projects?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/tiborsimon/projects.svg?branch=master)](https://travis-ci.org/tiborsimon/projects)
[![Coverage Status](https://coveralls.io/repos/github/tiborsimon/projects/badge.svg?branch=master)](https://coveralls.io/github/tiborsimon/projects?branch=master)
[![PyPI](https://img.shields.io/pypi/v/projects.svg?maxAge=2592000)](https://pypi.python.org/pypi?name=projects&version=0.1.1&:action=display)
[![license](https://img.shields.io/github/license/tiborsimon/projects.svg?maxAge=2592000)](https://github.com/tiborsimon/projects#license)
[![PyPI](https://img.shields.io/pypi/dm/projects.svg?maxAge=2592000)](https://pypi.python.org/pypi?name=projects&version=0.1.1&:action=display)
[![Status](https://img.shields.io/badge/status-under_development-yellow.svg)]()


 __PROJECTS__ is a project management tool. You can list all of your projects and access
 them with ease. Custom, project specific commands can be defined also. The built
 in plugin system provides maximal flexibility.
 
 
 ```
from v1.1.0

deploy_url = 'hello_imre'

bootstrap|b:
  """
  This is the initialization command that you should run on a clean project.
  """
  mkdir build
  cd build
  cmake ..
  make
  ===
  cd ..
  git status

publish|p: [bootstrap, build]
  """
  Publishing the project means that you will upload this project to the deployment server
  """
 ```
 
 ```
 {
    'min-version': 'v1.1.0',
    'commands': {
        'bootstrap': {
            'description': 'This is the initialization command that you should run on a clean project.',
            'dependency': [],
            'pre': ['mkdir build', 'cd build', 'cmake ..', 'make'],
            'post': ['cd ..', 'git status']
        },
        'b': {
            'alias': 'bootstrap'
        },
        'publish': {
            'description': 'Publishing the project means that you will upload this project to the deployment server',
            'dependency': ['bootstrap', 'build'],
            'pre': [],
            'post': []
        },
        'p': {
            'alias': 'publish'
        }
    }
}
```


## License

This project is under the __MIT license__. 
See the included license file for further details.

```
Copyright (c) 2016 Tibor Simon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
