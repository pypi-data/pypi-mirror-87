# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymfy', 'pymfy.api', 'pymfy.api.devices']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0']

extras_require = \
{':python_version < "3.5"': ['typing>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'pymfy',
    'version': '0.9.3',
    'description': 'A Somfy Open API library',
    'long_description': '<p align=center>\n    <img src="https://developer.somfy.com/sites/default/files/img/SoOpen.png"/>\n</p>\n<p align=center>\n    <a href="https://pypi.org/project/pymfy/"><img src="https://img.shields.io/pypi/v/pymfy.svg"/></a>\n    <a href="https://github.com/tetienne/somfy-open-api/actions"><img src="https://github.com/tetienne/somfy-open-api/workflows/CI/badge.svg"/></a>\n    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/maintainability" /></a>\n    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/test_coverage" /></a>\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>\n</p>\n\nThis library is an attempt to implement the entire Somfy API in Python 3.\nDocumentation for the Somfy API can be found [here](https://developer.somfy.com/somfy-open-api/apis).\n\n\n## Get developer credentials\n\n1. Vist https://developer.somfy.com\n2. Create an account\n3. Open the *My Apps* menu\n4. Add a new App (for testing, redirect url can be anything in https)\n4. Plug in your details into the test script below.\n\n## Supported devices\nSomfy currently exposes the following type of devices:\n  - [Blinds](https://developer.somfy.com/products/blinds-interior-and-exterior)\n  - [Rolling shutters](https://developer.somfy.com/products/rolling-shutters)\n  - [Cameras](https://developer.somfy.com/products/cameras)\n  - [Connected Thermostat](https://developer.somfy.com/products/connected-thermostat)\n\nIf you find on this [page](https://developer.somfy.com/products-services-informations) devices not yet handle by this\nrepository, don\'t hesitate to open an issue.\n\n## Installation\n```\npip install pymfy\n```\n\n## Example usage\n\nPrint all covers position.\n\n```python\nimport os\nimport json\nfrom urllib.parse import urlparse, parse_qs\n\nfrom pymfy.api.devices.roller_shutter import RollerShutter\nfrom pymfy.api.somfy_api import SomfyApi\nfrom pymfy.api.devices.category import Category\n\nclient_id = r"<CLIENT_ID>"  # Consumer Key\nredir_url = "<REDIR_URL>"  # Callback URL (for testing, can be anything)\nsecret = r"<secret>"  # Consumer Secret\n\n\ndef get_token():\n    try:\n        with open(cache_path, "r") as cache:\n            return json.loads(cache.read())\n    except IOError:\n        pass\n\n\ndef set_token(token) -> None:\n    with open(cache_path, "w") as cache:\n        cache.write(json.dumps(token))\n\n\ncache_path = "/optional/cache/path"\napi = SomfyApi(client_id, secret, redir_url, token=get_token(), token_updater=set_token)\nif not os.path.isfile(cache_path):\n    authorization_url, _ = api.get_authorization_url()\n    print("Please go to {} and authorize access.".format(authorization_url))\n    authorization_response = input("Enter the full callback URL")\n    code = parse_qs(urlparse(authorization_response).query)["code"][0]\n    set_token(api.request_token(code=code))\n\ndevices = api.get_devices(category=Category.ROLLER_SHUTTER)\n\ncovers = [RollerShutter(d, api) for d in devices]\n\nfor cover in covers:\n    print(\n        "Cover {} has the following position: {}".format(\n            cover.device.name, cover.get_position()\n        )\n    )\n```\n\n## Contribute\nThe current [documentation](https://developer.somfy.com/products-services-informations) does not give enough information to implement all the devices.\nIf you want to contribute to this repository adding new devices, you can create an issue with the output of this script:\n```python\nimport json\nimport re\nfrom urllib.parse import urlparse, parse_qs\nfrom pymfy.api.somfy_api import SomfyApi\n\n\nclient_id = r"<CLIENT_ID>"  # Consumer Key\nredir_url = "<REDIR_URL>"  # Callback URL (for testing, can be anything)\nsecret = r"<secret>"  # Consumer Secret\n\napi = SomfyApi(client_id, secret, redir_url)\nauthorization_url, _ = api.get_authorization_url()\nprint("Please go to {} and authorize access.".format(authorization_url))\nauthorization_response = input("Enter the full callback URL")\ncode = parse_qs(urlparse(authorization_response).query)["code"][0]\napi.request_token(code=code)\n\nsite_ids = [s.id for s in api.get_sites()]\ndevices = [api.get("/site/" + s_id + "/device").json() for s_id in site_ids]\n\n# Remove personal information\ndumps = json.dumps(devices, sort_keys=True, indent=4, separators=(",", ": "))\ndumps = re.sub(\'".*id.*": ".*",\\n\', "", dumps)\n\nprint(dumps)\n```\n',
    'author': 'ETIENNE Thibaut',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tetienne/somfy-open-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
