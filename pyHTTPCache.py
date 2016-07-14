# pyHTTPCache

import hashlib
import os
import requests

############################################################
# HELPERS
############################################################

# LazyProperty Decorator
class LazyProperty(object):
	'''
	meant to be used for lazy evaluation of an object attribute.
	property should represent non-mutable data, as it replaces itself.
	'''

	def __init__(self,fget):
		self.fget = fget
		self.func_name = fget.__name__


	def __get__(self,obj,cls):
		if obj is None:
			return None
		value = self.fget(obj)
		setattr(obj,self.func_name,value)
		return value



############################################################
# MAIN
############################################################

# pyHTTPCache Resource class
class Resource(object):


	def __init__(self, url=None):
		self.url = url
		
		# temporarily hardcoded
		self.fs_root = '/tmp/pyHTTPCache'


	@LazyProperty
	def md5(self):
		return hashlib.md5(self.url).hexdigest()


	@LazyProperty
	def path(self):
		return "/".join([self.fs_root, self.md5])


	def _cache_check(self):
		pass


