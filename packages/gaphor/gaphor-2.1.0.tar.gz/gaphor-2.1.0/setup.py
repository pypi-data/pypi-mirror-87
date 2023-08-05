# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaphor',
 'gaphor.SysML',
 'gaphor.SysML.blocks',
 'gaphor.SysML.blocks.tests',
 'gaphor.SysML.requirements',
 'gaphor.SysML.requirements.tests',
 'gaphor.SysML.tests',
 'gaphor.UML',
 'gaphor.UML.actions',
 'gaphor.UML.actions.tests',
 'gaphor.UML.classes',
 'gaphor.UML.classes.tests',
 'gaphor.UML.components',
 'gaphor.UML.components.tests',
 'gaphor.UML.interactions',
 'gaphor.UML.interactions.tests',
 'gaphor.UML.profiles',
 'gaphor.UML.profiles.tests',
 'gaphor.UML.states',
 'gaphor.UML.states.tests',
 'gaphor.UML.tests',
 'gaphor.UML.usecases',
 'gaphor.UML.usecases.tests',
 'gaphor.codegen',
 'gaphor.codegen.tests',
 'gaphor.core',
 'gaphor.core.modeling',
 'gaphor.core.modeling.tests',
 'gaphor.core.styling',
 'gaphor.core.styling.tests',
 'gaphor.diagram',
 'gaphor.diagram.general',
 'gaphor.diagram.general.tests',
 'gaphor.diagram.tests',
 'gaphor.plugins',
 'gaphor.plugins.console',
 'gaphor.plugins.console.tests',
 'gaphor.plugins.diagramexport',
 'gaphor.plugins.diagramexport.tests',
 'gaphor.plugins.xmiexport',
 'gaphor.plugins.xmiexport.tests',
 'gaphor.services',
 'gaphor.services.helpservice',
 'gaphor.services.tests',
 'gaphor.storage',
 'gaphor.storage.tests',
 'gaphor.tests',
 'gaphor.ui',
 'gaphor.ui.tests']

package_data = \
{'': ['*'],
 'gaphor': ['locale/*'],
 'gaphor.ui': ['icons/*', 'icons/hicolor/scalable/actions/*']}

install_requires = \
['PyGObject>=3.30,<4.0',
 'gaphas>=2.1.1,<3.0.0',
 'generic>=1.0.0,<2.0.0',
 'importlib_metadata>=1.4,<2.0',
 'pycairo>=1.18,<2.0',
 'tinycss2>=1.0.2,<2.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['gaphor = gaphor.ui:main',
                     'gaphorconvert = '
                     'gaphor.plugins.diagramexport.gaphorconvert:main'],
 'gaphor.appservices': ['app_file_manager = '
                        'gaphor.ui.appfilemanager:AppFileManager',
                        'event_manager = gaphor.core.eventmanager:EventManager',
                        'help = gaphor.services.helpservice:HelpService',
                        'session = gaphor.services.session:Session'],
 'gaphor.modelinglanguages': ['SysML = '
                              'gaphor.SysML.modelinglanguage:SysMLModelingLanguage',
                              'UML = '
                              'gaphor.UML.modelinglanguage:UMLModelingLanguage'],
 'gaphor.services': ['component_registry = '
                     'gaphor.services.componentregistry:ComponentRegistry',
                     'consolewindow = gaphor.plugins.console:ConsoleWindow',
                     'copy = gaphor.services.copyservice:CopyService',
                     'diagram_export = '
                     'gaphor.plugins.diagramexport:DiagramExport',
                     'diagrams = gaphor.ui.diagrams:Diagrams',
                     'element_dispatcher = '
                     'gaphor.core.modeling.elementdispatcher:ElementDispatcher',
                     'element_factory = gaphor.core.modeling:ElementFactory',
                     'elementeditor = gaphor.ui.elementeditor:ElementEditor',
                     'event_manager = gaphor.core.eventmanager:EventManager',
                     'export_menu = gaphor.ui.menufragment:MenuFragment',
                     'file_manager = gaphor.ui.filemanager:FileManager',
                     'main_window = gaphor.ui.mainwindow:MainWindow',
                     'modeling_language = '
                     'gaphor.services.modelinglanguage:ModelingLanguageService',
                     'namespace = gaphor.ui.namespace:Namespace',
                     'properties = gaphor.services.properties:Properties',
                     'recent_files = gaphor.ui.recentfiles:RecentFiles',
                     'sanitizer = gaphor.UML.sanitizerservice:SanitizerService',
                     'toolbox = gaphor.ui.toolbox:Toolbox',
                     'tools_menu = gaphor.ui.menufragment:MenuFragment',
                     'undo_manager = gaphor.services.undomanager:UndoManager',
                     'xmi_export = gaphor.plugins.xmiexport:XMIExport']}

