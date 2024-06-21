The code was developed from scratch using the framework that Odoo provides. Odoo modules have a definite structure composed of security files (that provide access to models), models (database tables with different fields), and views (how the models are displayed in the platform). This code can’t be run on a regular terminal. It needs to be located inside the Odoo installation (in this case an Odoo installation in an AWS server that allows for online access). To effectively deploy this code, an Odoo installation was set up in AWS, adding this module to the custom modules section and the installing it in the platform. This module has no relation with Odoo’s existing module, and the platform requires no other module installed to work. All the models and views observed in the code were defined and written explicitly for the prototype.

| File or Folders  | File or Folders         | Description                                                    |
|------------------|-------------------------|----------------------------------------------------------------|
| controllers      | __init__.py             | Not used at the moment                                         |
|                  | controllers.py          | Not used at the moment                                         |
| demo             | demo.xml                | Not used at the moment                                         |
| models           | __init__.py             | Code to include models.py into the module                      |
|                  | models.py               | Declaration of all the different models / objects used in the platform (solutions, suppliers, searches, etc) |
| security         | ir.model.access.csv     | File that contains access permissions to each model            |
| static           | description             | Folder containing icon for the module                          |
|                  | icons                   | Folder containing icons for all the menus                      |
|                  | src                     | Folder containing icon for the whole platform                  |
| views            | views.xml               | Definition of the views for all the models                     |
| wizards          | __init__.py             | Code to include search_solutions.py into the module            |
|                  | search_solutions.py     | Code that performs the search of the solutions                 |
|                  | search_solutions.xml    | Definition of the views for the search wizard                  |
| __init__.py      |                         | Overall initialization of the module                           |
| __manifest__.py  |                         | File with architecture and information of the module           |
