import re, os
import sublime, sublime_plugin

class NwNewAngularDirectiveCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		super(NwNewAngularDirectiveCommand, self).__init__(window)

	def run(self, paths):
		if len(paths) != 1:
			return
		notOsSep = "[^\\" + os.sep + "]+"
		self.path = re.sub("(" + notOsSep + "\\.)+" + notOsSep + "$", "", paths[0])
		if not self.path.endswith(os.sep):
			self.path = self.path + os.sep
		self.view = self.window.active_view()
		self.open_folder = self.window.folders()[0]

		self.show_filename_input(self.extrapolate_module(self.open_folder + os.sep,self.path))

	def show_filename_input(self, initial):
		self.input_panel_view = self.window.show_input_panel(
			"Directive Name: ", initial,
			self.on_done, None, None
		)

	def extrapolate_module(self, open_folder, selected_path):
		return selected_path.replace(open_folder,"").replace(os.sep,".")

	def on_done(self, input_string):
		path, filestub = input_string.rsplit(".",1)
		path = os.path.join(self.open_folder, path.replace(".",os.sep))
		filename = filestub + ".directive"

		self.create_folder(path)
		print(os.path.join(path,filename + ".js"))
		self.create_file(os.path.join(path,filename + ".js"), 'ng-directive')
		self.create_file(os.path.join(path,filename + ".spec.js"), 'ng-directive-spec')
		self.create_file(os.path.join(path,filename + ".scss"))
		self.create_file(os.path.join(path,filename + ".html"))

	def create_file(self, filepath, content = ""):
		if not os.path.exists(filepath):
			f = open(filepath, "w")
			f.write(content)
			f.close()

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
			self.create_file(os.path.join(entry, 'module.js'), 'ng-module')
			self.create_file(os.path.join(entry, 'module.spec.js'), 'ng-module-spec')
