# Angular Template Sublime Plugin
Adds support to Sublime for generating files for new Angular components. It will create:
* Module files
* Test module files
* Directive files
* Directive test files
* Directive templates
* Directive stylesheets

Exposes the ctrl+shift+g keybinding with the following additional sequences:
* d - For making new directives

Requires a sublime-project file containing the following:

    "nw_ng_templates": {
	  "module_aliases": {
	    "./testLib": ".lib",
	    ".": "app",
	    "./testSdk": "sdk"
	   }
	  }
