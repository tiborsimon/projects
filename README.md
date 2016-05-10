#PROJECTS - the extensible project manager

[![Join the chat at https://gitter.im/tiborsimon/projects](https://badges.gitter.im/tiborsimon/projects.svg)](https://gitter.im/tiborsimon/projects?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Warning - this projects is currently under development and it is not ready to use!

[![Build Status](https://travis-ci.org/tiborsimon/projects.svg?branch=master)](https://travis-ci.org/tiborsimon/projects) [![PyPI](https://img.shields.io/pypi/v/projects.svg?maxAge=2592000)](https://pypi.python.org/pypi?name=projects&version=0.1.1&:action=display)

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
