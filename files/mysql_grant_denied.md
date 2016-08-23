---
title: access denied for user root @localhost
summary:
  When i use grant clause on localhost ,the operation denied for no permission.
tags:
  - mysql
  - upgrade
...

access denied for user root @localhost
=================

MySQL upgrade from 5.1 to 5.5 by mysql_upgrade, the mysql.user.password column is changed.
If your MySQL version > 5.5.50, verify the authentication_string for users.

```
UPDATE mysql.user SET authentication_string=PASSWORD('todo2TODO') where USER='root';
```

restart mysql service by:
```
service mysql restart
```

[reference](http://superuser.com/questions/603026/mysql-how-to-fix-access-denied-for-user-rootlocalhost)