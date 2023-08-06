__requires__= 'joke==0.1'
import pkg_resources
pkg_resources.require("joke==0.1")
import joke
print(joke.tell())
