# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.0.0,<2.0.0',
 'diot',
 'enlighten>=1.0.0,<2.0.0',
 'liquidpy',
 'more-itertools>=8.0.0,<9.0.0',
 'pandas>=1.0.0,<2.0.0',
 'pipda',
 'pyparam',
 'python-simpleconf',
 'python-slugify>=4.0.0,<5.0.0',
 'rich>=9.0.0,<10.0.0',
 'simplug',
 'toml>=0.10,<0.11',
 'uvloop<1.0.0',
 'varname',
 'xqute']

entry_points = \
{'console_scripts': ['pipen = pipen.cli:main']}

setup_kwargs = {
    'name': 'pipen',
    'version': '0.0.2',
    'description': 'A pipeline framework for python',
    'long_description': '# pipen - A pipeline framework for python\n<!--\n[![Pypi][1]][2] [![Github][3]][4] [![PythonVers][5]][2] [![docs][6]][7] [![building][8]][7] [![Codacy][9]][10] [![Codacy coverage][11]][10]\n\n[Documentation][7] | [API][11] | [Change log][12]\n-->\n\n\n## Installation\n```bash\npip install -U pipen\n```\n\n## Quickstart\n`example.py`\n```python\nfrom pipen import Proc, Pipen\n\nclass Subset(Proc):\n    """Subset the input data using pandas"""\n    input_keys = \'datafile\'\n    input = [\'https://raw.githubusercontent.com/tidyverse/ggplot2/master/data-raw/mpg.csv\']\n    output = \'outfile:file:mpg-subset.csv\'\n    lang = \'python\'\n    script = """\n        import pandas\n        data = pandas.read_csv(\'{{in.datafile}}\')\n        data = data[[\'model\', \'displ\']]\n        data.to_csv(\'{{out.outfile}}\')\n    """\n\nclass Plot(Proc):\n    """Plot the data with ggplot2 in R"""\n    requires = Subset\n    input_keys = \'datafile:file\'\n    output = \'plotfile:file:mpg.png\'\n    lang = \'Rscript\'\n    script = """\n        library(ggplot2)\n        data = read.csv(\'{{in.datafile}}\')\n        png(\'{{out.plotfile}}\')\n        ggplot(data) + geom_boxplot(aes(x=model, y=displ)) +\n            theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))\n        dev.off()\n    """\n\nif __name__ == \'__main__\':\n    pipen = Pipen(name=\'plot-mpg\', starts=Subset)\n    pipen.run()\n```\n\n```shell\n$ python example.py\n```\n\n![example](example/example.png)\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pipen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
