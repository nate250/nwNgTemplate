from abc import ABCMeta, abstractmethod
import re, os
import sublime, sublime_plugin

class AbstractNamespacedTemplateCommand(sublime_plugin.WindowCommand):
    __metaclass__ = ABCMeta

	def __init__(self, window):
		super(AbstractNamespacedTemplateCommand, self).__init__(window)
		self.save_namespace_path_aliases()

	def run(self, paths=None):
		if paths is None:
			paths = [self.window.active_view().file_name()]
		if len(paths) != 1:
			return
		if os.path.isdir(paths[0]):
			self.path = paths[0]
		else:
			self.path = os.path.dirname(paths[0])
		
		self.save_namespace_path_aliases()
		self.view = self.window.active_view()

		current_namespace = self.path_to_namespace(self.path)
		self.show_filename_input(current_module, self.on_done)

	def on_done(self, input_string):
		namespace,component = self.isolate_component_name(input_string)
		path = self.namespace_to_path(namespace)
		files = self.component_to_files(component)

		self.create_folder(path)

		create_files(path, files, true)

	def create_folder(self, path):
		init_list = []
		temp_path = path
		while not os.path.exists(temp_path):
			init_list.append(temp_path)
			temp_path = os.path.dirname(temp_path)
		try:
			if not os.path.exists(path):
				os.makedirs(path)
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				raise

		for entry in init_list:
			init_files = self.get_namespace_base_files(self.path_to_namespace(entry))
			self.create_files(entry, init_files, false)

	def create_and_open_file(self, filepath, content=""):
		self.create_file(filepath, content)
		self.window.open_file(filepath)

	def create_file(self, filepath, content = ""):
		if not os.path.exists(filepath):
			f = open(filepath, "w")
			f.write(content)
			f.close()

	def create_files(self, path, files, open):
		for file in files:
			full_path = os.path.join(path, file.path)
			if open:
				self.create_and_open_file(full_path, file.content)
			else:
				self.create_file(full_path, file.content)


	def show_filename_input(self, initial, then):
		self.input_panel_view = self.window.show_input_panel(
			"Directive Name: ", initial,
			then, None, None
		)

	def get_project_folder(self):
		return self.window.folders()[0]

	def get_settings(self):
		return self.window.project_data()["nw_ng_templates"]

	def save_namespace_path_aliases(self):
		aliases = {}
		self.namespace_aliases = {}
		self.path_aliases = {}
		for directory, module in self.get_settings()["module_aliases"].items():
			aliases[os.path.normpath(os.path.join(self.open_folder, directory))] = module
		alias_keys = sorted(aliases, key=lambda key: len(key))

		for directory in alias_keys:
			module = aliases[directory]
			if module.startswith("."):
				pathUp, name = os.path.split(directory)
				self.path_aliases[directory] = aliases[pathUp] + module
			else:
				self.path_aliases[directory] = module
			self.namespace_aliases[self.path_aliases[directory]] = directory

	def path_to_namespace(self, path):
		path_pieces = path.split(os.sep)
		paths_left = []

		while(len(path_pieces) > 0):
			path = os.sep.join(path_pieces)

			if path in self.path_aliases:
				return self.join_namespaces([self.path_aliases[path]] + paths_left)

			paths_left.insert(0,path_pieces.pop())

		return self.join_namespaces(path.replace(self.get_project_folder() + os.sep,"").split(os.sep))

	def namespace_to_path(self, namespace):
		namespaces = split_namespace(namespace)
		namespaces_left = []
		
		while (len(namespaces) > 0):
			namespace = ".".join(namespaces)

			if namespace in self.namespace_aliases:
				return os.path.join(self.namespace_aliases[namespace], os.sep.join(namespaces_left))

			namespaces_left.insert(0,namespaces.pop())
		
		return os.path.join(self.get_project_folder(), os.sep.join(namespaces_left))

    @abstractmethod
    def split_namespace(self, namespace):
        pass

    @abstractmethod
    def join_namespaces(self, namespaces):
    	pass

    @abstractmethod
    def isolate_component_name(self, namespace):
    	pass

    @abstractmethod
    def component_to_files(self, component):
    	pass

    @abstractmethod
    def get_namespace_base_files(self, namespace):
    	pass