# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_railway', 'git_railway.resources', 'git_railway.view']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.8,<4.0.0',
 'colour>=0.1.5,<0.2.0',
 'dataclasses',
 'importlib_resources>=3.1.1,<4.0.0',
 'svgwrite>=1.4,<2.0']

entry_points = \
{'console_scripts': ['git-railway = git_railway.__main__:main']}

setup_kwargs = {
    'name': 'git-railway',
    'version': '0.3.0',
    'description': 'Visualise local git branches as neat interactive HTML pages',
    'long_description': '<h1 align="center">Git Railway</h1>\n\n<h3 align="center">Visualise local git branches as neat interactive HTML pages</h3>\n\n<p align="center">\n  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/Tux_Mono.svg"\n       height="24px" />\n  &nbsp;&nbsp;&nbsp;&nbsp;\n  <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"\n       height="24px" />\n  &nbsp;&nbsp;&nbsp;&nbsp;\n  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Windows_logo_2012-Black.svg"\n       height="24px" />\n</p>\n\n<p align="center">\n  <!-- <a href="https://github.com/P403n1x87/git-railway/actions?workflow=Tests">\n    <img src="https://github.com/P403n1x87/git-railway/workflows/Tests/badge.svg"\n         alt="GitHub Actions: Tests">\n  </a> -->\n\t<a href="https://github.com/P403n1x87/git-railway/actions?workflow=Release">\n    <img src="https://github.com/P403n1x87/git-railway/workflows/Release/badge.svg"\n         alt="GitHub Actions: Tests">\n  </a>\n  <!-- <a href="https://codecov.io/gh/P403n1x87/git-railway">\n    <img src="https://codecov.io/gh/P403n1x87/git-railway/branch/master/graph/badge.svg"\n         alt="Codecov">\n  </a> -->\n  <a href="https://pypi.org/project/git-railway/">\n    <img src="https://img.shields.io/pypi/v/git-railway.svg"\n         alt="PyPI">\n  </a>\n  <a href="https://github.com/P403n1x87/git-railway/blob/master/LICENSE.md">\n    <img src="https://img.shields.io/badge/license-GPLv3-ff69b4.svg"\n         alt="LICENSE">\n  </a>\n</p>\n\n<p align="center">\n  <!-- <a href="#synopsis"><b>Synopsis</b></a>&nbsp;&bull; -->\n  <a href="#installation"><b>Installation</b></a>&nbsp;&bull;\n  <a href="#usage"><b>Usage</b></a>&nbsp;&bull;\n  <a href="#details"><b>Details</b></a>\n\t<!-- &nbsp;&bull; -->\n  <!-- <a href="#compatibility"><b>Compatibility</b></a>&nbsp;&bull;\n  <a href="#contribute"><b>Contribute</b></a> -->\n</p>\n\n<p align="center">\n\t<img alt="Git Railway Example"\n\t     src="art/sample.png" />\n</p>\n\n# Installation\n\nGit Railway is available from PyPI\n\n~~~\npipx install git-railway\n~~~\n\n\n# Usage\n\nNavigate to a git repository, or any sub-folder, and run\n\n~~~ shell\ngit-railway\n~~~\n\nYour railway graph will be generated in `railway.html`. Use the `-o` or\n`--output` option to override the default location, e.g.\n\n~~~ shell\ngit-railway --output /tmp/mytemprailwaygraph.html\n~~~\n\n## Remote Branches\n\nIf you want to include all the remote branches to the railway graph, you can\npass the `-a` or `--all` option, e.g.\n\n~~~ shell\ngit-railway --all\n~~~\n\n## GitHub References\n\nIf the remote repository is hosted on GitHub, issue and PR\nreferences are replaced with actual links. If the GitHub slug derived from the\nremotes is wrong, you can override it with the `--gh` option, e.g.\n\n~~~ shell\ngit-railway --gh p403n1x87/git-railway\n~~~\n\n## Scaling\n\nYou can control the size of the generated railway graph by setting the scaling\nfactor with the `-s` or `--scale` option, e.g.\n\n~~~ shell\ngit-railway -s 1.5\n~~~\n\nThis will make the SVG 50% larger than normal.\n\n## Verbosity\n\nYou can also control the amount of information to include using the `-v` or\n`--verbose` option. If you switch this on, the railway graph will inline the\ncommit summary for easier navigation.\n\n~~~ shell\ngit-railway -v\n~~~\n\n<p align="center">\n\t<img alt="Git Railway Verbose Mode Example"\n\t     src="art/verbose.png" />\n</p>\n\n## Conventional Commits\n\nIf you\'re into the habit of using the [Conventional Commits] format for your\ncommit messages, the popup window that appears when you hover over a commit will\nhighlight that information for you. Additionally, commits that are marked as a\n_BREAKING CHANGE_ will have a different colour for easy identification.\n\n<p align="center">\n\t<img alt="Git Railway Breaking Change Example"\n\t     src="art/breaking_change.png" />\n</p>\n\n# Details\n\n## There\'s no such thing as *branch* in Git!\n\nAs you probably know already, a branch in git is a mere reference (or label)\nthat moves with every new commit. As such, it\'s hard if not impossible to\nreconstruct the *actual* branch from the information available from within a git\nrepository. This tools works by looking at the current local refs and collecting\nall the commits that can be reached from them. The "branches" are the\nreconstructed "best effort" by looking at the reflog to determine on which\ncommit a certain ref has been on. Sometimes this information is missing. For\nexample, when one does a merge by fast-forwarding, all the intermediate commits\nare not marked with the ref of the target branch. Should they be part of the\nbranch or not? Whenever you see a piece of grey rail in the graph, that\'s where\nthe ref information is missing.\n\n## Chrono-topological ordering\n\nTo complicate things even more, there can be cases where a parent commit has a\ntimestamp which is in the *future* with respect to some of its children. Hence,\nthe trivial chronological ordering does not always work. Furthermore, one can\nalso have precision issues; if one creates multiple commits in quick succession,\nthey are likely to end up having the same timestamp. Topological order, on the\nother hand, is not optimal either in its own. For what if we have some stale\nbranches that were never merged? They might end up at the very top of the graph,\neven though its commits are quite old.\n\nThe solution is a mix of chronological and topological sorting. For example, we\ncan start by sorting all the commits based on their timestamp, and then make\nsome changes to Kahn\'s algorithm to ensure that we position oldest commits\nfirst. With the chronological sorting step at the beginning, the complexity is\n`O(n log n)`.\n\n\n[Conventional Commits]: https://www.conventionalcommits.org',
    'author': 'Gabriele N. Tornetta',
    'author_email': 'phoenix1987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/P403n1x87/git-railway',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
