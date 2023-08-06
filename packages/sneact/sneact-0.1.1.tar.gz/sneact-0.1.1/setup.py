# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sneact', 'sneact.web']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sneact',
    'version': '0.1.1',
    'description': 'Sneact is a python library for building user interfaces',
    'long_description': '# Sneact\n\nSneact is a python library for building user interfaces.\n\n__That\'s so draft.__\n\n\n## Hot new features!\n\n### Conditions!\n\n```python\nfrom sneact import Sneact, s, _\nfrom sneact.cond import when, when_not, then\nfrom sneact.html import div, p\n\nscope = {\n    "ok_text": "Hello!",\n    "not_text": "Hello not!",\n    "show_text": True\n}\npage = (+Sneact(scope)\n    <<div>>_\n        @when(s.show_text, +then\n            <<p>> s.ok_text <<-p>>_\n        )\n        @when_not(s.show_text, +then\n            <<p>> s.not_text <<-p>>_\n        )\n    <<-div>>_\n)\n```\n\n##### Result:\n\n```html\n<div>\n<p>Hello!</p>\n</div>\n```\n\n### Loops!\n\n```python\nfrom sneact import Sneact, s, _\nfrom sneact.html import div, img\nfrom sneact.loop import for_each, do, item\n\nscope = {\n    "images": ["cat.png", "dog.png", "frog.png"]\n}\npage = (+Sneact(scope)\n    <<div>>_\n        @for_each(s.images, +do\n            <<img(src=item)>>_\n        )\n    <<-div>>_\n)\n```\n\n##### Result:\n\n```html\n<div>\n<img src=cat.png>\n<img src=dog.png>\n<img src=frog.png>\n</div>\n```\n\n## Example 1\n\n### Python code\n\n```python\nfrom sneact import Sneact, s, _\nfrom sneact.html import div, p, img\n\nscope = {\n    "title": "Tiger",\n    "subtitle": "About tigers",\n    "image": \'"tiger.png"\',\n}\nhome_page = (+Sneact(scope)\n    <<div>>_\n        <<p>> s.title <<-p>>_\n        <<p>> s.subtitle <<-p>>_\n        <<div>>_\n            <<p>> s.text <<-p>>_\n            <<img(src=s.image)>>_\n        <<-div>>_\n    <<-div>>_\n)\nscope["text"] = "Hello tigers. We love Tigers."\nresult = home_page.as_html()\n```\n\n### Resulting html\n\n```html\n<div>\n<p>Tiger</p>\n<p>About tigers</p>\n<div>\n<p>Hello tigers. We love Tigers.</p>\n<img src="tiger.png">\n</div>\n</div>\n```\n\n[Pytest code link](https://github.com/machineandme/sneact/blob/df9c3c47a6da3d219724240ca298d2240274ac0c/tests/test_sneact.py#L11)\n\n## Example 2\n\n\n### Python code\n\n```python\nfrom sneact import Sneact, s, _\nfrom sneact.html import p, h1, header, footer\n\nscope = {}\npage = (+Sneact(scope)\n    <<header>>_\n    \t**s.header\n    <<-header>>_\n    <<p>> "Lorem you know" <<-p>>_\n    <<footer>>_\n    \t**s.footer\n    <<-footer>>_\n)\nscope["header"] = (+Sneact(scope)\n    <<h1>> "Page" <<-h1>>_\n)\nscope["footer"] = (+Sneact(scope)\n    <<p>> "Copyright Kiselev Nikolay 2020" <<-p>>_\n)\nresult = page.as_html()\n```\n\n### Resulting html\n\n```html\n<header>\n<h1>Page</h1>\n</header>\n<p>Lorem you know</p>\n<footer>\n<p>Copyright Kiselev Nikolay 2020</p>\n</footer>\n```\n\n[Pytest code link](https://github.com/machineandme/sneact/blob/df9c3c47a6da3d219724240ca298d2240274ac0c/tests/test_sneact.py#L49)\n',
    'author': 'Kiselev Nikolay',
    'author_email': 'ceo@machineand.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://machineand.me/sneact?f=pypi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
