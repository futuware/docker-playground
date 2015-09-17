## WORK IN PROGRESS

What we currently do in this repo is play with automation tools 
in a local environment, figuring out a perfect way to deploy our apps.

What we trying to achieve is the following:

* Web app itself and all required components, such as search, queue, cron, etc
are described, distributed and run with docker. 

* Docker images for production should be lightweight and should not include 
any unnecessary packages, especially compilers, python-dev, this kind of stuff.
On the other hand, all libraries should include all possible optimizations,
because, well, something for nothing. To achieve that we are going 
to adapt practices described in this article: 
https://glyph.twistedmatrix.com/2015/03/docker-deploy-double-dutch.html

* Deployment process causes zero downtime, is fully atomic, and prior
to switching traffic to a new version we can have a look at it at special url.
We are going to achieve that by juggling with nginx configs
and putting a bit of magic into them.

* Application should expose and listen to a unix socket rather than a port.

* Almost nothing except for standart software should run with init-scripts, 
as I find them clumsy and bum-hurting. 
We're probably go with supervisord or something similar.

* There should be a single source of truth about servers configuration,
and that's going to be ansible. Not sure yet whether to use an ansible vault
or to think of a better way.

* All of our infrastructural services are deployed with ansible as well:
Sentry, Zabbix, Jira, Teamcity, etc.

* Talking about Teamcity, it should deploy every pushed branch of repository
as completely separate and guaranteed-to-be-working-fine application
on a staging server under corresponding prefix.
Databases and migrations might be a bit of a problem here.

* Optionally, it would be nice to have an opportunity for canary deployments,
when we roll our update to a small percent of users, and have separate stats 
for that app and can compare them with those of a previous version, 
or even have an A/B test.

---

This repository consists of:

- `Vagrantfile`, `vagrant_rsa`, `vagrant_rsa.pub` to boot up virtual machines
which would pretend to be our servers. Execute `vagrant up` to get them running.
This is only required for testing purposes. We'll configure this machinery 
to use our real servers when things will become real.

- Our test app which tries to mimic our real apps. It resides in `testapp`
directory, and consists of `testapp` package and `setup.py` file to install it.


---

Instructions:

1. First, bring up testing VMs:

        $ vagrant up
1. Then, on your local machine, setup deploy server:

        $ make setup_deploy
1. And appserver

        $ make setup_appserver
1. Then go to deploy server

        $ vagrant ssh deploy
        vagrant@deploy:/vagrant$
1. Now, from deploy machine, start version build and install

        $ vagrant@deploy:/vagrant$ depl buildinst
At the end, you will get a message like this

        "msg": "Version 2015.09.15.20.56 is successfully installed"
1. When version is installed, go to `http://2015.09.15.20.56.app1.foo` and see
`Hello from base domain` or to `http://2015.09.15.20.56.foo.app1.foo/` and see
`Hello from foo`
