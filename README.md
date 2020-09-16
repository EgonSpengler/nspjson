# nspjson
### Tinfoil-compatible json generator for serving NSP/NSZ files at home

Got NSP backups and tired of re-installing them one by one?  Now you can browse your collection in Tinfoil and queue multiple installs, among its other features.

***

Your files will need to be browseable on an HTTP server (a very quick Apache setup can accomplish this, numerous guides are available for any platform).  
Supports basic HTTP user/pass authentication, though I gave up on getting special characters in passwords to work.  (pull requests welcome)

Simply fill `config.ini.template` with your own settings and save it as `config.ini`

![Switch Screenshot](https://i.imgur.com/WHiysyB.jpg)
