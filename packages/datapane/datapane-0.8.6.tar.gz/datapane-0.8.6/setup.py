# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.scripts',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.templates',
 'datapane.resources.templates.report_py',
 'datapane.resources.templates.script',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.templates': ['report_ipynb/*']}

install_requires = \
['PyYAML>=5.1.0,<6.0.0',
 'altair>=4.0.0,<5.0.0',
 'bokeh==2.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.0.0,<8.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'dacite>=1.2.0,<2.0.0',
 'flit-core>=3.0.0,<3.1.0',
 'folium>=0.11.0,<0.12.0',
 'furl>=2.1.0,<3.0.0',
 'importlib_resources>=3.0.0,<4.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'lxml>=4.5.2,<5.0.0',
 'matplotlib>=3.1.0,<4.0.0',
 'munch>=2.5.0,<3.0.0',
 'nbconvert>=6.0.0,<6.1.0',
 'numpy>=1.18.0,<2.0.0',
 'packaging>=20.3,<21.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.20.0,<3.0.0',
 'ruamel.yaml>=0.16.5,<0.17.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toolz>=0.11.1,<0.12.0',
 'validators>=0.18.0,<0.19.0']

extras_require = \
{':python_version >= "3.6.1" and python_version < "3.7.0"': ['dataclasses==0.7']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.8.6',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n    <a href="https://datapane.com">Datapane.com</a> |\n    <a href="https://docs.datapane.com">Documentation</a> |\n    <a href="https://twitter.com/datapaneapp">Twitter</a>\n    <br /><br />\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n    </a>\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n    </a>\n    <a href="https://anaconda.org/conda-forge/datapane">\n        <img src="https://anaconda.org/conda-forge/datapane/badges/version.svg" alt="Latest release" />\n    </a>\n    <img src="https://github.com/datapane/datapane-hosted/workflows/Test%20%5BDP%20CLI%5D/badge.svg" alt="Latest release" />\n</p>\n\nDatapane is a Python library which makes it simple to build reports from the common objects in your data analysis, such as pandas DataFrames, plots from Python visualisation libraries, and Markdown.\n\nReports can be exported as standalone HTML documents, with rich components which allow data to be explored and visualisations to be used interactively.\n\nFor example, if you wanted to create a report with a table viewer and an interactive plot:\n\n```python\nimport pandas as pd\nimport altair as alt\nimport datapane as dp\n\ndf = pd.read_csv(\'https://query1.finance.yahoo.com/v7/finance/download/GOOG?period2=1585222905&interval=1mo&events=history\')\n\nchart = alt.Chart(df).encode(\n    x=\'Date:T\',\n    y=\'Open\'\n).mark_line().interactive()\n\nr = dp.Report(dp.Table(df), dp.Plot(chart))\nr.save(path=\'report.html\', open=True)\n```\n\nThis would package a standalone HTML report such as the following, with an searchable Table and Plot component.\n\n![Report Example](https://i.imgur.com/RGp7RzM.png)\n\n# Getting Started\n\n- [Read the documentation](https://docs.datapane.com)\n- [View samples and demos](https://github.com/datapane/datapane-demos/)\n\n# Components\n\nDatapane currently contains the following components. Need something different? Open an issue (or make a PR!)\n\n| Component | Description                                                                    | Supported Formats                                  | Example                      |\n| --------- | ------------------------------------------------------------------------------ | -------------------------------------------------- | ---------------------------- |\n| Table     | A searchable, sortable table component for datasets. Supports up to 10m cells. | Pandas DataFrames, JSON documents, Local CSV files | `Table(df)`                  |\n| Plot      | A wrapper for plots from Python visualisation libraries.                       | Altair, Bokeh, Matplotlib, SVG                     | `Plot(altair_chart)`         |\n| Markdown  | A simple Markdown component to document your report.                           | Markdown, Text                                     | `Markdown("# My fun title")` |\n\n# Datapane.com\n\nIn addition to the this local library, Datapane.com provides an API and hosted platform which allows you to:\n\n1. Upload Jupyter Notebooks and Python scripts, so that other people can run them in their browser with parameters to generate reports dynamically\n1. Share and embed reports online -- either publicly, or privately within your team\n\n# Joining the community\n\nLooking to get answers to questions or engage with us and the wider community? Our community is most active on our Discourse Forum. Submit requests, issues, and bug reports on this GitHub repo, or join us by contributing on some good first issues on this repo.\n\nWe look forward to building an amazing open source community with you!\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
