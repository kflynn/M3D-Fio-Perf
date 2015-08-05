import sys

import json
import logging

logging.basicConfig()

sys.path.append("../M3D-Fio")

from octoprint_m3dfio import M3DFioPlugin

class dummyPluginManager (object):
	def __init__(self, logger):
		self._logger = logger

	def send_plugin_message(self, plugin, data):
		dataStr = json.dumps(data, indent=4, separators=(',',':'), sort_keys=True)
		# self._logger.info("%s -- %s" % (plugin, dataStr))

class dummyFileObj (object):
    def __init__(self, path):
        self.path = path
        self.fileObj = open(path, "r")

    def stream(self):
        return self.fileObj

class dummySettings (object):
	def __init__(self, pluginObj):
		self._settings = pluginObj.get_settings_defaults()

	def get(self, keys):
		return self._settings.get(keys[0], None)

	def get_float(self, keys):
		return float(self._settings.get(keys[0], 0.0))

	def get_int(self, keys):
		return int(self._settings.get(keys[0], 0))

	def get_boolean(self, keys):
		return bool(self._settings.get(keys[0], False))

m3d = M3DFioPlugin()
m3d._logger = logging.getLogger("M3D")
m3d._logger.setLevel(logging.DEBUG)

m3d._plugin_manager = dummyPluginManager(m3d._logger)
m3d._identifier = "M3D-Fio"

m3d._settings = dummySettings(m3d)

inputObj = dummyFileObj(sys.argv[1])

result = m3d.preprocessesGcode(inputObj.path, inputObj,
                               links = None, printer_profile = None, allow_overwrite = True)

print(result)

