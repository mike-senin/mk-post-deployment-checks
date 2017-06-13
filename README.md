Salt MK Verificator
========================

This is salt-based set of tools for basic verification of mk* deployments 

How to start
=======================

1) Copy repo to **cfg-*** node or clone it:
```bash 
   # root@cfg-01:~/# git clone https://github.com/msenin94/mk-post-deployment-checks 
   # cd mk-post-deployment-checks/
```
Use git config --global http.proxy http://proxyuser:proxypwd@proxy.server.com:8080
if needed.

2) Install virtualenv 
```bash
   # curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
   # tar xvfz virtualenv-X.X.tar.gz
   # cd virtualenv-X.X
   # sudo python setup.py install
```

3) Create virtualenv and install requirements and package:
```bash
   # virtualenv --system-site-packages .venv
   # source .venv/bin/activate
   # pip install --proxy http://$PROXY:8678 -r requirements.txt
   # python setup.py install
   # python setup.py develop
```

4) Prepare test state (you need to create it in your env folder):
```bash
   # mkdir /srv/salt/env/prd/test_state/
   # cat mk_verificator/tests/state_checker/init.sls.example > /srv/salt/env/prd/test_state/init.sls
```
Please change this state according to your environment (add services/packages).

5) Start tests (make sure you are root):
```bash 
   # pytest --tb=short -sv mk_verificator/tests/
```

6) Also you can use some scripts from mk_verificator/scripts:
* iperf.py - run iperf for any pair of cluster nodes
* list_services_by_group.py - list services on all nodes
* package_checker.py - check diff in packages on nodes
* services_checker.py - check diff in services on nodes