setup_kwargs = {
    'name': 'gaphor',
    'version': '2.1.0',
    'description': 'Gaphor is the simple modeling tool written in Python.',
    'long_description': '<div align="center"><img src="https://github.com/gaphor/gaphor/blob/2.0.0/logos/org.gaphor.Gaphor.svg" alt="Gaphor logo" width="64" /></div>\n<h1 align="center">Gaphor</h1>\n\n[![Build state](https://github.com/gaphor/gaphor/workflows/Build/badge.svg)](https://github.com/gaphor/gaphor/actions)\n[![Docs build state](https://readthedocs.org/projects/gaphor/badge/?version=latest)](https://gaphor.readthedocs.io)\n[![PyPI](https://img.shields.io/pypi/v/gaphor.svg)](https://pypi.org/project/gaphor)\n[![Downloads](https://pepy.tech/badge/gaphor)](https://pepy.tech/project/gaphor)\n[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Gaphor/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/f00974f5d7fe69fe4ecd/maintainability)](https://codeclimate.com/github/gaphor/gaphor/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/f00974f5d7fe69fe4ecd/test_coverage)](https://codeclimate.com/github/gaphor/gaphor/test_coverage)\n[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)\n[![All Contributors](https://img.shields.io/badge/all_contributors-32-brightgreen.svg)](#contributors)\n\n\nGaphor is a UML and SysML modeling application written in Python.\nIt is designed to be easy to use, while still being powerful. Gaphor implements a fully-compliant UML 2 data model, so it is much more than a picture drawing tool. You can use Gaphor to quickly visualize different aspects of a system as well as create complete, highly complex models.\n\n<div align="center">\n<br/>\n<img src="https://github.com/gaphor/gaphor/blob/2.0.0/docs/images/gaphor-demo.gif" width="75%">\n<br/><br/>\n</div>\n\n## :bookmark_tabs: Table of Contents\n\n- [Background](#background)\n- [Install](#floppy_disk-install)\n- [Usage](#usage)\n- [Contributing](#contributing)\n- [License](#license)\n\n## :scroll: Background\n\nGaphor is a UML and SysML modeling application written in Python. We designed\nit to be easy to use, while still being powerful. Gaphor implements a\nfully-compliant UML 2 data model, so it is much more than a picture drawing\ntool. You can use Gaphor to quickly visualize different aspects of a system as\nwell as create complete, highly complex models.\n\nGaphor is designed around the following principles:\n\n- Simplicity: The application should be easy to use. Only some basic knowledge of UML or SysML is required.\n- Consistency: UML is a graphical modeling language, so all modeling is done in a diagram.\n- Workability: The application should not bother the user every time they do something non-UML-ish.\n\nGaphor is a GUI application that is built on\n[GTK](https://gtk.org) and [Cairo](https://www.cairographics.org/). [PyGObject](https://pygobject.readthedocs.io/) and [PyCairo](https://pycairo.readthedocs.io/) provide Python bindings for those libraries.\n[Gaphas](https://github.com/gaphor/gaphas) provides\nthe foundational diagramming functionality.\n\n## :floppy_disk: Install\n\nYou can find [the latest version](https://gaphor.org/download) on the [gaphor.org website](https://gaphor.org/download).\nGaphor ships installers for macOS and Windows. Those can be found there.\nThe Python package is also [available on PyPI](https://pypi.org/project/gaphor/).\n\nAll releases are available on\n[GitHub](https://github.com/gaphor/gaphor/releases/).\n\nIf you want to start developing on Gaphor, have a look at the [Installation section of our Tech docs](https://gaphor.readthedocs.io/en/latest/).\n\n## :flashlight: Usage\n### Creating models\n\nOnce Gaphor is started a new empty model is automatically created. The main\ndiagram is already open in the Diagram section.\n\nSelect an element you want to place, for example a Class, by clicking on the icon in\nthe Toolbox and click on the diagram. This will place a new\nClass item instance on the diagram and add a new Class to the model (it shows\nup in the Navigation). The selected tool will reset itself to\nthe Pointer tool if the option \'\'Diagram -> Reset tool\'\' is selected.\n\nSome elements are not directly visible. The section in the toolbox is collapsed\nand needs to be clicked first to reveal its contents.\n\nGaphor only has one diagram type, and it does not enforce which elements should\nbe placed on a diagram.\n\n### Create a New Diagram\n\n1. Use the Navigation to select an element that can contain a diagram (a\nPackage or Profile)\n1. Select Diagram, and New diagram. A new diagram is created.\n\n### Copy and Paste\n\nItems in a diagram can be copied and pasted in the same diagram or other\ndiagrams. Pasting places an existing item in the diagram, but the item itself\nis not duplicated. In other words, if you paste a Class object in a diagram,\nthe Class will be added to the diagram, but there will be no new Class in the\nNavigation.\n\n### Drag and Drop\n\nAdding an existing element to a diagram is done by dragging the element from\nthe Navigation section onto a diagram. Diagrams and attribute/operations of a\nClass show up in the Navigation but can not be added to a diagram.\n\nElements can also be dragged within the Navigation in order to rearrange them\nin to different packages.\n\n\n## :heart: Contributing\n\nThanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://github.com/amolenaar"><img src="https://avatars0.githubusercontent.com/u/96249?v=4" width="100px;" alt=""/><br /><sub><b>Arjan Molenaar</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=amolenaar" title="Code">💻</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Aamolenaar" title="Bug reports">🐛</a> <a href="https://github.com/gaphor/gaphor/commits?author=amolenaar" title="Documentation">📖</a> <a href="https://github.com/gaphor/gaphor/pulls?q=is%3Apr+reviewed-by%3Aamolenaar" title="Reviewed Pull Requests">👀</a> <a href="#question-amolenaar" title="Answering Questions">💬</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Aamolenaar" title="Bug reports">🐛</a> <a href="#plugin-amolenaar" title="Plugin/utility libraries">🔌</a> <a href="https://github.com/gaphor/gaphor/commits?author=amolenaar" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/wrobell"><img src="https://avatars2.githubusercontent.com/u/105664?v=4" width="100px;" alt=""/><br /><sub><b>wrobell</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=wrobell" title="Code">💻</a> <a href="https://github.com/gaphor/gaphor/commits?author=wrobell" title="Tests">⚠️</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Awrobell" title="Bug reports">🐛</a> <a href="#design-wrobell" title="Design">🎨</a></td>\n    <td align="center"><a href="https://ghuser.io/danyeaw"><img src="https://avatars1.githubusercontent.com/u/10014976?v=4" width="100px;" alt=""/><br /><sub><b>Dan Yeaw</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=danyeaw" title="Code">💻</a> <a href="https://github.com/gaphor/gaphor/commits?author=danyeaw" title="Tests">⚠️</a> <a href="https://github.com/gaphor/gaphor/commits?author=danyeaw" title="Documentation">📖</a> <a href="#platform-danyeaw" title="Packaging/porting to new platform">📦</a> <a href="#infra-danyeaw" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Adanyeaw" title="Bug reports">🐛</a> <a href="#question-danyeaw" title="Answering Questions">💬</a></td>\n    <td align="center"><a href="https://github.com/melisdogan"><img src="https://avatars2.githubusercontent.com/u/33630433?v=4" width="100px;" alt=""/><br /><sub><b>melisdogan</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=melisdogan" title="Documentation">📖</a></td>\n    <td align="center"><a href="http://www.boduch.ca"><img src="https://avatars2.githubusercontent.com/u/114619?v=4" width="100px;" alt=""/><br /><sub><b>Adam Boduch</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=adamboduch" title="Code">💻</a> <a href="https://github.com/gaphor/gaphor/commits?author=adamboduch" title="Tests">⚠️</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Aadamboduch" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/egroeper"><img src="https://avatars3.githubusercontent.com/u/535113?v=4" width="100px;" alt=""/><br /><sub><b>Enno Gröper</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=egroeper" title="Code">💻</a></td>\n    <td align="center"><a href="https://pfeifle.tech"><img src="https://avatars2.githubusercontent.com/u/23027708?v=4" width="100px;" alt=""/><br /><sub><b>JensPfeifle</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=JensPfeifle" title="Documentation">📖</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="http://www.aejh.co.uk"><img src="https://avatars1.githubusercontent.com/u/927233?v=4" width="100px;" alt=""/><br /><sub><b>Alexis Howells</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=aejh" title="Documentation">📖</a></td>\n    <td align="center"><a href="http://encolpe.wordpress.com"><img src="https://avatars1.githubusercontent.com/u/124361?v=4" width="100px;" alt=""/><br /><sub><b>Encolpe DEGOUTE</b></sub></a><br /><a href="#translation-encolpe" title="Translation">🌍</a></td>\n    <td align="center"><a href="https://github.com/choff"><img src="https://avatars1.githubusercontent.com/u/309979?v=4" width="100px;" alt=""/><br /><sub><b>Christian Hoff</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=choff" title="Code">💻</a></td>\n    <td align="center"><a href="https://oskuro.net/"><img src="https://avatars3.githubusercontent.com/u/929712?v=4" width="100px;" alt=""/><br /><sub><b>Jordi Mallach</b></sub></a><br /><a href="#translation-jmallach" title="Translation">🌍</a></td>\n    <td align="center"><a href="https://github.com/tonytheleg"><img src="https://avatars3.githubusercontent.com/u/43508092?v=4" width="100px;" alt=""/><br /><sub><b>Tony</b></sub></a><br /><a href="#maintenance-tonytheleg" title="Maintenance">🚧</a></td>\n    <td align="center"><a href="https://github.com/jischebeck"><img src="https://avatars0.githubusercontent.com/u/3011242?v=4" width="100px;" alt=""/><br /><sub><b>Jan</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Ajischebeck" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://btibert3.github.io"><img src="https://avatars2.githubusercontent.com/u/203343?v=4" width="100px;" alt=""/><br /><sub><b>Brock Tibert</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3ABtibert3" title="Bug reports">🐛</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="http://www.rmunoz.net"><img src="https://avatars2.githubusercontent.com/u/23944?v=4" width="100px;" alt=""/><br /><sub><b>Rafael Muñoz Cárdenas</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3AMenda" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/mbessonov"><img src="https://avatars2.githubusercontent.com/u/172974?v=4" width="100px;" alt=""/><br /><sub><b>Mikhail Bessonov</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Ambessonov" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://twitter.com/kapilvt"><img src="https://avatars3.githubusercontent.com/u/21650?v=4" width="100px;" alt=""/><br /><sub><b>Kapil Thangavelu</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Akapilt" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/DimShadoWWW"><img src="https://avatars2.githubusercontent.com/u/25516?v=4" width="100px;" alt=""/><br /><sub><b>DimShadoWWW</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3ADimShadoWWW" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://nedko.arnaudov.name"><img src="https://avatars2.githubusercontent.com/u/96399?v=4" width="100px;" alt=""/><br /><sub><b>Nedko Arnaudov</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Anedko" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/Alexander-Wilms"><img src="https://avatars2.githubusercontent.com/u/3226457?v=4" width="100px;" alt=""/><br /><sub><b>Alexander Wilms</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3AAlexander-Wilms" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://stevenliu216.github.io"><img src="https://avatars3.githubusercontent.com/u/1274417?v=4" width="100px;" alt=""/><br /><sub><b>Steven Liu</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Astevenliu216" title="Bug reports">🐛</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="https://github.com/ruimaciel"><img src="https://avatars3.githubusercontent.com/u/169121?v=4" width="100px;" alt=""/><br /><sub><b>Rui Maciel</b></sub></a><br /><a href="#ideas-ruimaciel" title="Ideas, Planning, & Feedback">🤔</a></td>\n    <td align="center"><a href="https://github.com/ezickler"><img src="https://avatars3.githubusercontent.com/u/3604310?v=4" width="100px;" alt=""/><br /><sub><b>Enno Zickler</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Aezickler" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/tronta"><img src="https://avatars1.githubusercontent.com/u/5135577?v=4" width="100px;" alt=""/><br /><sub><b>tronta</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Atronta" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/actionless"><img src="https://avatars1.githubusercontent.com/u/1655669?v=4" width="100px;" alt=""/><br /><sub><b>Yauhen Kirylau</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=actionless" title="Documentation">📖</a> <a href="#platform-actionless" title="Packaging/porting to new platform">📦</a> <a href="#ideas-actionless" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3Aactionless" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://www.zorinos.com"><img src="https://avatars1.githubusercontent.com/u/34811668?v=4" width="100px;" alt=""/><br /><sub><b>albanobattistella</b></sub></a><br /><a href="#translation-albanobattistella" title="Translation">🌍</a></td>\n    <td align="center"><a href="https://gavr123456789.gitlab.io/hugo-test/"><img src="https://avatars3.githubusercontent.com/u/30507409?v=4" width="100px;" alt=""/><br /><sub><b>gavr123456789</b></sub></a><br /><a href="#ideas-gavr123456789" title="Ideas, Planning, & Feedback">🤔</a></td>\n    <td align="center"><a href="https://github.com/Xander982"><img src="https://avatars2.githubusercontent.com/u/51178927?v=4" width="100px;" alt=""/><br /><sub><b>Xander982</b></sub></a><br /><a href="#content-Xander982" title="Content">🖋</a> <a href="https://github.com/gaphor/gaphor/issues?q=author%3AXander982" title="Bug reports">🐛</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="https://github.com/seryafarma"><img src="https://avatars0.githubusercontent.com/u/3274071?v=4" width="100px;" alt=""/><br /><sub><b>seryafarma</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/commits?author=seryafarma" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/dlagg"><img src="https://avatars3.githubusercontent.com/u/44321931?v=4" width="100px;" alt=""/><br /><sub><b>Jorge DLG</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Adlagg" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/abjurstrom-torch"><img src="https://avatars1.githubusercontent.com/u/62608984?v=4" width="100px;" alt=""/><br /><sub><b>Adam Bjurstrom</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Aabjurstrom-torch" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/kellenmoura"><img src="https://avatars0.githubusercontent.com/u/69016459?v=4" width="100px;" alt=""/><br /><sub><b>kellenmoura</b></sub></a><br /><a href="https://github.com/gaphor/gaphor/issues?q=author%3Akellenmoura" title="Bug reports">🐛</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-enable -->\n<!-- prettier-ignore-end -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the\n[all-contributors](https://github.com/kentcdodds/all-contributors)\nspecification. Contributions of any kind are welcome!\n\n1.  Check for open issues or open a fresh issue to start a discussion\n    around a feature idea or a bug. There is a\n    [first-timers-only](https://github.com/gaphor/gaphor/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Afirst-timers-only)\n    tag for issues that should be ideal for people who are not very\n    familiar with the codebase yet.\n2.  Fork [the repository](https://github.com/gaphor/gaphor) on\n    GitHub to start making your changes to the **master** branch (or\n    branch off of it).\n3.  Write a test which shows that the bug was fixed or that the feature\n    works as expected.\n4.  Send a pull request and bug the maintainers until it gets merged and\n    published. :smile:\n\nSee [the contributing file](CONTRIBUTING.md)!\n\n\n## :copyright: License\nCopyright (C) Arjan Molenaar and Dan Yeaw\n\nLicensed under the [Apache License v2](LICENSE.txt).\n\nSummary: You can do what you like with Gaphor, as long as you include the\nrequired notices. This permissive license contains a patent license from the\ncontributors of the code.\n',
    'author': 'Arjan J. Molenaar',
    'author_email': 'gaphor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gaphor.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
