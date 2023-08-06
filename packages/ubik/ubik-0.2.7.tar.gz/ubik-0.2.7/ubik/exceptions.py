# coding: utf-8

# Core
class UbikError(RuntimeError):
	""" Ubik Error """

class CoreException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class DatabaseException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class InstallerException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class ReinstallerException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class RemoverException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class UpgraderException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class ConfigException(UbikError):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)
