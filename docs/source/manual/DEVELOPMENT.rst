NRTK Explorer Development
-------------------------

Clone the Repo
~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/Kitware/nrtk-explorer.git
    cd nrtk-explorer


Setup NPM
~~~~~~~~~

To develop nrtk-explorer ensure that `npm is installed <setup>`_.

For convenience we provide scriptable instructions for Ubuntu 22.04

On Ubuntu 22.04
Installing a more modern version of node js from 06-Aug-2024 17:08

.. code:: bash

    # https://nodejs.org/en/download
    URL=https://nodejs.org/dist/v22.6.0/node-v22.6.0-linux-x64.tar.xz
    DST=node.tar.xz
    EXPECTED_SHA256="acbbe539edc33209bb3e1b25f7545b5ca5d70e6256ed8318e1ec1e41e7b35703"
    curl "$URL" -o "$DST"
    INSTALL_CAN_CONTINUE=0
    if echo "${EXPECTED_SHA256} $DST" | sha256sum --status -c ; then
        echo "checksum is ok"
        INSTALL_CAN_CONTINUE=1
    else
        echo "ERROR checksum is NOT the same"
    fi
    echo "INSTALL_CAN_CONTINUE = $INSTALL_CAN_CONTINUE"

    if [[ "$INSTALL_CAN_CONTINUE" == "1" ]]; then
        INSTALL_PREFIX="$HOME/.local/opt"
        mkdir -p "$INSTALL_PREFIX"
        tar -xvf "$DST" -C "$INSTALL_PREFIX"
        ln -s "$INSTALL_PREFIX/node-v22.6.0-linux-x64" "$INSTALL_PREFIX/node"

        if [ -d "$HOME/.local/opt/node" ]; then
            export PATH=$PATH:$HOME/.local/opt/node/bin
            export CPATH=$HOME/.local/opt/node/include:$CPATH
            export LD_LIBRARY_PATH=$HOME/.local/opt/node/lib:$LD_LIBRARY_PATH
        fi
    fi



Install in Development Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing this module, it is a good idea to be in a virtual environment. If you are no in one, you can set one up:


.. code:: bash

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip


Then you can install the library

.. code:: bash

    pip install -e '.[dev]'


Finally run tests to check that everything is working.

.. code:: bash

    pytest .
