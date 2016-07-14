# pyHTTPCache

import hashlib
import os
import requests
import sys


############################################################
# CONFIG
############################################################
'''
move to configuration
'''
chunk_size = 1024


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


	# generate md5 based on url
	@LazyProperty
	def md5(self):

		return hashlib.md5(self.url).hexdigest()


	# path prop based on cache root and md5 checksum of url
	@LazyProperty
	def path(self):

		return "/".join([self.fs_root, self.md5])


	# set resource in cache
	def _set_cache(self, force=False):

		if not self._cache_check() or force:
			print "CACHE SET"
			r = requests.get(self.url,stream=True)
			with open(self.path,'w') as fd:
				for chunk in r.iter_content(chunk_size):
					fd.write(chunk)


	# remove resource from cache
	def _del_cache(self, force=False):

		print "CACHE DEL"
		return os.remove(self.path)


	# check cache
	def _cache_check(self):

		return os.path.exists(self.path)


############################################################
# TESTS
############################################################
def tests():
	
	test_resources = {
		'image' : Resource(url='http://digital.library.wayne.edu/loris/fedora:wayne:vmc77431_1%7Cvmc77431_1_JP2/full/full/0/default.jpg')
	}

	# clean test area


	for k in test_resources:
		print "\n\n"
		print "#### Tests for %s type ####" % k

		# resource example
		r = test_resources[k]

		# set check cache
		print "check cache..."
		print r._cache_check()

		# download content
		print "setting cache"
		r._set_cache()

		# set re-check cache
		print "re-check cache..."
		print r._cache_check()

		# force re-set
		print "forcing re-set"
		r._set_cache(force=True)

		# del cache
		print "removing from cache"
		r._del_cache()




############################################################
# SCRIPT
############################################################
def main():

	r = Resource(url=sys.argv[1])
	print r.path


if __name__ == '__main__':
	main()