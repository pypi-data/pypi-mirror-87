#!python

__requires__= 'funnyjoke==0.4'
import pkg_resources
pkg_resources.require("funnyjoke==0.4")
import funnyjoke
funnyjoke.tell()

import funnyjoke.fastjoke
funnyjoke.fastjoke.tell()
