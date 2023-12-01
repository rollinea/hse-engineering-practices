## Вывод линтеров
### flake8
`./ep_hw1/life_game.py:1:1: F403 'from collections import *' used; unable to detect undefined names`\
`./ep_hw1/life_game.py:37:49: F405 'Counter' may be undefined, or defined from star imports: collections`\
`./ep_hw1/life_game.py:38:20: F405 'Counter' may be undefined, or defined from star imports: collections`\
`./ep_hw1/life_game.py:38:35: F405 'Counter' may be undefined, or defined from star imports: collections`\
`./ep_hw1/life_game.py:42:80: E501 line too long (91 > 79 characters)`\
`./ep_hw1/life_game.py:57:80: E501 line too long (81 > 79 characters)`\
`./ep_hw1/life_game.py:59:80: E501 line too long (88 > 79 characters)`
### pylint
`************* Module ep_hw1.life_game`
`ep_hw1/life_game.py:42:0: C0301: Line too long (91/80) (line-too-long)`\
`ep_hw1/life_game.py:57:0: C0301: Line too long (81/80) (line-too-long)`\
`ep_hw1/life_game.py:59:0: C0301: Line too long (88/80) (line-too-long)`\
`ep_hw1/life_game.py:1:0: C0114: Missing module docstring (missing-module-docstring)`\
`ep_hw1/life_game.py:1:0: W0401: Wildcard import collections (wildcard-import)`\
`ep_hw1/life_game.py:6:0: C0115: Missing class docstring (missing-class-docstring)`\
`ep_hw1/life_game.py:6:0: R0205: Class 'LifeGame' inherits from object, can be safely removed from bases in python3 (useless-object-inheritance)`\
`ep_hw1/life_game.py:55:19: R1714: Consider merging these comparisons with 'in' by using 'entity_name in ('fish', 'shrimp')'. Use a set instead if elements are hashable. (consider-using-in)`\
`ep_hw1/life_game.py:69:4: C0116: Missing function or method docstring (missing-function-docstring)`\
`ep_hw1/life_game.py:6:0: R0903: Too few public methods (1/2) (too-few-public-methods)`\
`ep_hw1/life_game.py:1:0: W0614: Unused import(s) OrderedDict, namedtuple, ChainMap, UserDict, UserList, UserString, deque and defaultdict from wildcard import of collections (unused-wildcard-import)`
------------------------------------------------------------------
`Your code has been rated at 7.18/10 (previous run: 7.18/10, +0.00)`
