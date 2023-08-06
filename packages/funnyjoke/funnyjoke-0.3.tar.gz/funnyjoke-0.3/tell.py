#!/usr/bin/env python3

__requires__= 'funnyjoke==0.3'
import pkg_resources
pkg_resources.require("funnyjoke==0.3")
import funnyjoke
funnyjoke.tell()


__requires__= 'fastjoke==0.3'
import pkg_resources
pkg_resources.require("fastjoke==0.3")
import fastjoke
fastjoke.tell()
