__requires__= 'funnyjoke==0.1'
import pkg_resources
pkg_resources.require("funnyjoke==0.1")
import funnyjoke
print(funnyjoke.tell())
