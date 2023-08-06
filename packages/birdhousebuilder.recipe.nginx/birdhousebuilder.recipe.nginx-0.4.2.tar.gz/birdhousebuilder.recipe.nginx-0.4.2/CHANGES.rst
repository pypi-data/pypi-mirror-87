Changes
*******

0.4.2 (2020-12-02)
==================

* Added group option for nginx config (#14).

0.4.1 (2020-12-01)
==================

* Added more SSL certificate settings to inject into nginx.conf (#13).
* Updated travis config.

0.4.0 (2019-05-02)
==================

* Fixed certificate generation on Python 3.x (#12).

0.3.7 (2018-02-07)
==================

* Feature #8: added options to handle SSL client verification.
* fixed travis build ... needed to update versions.
* pep8.

0.3.6 (2017-03-09)
==================

* Fixed #7: create ``var/tmp/nginx`` folder.
* set ``user`` directive only if different from etc-user.

0.3.5 (2016-12-12)
==================

* fixed ``etc/`` folder permissions.
* update MANIFEST.in.

0.3.4 (2016-07-14)
==================

* fixed ssl-key-length option (int value).

0.3.3 (2016-07-13)
==================

* ssl-key-length option added.

0.3.2 (2016-07-11)
==================

* create ``var/www`` folder.

0.3.1 (2016-07-04)
==================

* enabled user in nginx.conf.
* using supervisor skip-user option.

0.3.0 (2016-06-30)
==================

* enabled travis.
* updated buildout and doctests.
* added conda options env, pkgs, channels.
* using zc.recipe.deployment
* fail save with log message when cert generation fails.

0.2.6 (2016-04-11)
==================

* added cryptography conda package.

0.2.5 (2016-01-19)
==================

* set keepalive_timeout to 5s (can be overwritten in options).


0.2.4 (2016-01-15)
==================

* disabled sendfile in nginx.conf.
* ``worker_processes`` is now configurable.

0.2.3 (2015-07-06)
==================

* create cert.pem only if it does not exist.

0.2.2 (2015-06-25)
==================

* cleaned up templates.
* added user option.

0.2.1 (2015-06-23)
==================

* generates self-signed certificate for https.

0.2.0 (2015-02-24)
==================

* installing in conda enviroment ``birdhouse``.
* using ``$ANACONDA_HOME`` environment variable.
* separation of anaconda-home and installation prefix.

0.1.7 (2014-12-06)
==================

* Don't update conda on buildout update.

0.1.6 (2014-11-11)
==================

* Removed proxy configuration.
* Fixed supervisor config: nginx didn't stop.
* nginx is started as supervisor service.

0.1.5 (2014-10-27)
==================

* disabled SSLv3 (poodle attack)

0.1.4 (2014-10-21)
==================

* Updated docs.
* Fixed pyOpenSSL dependency.

0.1.3 (2014-08-26)
==================

* Fixed proxy config for wpsoutputs.
* Using proxy-enabled buildout option.
* options master and superuser_enabled added.

0.1.2 (2014-08-01)
==================

* Updated documentation.

0.1.1 (2014-07-24)
==================

* Added start-stop script for nginx.
* Generates self-signed certificate for https.

0.1.0 (2014-07-10)
==================

Initial Release.
