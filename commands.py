import re, os
import sublime, sublime_plugin

class NwNewAngularDirectiveCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		super(NwNewAngularDirectiveCommand, self).__init__(window)
		self.open_folder = self.get_open_folder()
		self.load_aliases()

	def run(self, paths=None):
		if paths is None:
			paths = [self.window.active_view().file_name()]
		if len(paths) != 1:
			return
		if os.path.isdir(paths[0]):
			self.path = paths[0]
		else:
			self.path = os.path.dirname(paths[0])

		
		self.view = self.window.active_view()
		self.open_folder = self.window.folders()[0]
		module = self.lookup_module(self.path)
		self.show_filename_input(module)

	def show_filename_input(self, initial):
		self.input_panel_view = self.window.show_input_panel(
			"Directive Name: ", initial,
			self.on_done, None, None
		)

	def extrapolate_module(self, selected_path):
		return selected_path.replace(self.open_folder + os.sep,"").replace(os.sep,".")

	def extrapolate_path(self, module):
		return os.path.join(self.open_folder, self.module_to_path(module))

	def module_to_path(self, module):
		return module.replace(".",os.sep)

	def on_done(self, input_string):
		module,directive = input_string.rsplit(".",1)
		path, filestub = os.path.split(self.lookup_path(input_string))
		filename = filestub + ".directive"

		self.create_folder(path)
		fullpath = os.path.join(path, filename)
		self.create_module_files(path, self.lookup_module(path))
		self.create_file(fullpath + ".js", self.get_directive_content(module,directive))
		self.create_file(fullpath + ".spec.js", self.get_directive_spec_content(module,directive))
		self.create_file(fullpath + ".scss")
		self.create_file(fullpath + ".html")

	def create_file(self, filepath, content = ""):
		if not os.path.exists(filepath):
			f = open(filepath, "w")
			f.write(content)
			f.close()

	def create_module_files(self, path, module):
		self.create_file(os.path.join(path, 'module.js'), self.get_module_content(module))
		self.create_file(os.path.join(path, 'module.spec.js'), self.get_module_spec_content(module))

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
			self.create_module_files(entry, self.lookup_module(entry))

	def get_open_folder(self):
		return self.window.folders()[0]

	def lookup_module(self, path):
		path_pieces = path.split(os.sep)
		paths_left = []

		while(len(path_pieces) > 0):
			path = os.sep.join(path_pieces)

			if path in self.aliases:
				return self.aliases[path] + "." + ".".join(paths_left)

			paths_left.insert(0,path_pieces.pop())

		return self.extrapolate_module(path)

	def lookup_path(self, module):
		module_pieces = module.split(".")
		modules_left = []
		
		while (len(module_pieces) > 0):
			module = ".".join(module_pieces)

			if module in self.aliases_by_module:
				return os.path.join(self.aliases_by_module[module], self.module_to_path(".".join(modules_left)))

			modules_left.insert(0,module_pieces.pop())
		
		return self.extrapolate_path(".".join(modules_left))

	def load_aliases(self):
		aliases = {}
		self.aliases = {}
		self.aliases_by_module = {}
		for directory, module in self.window.project_data()["nw_ng_templates"]["module_aliases"].items():
			aliases[os.path.normpath(os.path.join(self.open_folder, directory))] = module
		alias_keys = sorted(aliases, key=lambda key: len(key))

		for directory in alias_keys:
			module = aliases[directory]
			if module.startswith("."):
				pathUp, name = os.path.split(directory)
				self.aliases[directory] = aliases[pathUp] + module
			else:
				self.aliases[directory] = module
			self.aliases_by_module[self.aliases[directory]] = directory

	def get_module_content(self, module):
		return '''\
(function() {{
  'use strict';

  angular.module('{module}',[
    
  ]);
}})();
'''.format(module=module)

	def get_directive_content(self, module, directive):
		return '''\
(function() {{
  'use strict';

  angular
    .module('{module}')
    .directive('{directive}', directive);

  directive.$inject = [];
  function directive() {{
    return {{
      restrict: 'E',
      replace: true,
      bindToController: true,
      controllerAs: 'directive',
      controller: Controller
    }};
  }}

  Controller.$inject = [];
  function Controller() {{

  }}
}})();
'''.format(module=module,directive=directive)

	def get_directive_spec_content(self, module, directive):
		return '''\
describe('DIRECTIVE: {directive}', function() {{
  beforeEach(module());

  var $compile, element, $scope;

  beforeEach(inject(function(_$compile_, $rootScope) {{
    $compile = _$compile_;
    $scope = $rootScope.$new();
  }}));
}});
'''.format(module=module,directive=directive)

	def get_module_spec_content(self, module):
		return '''\
(function() {{
  'use strict';

  angular.module('{module}.test', [
    '{module}',
    
  ]);
}})();
'''.format(module=module)