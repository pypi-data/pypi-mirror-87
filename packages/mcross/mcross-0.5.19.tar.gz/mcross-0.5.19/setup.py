# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mcross', 'mcross.gui']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'curio>=1.2,<2.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['mcross = mcross:run', 'mcross-info = mcross:info']}

setup_kwargs = {
    'name': 'mcross',
    'version': '0.5.19',
    'description': 'Do you remember www?',
    'long_description': 'McRoss is a minimal and usable [gemini://](https://gemini.circumlunar.space/)\nbrowser written in python and tkinter, meaning it Just Works (tm) on any\nself-respecting desktop OS. I use and test it on Linux & Windows, but it should\nalso run fine on macOS or any of the BSDs.\n\nIt currently looks like this:\n\n![](https://junk.imnhan.com/mcross.png)\n\nSurfing plaintext and gemini content is already working well. The catch is it\ncurrently doesn\'t support downloading binary content and TOFU TLS verification.\nSee feature checklist below for more details.\n\nSee my [blog post][1] for the rationale behind this project.\n\n\n# Installation\n\nDependencies are:\n\n+ python3.7+\n+ tkinter\n+ idlelib\n\n`idlelib` is supposed to be included in the standard library but some linux\ndistros split it into a separate package which you\'ll need to install manually.\nI know at least [Ubuntu and Void Linux][2] do this.\n\n## On Ubuntu:\n\n```sh\nsudo apt install python3 python3-pip python3-tk idle3\npip3 install --user mcross\n# make sure ~/.local/bin is in $PATH first of course\nmcross\n```\n\n## On Arch:\n\n```sh\nsudo pacman -S python tk\npip install --user mcross\n```\n\nAlso consider using [pipx](https://github.com/pipxproject/pipx) for a cleaner,\nbetter isolated installation.\n\nBetter distribution methods to be explored later.\nMaybe it\'s finally time to try nuitka?\n\n# Usage\n\nRun `mcross -h` to get a full list of CLI arguments. The same arguments can\nalso be defined in a TOML config file: run `mcross-info` to know where this\nfile should be for your OS. For example, running mcross like this:\n\n```sh\nmcross --background-color pink -t "Ubuntu"\n```\n\nis the same as putting this in `$HOME/.config/mcross/mcross.toml` for linux:\n\n```toml\nbackground-color = "pink"\ntext-font = "Ubuntu"\n```\n\nThe priority is CLI arg > config file > default.\n\nKeyboard shortcuts:\n\n- `Ctrl-l`: jump to address bar.\n- Hold `Alt` to see possible button shortcuts underlined. This is what Qt calls\n  [Accelerator Keys](https://doc.qt.io/qt-5/accelerators.html).\n\n\n# Development\n\nTo get started:\n\n```sh\npyenv install 3.7.7\npyenv virtualenv 3.7.7 mcross\npyenv activate\npoetry install\nmcross\n\n# to publish, first bump version in pyproject.toml then\npoetry publish --build\n```\n\nThere are 2 McRoss-related mailing lists:\n\n- [~nhanb/mcross-devel](https://lists.sr.ht/~nhanb/mcross-devel): discuss and\n  submit your patches here\n- [~nhanb/mcross-announce](https://lists.sr.ht/~nhanb/mcross-announce):\n  low-volume announcement-only list\n\nIf you\'re not familiar with the mailing list workflow, check out\n[git-send-email.io][3] and [mailing list etiquette][4]. [useplaintext.email][5]\nalso has useful plaintext setup tips for various email clients, though I don\'t\nnecessarily agree with its "plaintext or nothing" stance.\n\n\n# Feature checklist\n\n- [x] back-forward buttons\n- [x] handle redirects\n- [x] non-blocking I/O using curio\n- [x] more visual indicators: waiting cursor, status bar\n- [x] parse gemini\'s advanced line types\n- [x] render `text/*` mime types with correct charset\n- [ ] handle `binary/*` mime types\n- [x] configurable document styling\n- [ ] human-friendly distribution\n- [ ] TOFU TLS (right now it always accepts self-signed certs)\n\nLong term high-level goals:\n\n## Easy for end users to install\n\nIf the words `cargo build` exists in the installation guide for your G U I\napplication then I\'m sorry it\'s not software made for people to _use_.\n\n## What-you-see-is-what-you-write\n\nA rendered text/gemini viewport should preserve its original text content.\nThis way once you\'ve read a gemini page on the browser, you already know how to\nwrite one. No "View Source" necessary.\n\n## Responsive & pleasant to use\n\nThe Castor browser doesn\'t have visual indicators at all, for example, when\nclicking on a link it just appears to do nothing until the new page is\ncompletely loaded. That is A Bad Thing (tm).\n\n## Lightweight\n\nIn terms of both disk space & memory/cpu usage.\nThe python/tkinter combo already puts us at a pretty good starting point.\n\n# Server bugs/surprises\n\n## Forces gemini:// in request\n\nSpec says protocol part is optional, but if I omit that one the server will\nrespond with `53 No proxying to other hosts!`.\n\n## Newline\n\nSpec says a newline should be \\r\\n but the server running\ngemini.circumlunar.space just uses \\n every time.\n\n# License\n\nCopyright (C) 2020 Bùi Thành Nhân\n\nThis program is free software: you can redistribute it and/or modify it under\nthe terms of the GNU Affero General Public License version 3 as published by\nthe Free Software Foundation.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\nPARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nthis program.  If not, see <https://www.gnu.org/licenses/>.\n\n# Forks\n\nMcRoss development is... conservative and sporadic.\nIf that bothers you, check out [picross][6] which is a nice fork with more\nfeatures (TOFU, tabs, among other things).\n\n[1]: https://hi.imnhan.com/posts/introducing-mcross-a-minimal-gemini-browser/\n[2]: https://todo.sr.ht/~nhanb/mcross/3\n[3]: https://git-send-email.io/\n[4]: https://man.sr.ht/lists.sr.ht/etiquette.md\n[5]: https://useplaintext.email/\n[6]: https://git.sr.ht/~fkfd/picross\n[7]: https://docs.python.org/3.8/library/tkinter.html#file-handlers\n',
    'author': 'nhanb',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~nhanb/mcross/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
