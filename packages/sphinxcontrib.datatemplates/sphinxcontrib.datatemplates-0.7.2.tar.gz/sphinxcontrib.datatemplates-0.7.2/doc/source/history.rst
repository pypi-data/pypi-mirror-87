=================
 Release History
=================

0.7.0
=====

* add sphinx builder environment to template context
* cli: add a 'dump' subcommand
* cli: create 'render' subcommand
* treat flag options as special
* add "datatemplate" console script
* Update domain.py
* pass the entire application config to the template
* add sample for nothing
* add 3.7 and 3.8 to list of supported python versions
* add html\_context to template context
* add data loaders registry
* make directive option conversion results more intuitive
* note source-file as dependency
* pass all options to template, allow unknown options

0.6.1
=====

* pbr versioning

0.6.0
=====

* pbr is required not just for setup. See #43
* better option validators
* Use directive head (arguments) for source path
* Allow specifying template in directive body

0.5.0
=====

* Fix linting errors
* Add domain for Python Modules
* Move import to the top of the module
* Use default template manager when the builder does not have one
* Necessary method for parallel builds
* list instead of tuple
* Add option to load multiple documents from yaml
* Restore Python3.6 compat
* Add support for DBM formats
* Set \_\_version\_\_
* ensure each directive page shows how to use the template

0.4.0
=====

* clarify/expand warning about legacy directive
* add a doc page to show that the legacy form of the directive still works
* turn off -W option in sphinx build
* Wrap directives in minimal domain
* stupid copy-paste merging
* linting error
* DataTemplate from 0.3.0 as DataTemplateLegacy for compat
* method for path resolution
* Add directive "datatemplate" for backwards compat
* Update yaml.rst
* Split datatemplate directive by file type
* Ignore venv, vscode settings
* add option for encoding

0.3.0
=====

* add examples to readme
* add twine check to linter
* fix packaging metadata
* add a table to show the template input types
* clean up bad comment in travis config
* tell travis to use py3.6 and not ignore failures
* remove extra doc format builds
* remove superfluous travis command for go tools
* tell git to ignore build artifacts
* set up travis configuration
* address flake8 errors
* move dependency settings from tox to setup.cfg
* Add dialect support, better dotumentation
* Use yaml.safe\_load
* Add a little bit of documentation for XML
* Use defusedxml
* Add XML support
* Add CSV support

0.2.0
=====

* Use sphinx.util.logging for logging calls
* Fix noqa flagging of import exception
* optionally exec the conf.py file and pass settings to the template
* make test-template support python 2 and 3
* update github URL in documentation
* update the source repo URL in readme
* update to python 3.5
* add license file
* Add links to repo and docs from README and docs frontpage
* add a command line tool to make testing templates easier

0.1.0
=====

* more protection against differences in builders
* avoid errors for builders without template lookup
* add usage instructions
* add table helpers and samples
* don't force a theme setting
* remove debug print
* add JSON support
* add YAML support
* fix flake8 warnings for sphinx conf.py
* add ourself to the doc extensions we use
* basic project setup
