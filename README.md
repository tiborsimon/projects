#p - the extensible project manager

 __p__ is a project management tool. You can list all of your projects and access
 them with ease. Custom, project specific commands can be defined also. The built
 in plugin system provides maximal flexibility.
 
 
 ```
from v1.1

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
