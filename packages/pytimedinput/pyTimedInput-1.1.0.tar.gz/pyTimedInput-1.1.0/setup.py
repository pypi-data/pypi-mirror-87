# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimedinput']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytimedinput',
    'version': '1.1.0',
    'description': 'Query a user for input with a timeout.',
    'long_description': 'pyTimedInput\n============\n\nDescription\n-----------\n\nA tiny, simplistic little alternative to the standard Python input()-function allowing you to specify a timeout for the function.\n\npyTimedInput should work on both Windows and Linux, though no exceedingly extensive testing has been done and there might be bugs.\n\nInstall\n-------\n\n.. code:: bash\n\n    $ pip3 install pyTimedInput\n\nUsage\n-----\n\n*timedInput()* works similar to Python\'s default *input()* - function, asking user for a string of text, but *timedInput()* allows you to also define an amount of time the user has to enter any text or how many consecutive seconds to wait for input, if the user goes idle.\n\n.. code:: python\n\n    def timedInput(prompt="", timeOut=5, forcedTimeout=False, endCharacters=[\'\\x1b\', \'\\n\', \'\\r\'])\n\nThe function *timedInput()* from *pyTimedInput* accepts the following parameters:\n\n - **prompt**, *str*: a string to show the user as a prompt when waiting for input.\n     *Defaults to an empty string.*\n - **timeout**, *int*: how many seconds to wait before timing out.\n     *Defaults to 5 seconds.*\n - **forcedTimeout**, *bool*: whether to wait for \'timeout\' many consecutive seconds of idle time or simply time out regardless of user-input.\n     *Defaults to False, ie. consecutive.*\n - **endCharacters** [], *list*: what characters to consider as end-of-input.\n     *Defaults to new-line, carrier-feed and ESC-key.*\n\nThe function returns a tuple of:\n\n - *str*: a string containing whatever the user typed, regardless of whether the function timed out or not.\n - *bool*: whether the function timed out or not.\n\n.. code:: python\n\n    from pyTimedInput import timedInput\n    userText, timedOut = timedInput("Please, do enter something: ")\n    if(timedOut):\n        print("Timed out when waiting for input.")\n        print(f"User-input so far: \'{userText}\'")\n    else:\n        print(f"User-input: \'{userText}\'")\n\n\n*timedKey()* waits for the user to press one of a set of predefined keys, with a timeout, while ignoring any keys not on the list.\n\n.. code:: python\n\n    def timedKey(prompt="", timeOut=5, forcedTimeout=False, endCharacters=[\'y\', \'n\'])\n\nThe function *timedKey()* from *pyTimedInput* accepts the following parameters:\n\n - **prompt**, *str*: a string to show the user as a prompt when waiting for input.\n     *Defaults to an empty string.*\n - **timeout**, *int*: how many seconds to wait before timing out.\n     *Defaults to 5 seconds.*\n - **forcedTimeout**, *bool*: whether to wait for \'timeout\' many consecutive seconds of idle time or simply time out regardless of user-input.\n     *Defaults to False, ie. consecutive.*\n - **endCharacters** [], *list*: what characters to accept.\n     *Defaults to \'y\' and \'n\'.*\n\nThe function returns a tuple of:\n\n - *str*: a string containing the key user pressed, if on the endCharacters - list, or an empty string.\n - *bool*: whether the function timed out or not.\n\n.. code:: python\n\n    from pyTimedInput import timedKey\n    userText, timedOut = timedKey("Please, press \'y\' to accept or \'n\' to decline: ", endCharacters=[\'y\', \'n\'])\n    if(timedOut):\n        print("Timed out when waiting for input. Pester the user later.")\n    else:\n        if(userText == "y"):\n            print("User consented to selling their first-born child!")\n        else:\n            print("User unfortunately declined to sell their first-born child!")\n\nExceptions\n----------\n\nBoth *timedInput()* and *timedKey()* require an interactive shell to function and will raise a Runtimerror - exception otherwise, which will need to be caught in any script that will be used both interactively and non-interactively.\n\nLicense\n-------\n\nMIT',
    'author': 'WereCatf',
    'author_email': 'werecatf@runbox.com',
    'maintainer': 'WereCatf',
    'maintainer_email': 'werecatf@runbox.com',
    'url': 'https://github.com/werecatf/pyTimedInput/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
