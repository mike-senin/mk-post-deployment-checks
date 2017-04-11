Salt MK Verificator
========================

This is salt-based set of tools for basic verification of mk* deployments 

How to start
=======================

1) Copy repo to **cfg-*** node or clone it:
```bash 
   # root@cfg-01:~/# git clone https://github.com/msenin94/mk-post-deployment-checks 
```
Use git config --global http.proxy http://proxyuser:proxypwd@proxy.server.com:8080
if needed.

2) Go to the repo folder:
```bash
   # cd mk-post-deployment-checks/
```

3) Create virtualenv and install requirements and package:
```bash
   # virtualenv --system-site-packages .venv
   # source .venv/bin/activate
   # pip install --proxy http://$PROXY:8678 -r requirements.txt
   # python setup.py install
   # python setup.py develop
```

4) Start tests (make sure you are root):
```bash 
   # pytest -sv mk_verificator/tests/ --ignore mk_verificator/tests/test_migration.py --ignore mk_verificator/tests/test_floating_ip.py 
```
Note that all tests and benchmarks that use nova client and ssh are not working from cfg node (only from bmk).
