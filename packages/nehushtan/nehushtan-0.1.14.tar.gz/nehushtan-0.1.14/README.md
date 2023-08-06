# Nehushtan (נְחֻשְׁתָּן)

A toolkit for projects in Python

![PyPI](https://img.shields.io/pypi/v/nehushtan)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nehushtan)
![PyPI - License](https://img.shields.io/pypi/l/nehushtan)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nehushtan)

<img src="https://github.com/sinri/nehushtan/blob/master/icon.png?raw=true" width="64" height="64"></img>

> ipse dissipavit excelsa et contrivit statuas et succidit lucos confregitque serpentem aeneum quem fecerat Moses siquidem usque ad illud tempus filii Israhel adolebant ei incensum vocavitque eum Naasthan

## History in Brief

### Released

* 0.1.2: First version on PYPI with MySQL Toolkit.
* 0.1.3: Add CLI Helper, Logger, SMTP.
* 0.1.4: Changed a lot for projects.
* 0.1.5: Rename `NehushtanArgumentParser`. Revoke the declaration of source root to rebuild the import package.
* 0.1.6: Fix packaging issue.
* 0.1.7: Fix bug, `make_condition_sql` should be replaced.
* 0.1.8: Remove shovel related static maker methods from logger class. Fix MySQL Toolkit Bug.
* 0.1.9: Fix loose throw policy in condition sql making. That has been proved very dangerous.
* 0.1.10: Support MySQL Deep Functions for one table, such as
    [INSERT ... ON DUPLICATE KEY UPDATE Statement](https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html), 
    etc.
* 0.1.11: Remove declarations of the class variables which would be initialized with instances.
* 0.1.12: MySQL Package Refines. 
    1. Raise Exception when tries to get result from MySQLQueryResult but actually not generated yet [GitHub Issue #1](https://github.com/sinri/nehushtan/issues/1)
    2. Add Grave sign to writer methods in `MySQLTableMixin`. (Reported by Leqee Staff) 
* 0.1.13: Standardize logger keys. MySQL Auto Reconnection. Database Error Display.
* 0.1.14: Fix a bug in `raw_query_for_all_dict_rows`.

### Developing

* 0.1.15: Pending

## Notice

* [Pythonのクラスの変数に潜む地雷](https://qiita.com/sinri/items/368a489412c78cb9d4e3)
    > Python的class变量声明也不是不能当动态变量用，安全起见一定要在初始化的时候彻底初始化一下，避免id固化。