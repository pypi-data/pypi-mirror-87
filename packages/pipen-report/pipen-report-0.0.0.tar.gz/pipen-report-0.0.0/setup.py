# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_report']

package_data = \
{'': ['*']}

install_requires = \
['liquidpy', 'pipen', 'python-slugify>=4.0.0,<5.0.0']

entry_points = \
{'pipen': ['report = pipen_report:PipenReportPlugin']}

setup_kwargs = {
    'name': 'pipen-report',
    'version': '0.0.0',
    'description': 'Report generation system for pipen.',
    'long_description': "# pipen-verbose\n\nAdd verbosal information in logs for [pipen][1].\n\n## Usage\n```python\nfrom pipen import Proc, Pipen\n\nclass Process(Proc):\n    input_keys = 'a'\n    input = range(10)\n    output = 'b:file:a.txt'\n    script = 'echo {{in.a}} > {{out.b}}'\n\nPipen(starts=Process).run()\n```\n\n```\n> python example.py\n11-04 12:00:19 I /main                _____________________________________   __\n               I /main                ___  __ \\___  _/__  __ \\__  ____/__  | / /\n               I /main                __  /_/ /__  / __  /_/ /_  __/  __   |/ /\n               I /main                _  ____/__/ /  _  ____/_  /___  _  /|  /\n               I /main                 /_/     /___/  /_/     /_____/  /_/ |_/\n               I /main\n               I /main                             version: 0.0.1\n               I /main\n               I /main    ┏━━━━━━━━━━━━━━━━━━━━━━━━━ pipeline-0 ━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n               I /main    ┃ Undescribed.                                                  ┃\n               I /main    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n               I /main    Enabled plugins: ['verbose', 'main-0.0.1']\n               I /main    Loaded processes: 1\n               I /main    Running pipeline using profile: 'default'\n               I /main    Output will be saved to: './pipeline-0-output'\n               I /main\n               I /main    ╭─────────────────── default configurations ────────────────────╮\n               I /main    │ cache            = True                                       │\n               I /main    │ dirsig           = 1                                          │\n               I /main    │ envs             = Config({})                                 │\n               I /main    │ error_strategy   = 'ignore'                                   │\n               I /main    │ forks            = 1                                          │\n               I /main    │ lang             = 'bash'                                     │\n               I /main    │ loglevel         = 'debug'                                    │\n               I /main    │ num_retries      = 3                                          │\n               I /main    │ plugin_opts      = Config({})                                 │\n               I /main    │ plugins          = None                                       │\n               I /main    │ scheduler        = 'local'                                    │\n               I /main    │ scheduler_opts   = Config({})                                 │\n               I /main    │ submission_batch = 8                                          │\n               I /main    │ template         = 'liquid'                                   │\n               I /main    │ workdir          = './.pipen'                                 │\n               I /main    ╰───────────────────────────────────────────────────────────────╯\n               I /main\n               I /main    ╭═══════════════════════════ Process ═══════════════════════════╮\n               I /main    ║ Undescribed.                                                  ║\n               I /main    ╰═══════════════════════════════════════════════════════════════╯\n               I /main    Process: Workdir: '.pipen/process'\n               I /verbose Process: size: 10\n               I /verbose Process: [0/9] in.a: 0\n               I /verbose Process: [0/9] out.b: pipeline-0-output/Process/0/a.txt\n               I /main    Process: Cached jobs: 0-1\n               I /verbose Process: Time elapsed: 00:00:00.034s\n\npipeline-0: 100%|████████████████████████████████████████| 1/1 [00:00<00:00, 10.50 procs/s]\n```\n\n[1]: https://github.com/pwwang/pipen\n",
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pipen-report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
