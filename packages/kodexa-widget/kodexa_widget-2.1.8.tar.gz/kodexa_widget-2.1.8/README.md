kodexa-widget
===============================

A Jupyter Widget for Kodexa

Installation
------------

To install use pip:

    $ pip install kodexa_widget
    $ jupyter nbextension enable --py --sys-prefix kodexa_widget

To install for jupyterlab

    $ jupyter labextension install kodexa_widget

For a development installation (requires npm),

    $ git clone https://github.com/kodexa-ai/kodexa-widget.git
    $ cd kodexa-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix kodexa_widget
    $ jupyter nbextension enable --py --sys-prefix kodexa_widget
    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

## Watch/test local edits made to the kodexa-vue project while running jupyter lab

* In the kodexa-vue project:
  * Issue the command: `npm run build-lib`.  This will pick up and package the latest changes.
* In the kodexa-widget project:
  * Stop jupyter, if it's running
  * Edit package.json's kodexa-vue entry to the following:
   
      ```"kodexa-vue": "file:///home/skep/Projects/Kodexa/kodexa-vue/dist"```

      Note: your path will differ, but the file path should begin with /// and end with /dist

  * Issue the command: `jupyter lab build`
  * Start juptyer lab in developer watch mode with the command: `jupyter lab --watch`

    You can now leave jupyter lab running and pick up changes made to the kodexa-vue project and test directly in jupyter lab.  
    First build & package those changes in the kodexa-vue project with the command: `npm run build-lib`.
    Next, open a new terminal session, navigate to the kodexa-widget directory, and issue the command: `jupyter lab build`.
    Finally, refresh the browser in which you're viewing jupyter lab to view/test the changes.

