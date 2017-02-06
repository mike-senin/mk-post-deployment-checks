Salt MK Verificator
========================

This is salt-based set of tools for basic verification of deployments tcpcloud solution

How to install 
=======================

1) Copy repo to cfg-* node
   .. code-block:: bash
       $ ssh cfg-01
2) Go to the repo folder
   .. code-block:: bash
       $ cd mk-post-deployment-checks/

3) Create virtualenv and install requirements and package:
   .. code-block:: bash
       $ virtualenv --system-site-packages venv
       $ source venv/bin/activate
       $ pip install --proxy http://$PROXY:8678 -r requirements.txt
       $ python setup.py install
       $ python setup.py develop

4) Start tests:
   .. code-block:: bash
       $ cd mk_verificator/
       $ py.test -sv
