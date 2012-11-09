TrendMiner
==========

Web services for the TrendMiner project

Overview
--------

We want to build a basic web interface for project [TrendMiner][1]. This interface should be similar to the [Accurat Showcase][2] which has been implemented as a minimal Django project. Its source code is available from [GitHub][3].


Functionality
-------------

A basic front page view should be available. Users should be able to login providing username and password. After successful authentication, users get redirected to a single "action" view that allows:

 * to upload a ZIP file;
 * which is then processed using an external script (`perl/om-xml.pl`);
 * and whose output is returned to the user.

Additional views will be added at a later time.


Tasks
-----

 1. Clone this GitHub repository;
 2. Create minimal Django project for TrendMiner, following the [Accurat showcase code][3];
 3. Implement basic "action" view without calling external script;
 4. Connect external script using `subprocess.call` (see `django` folder containing original MUSING code);
 5. Retrieve script output and render it into the page template of the "action" view.


Note
----

As always, stick to PEP8 guidelines and follow Django's documentation for its [template language][4].

[1]: http://www.trendminer-project.eu/
[2]: http://www.dfki.de/accurat-showcase/
[3]: https://github.com/cfedermann/ACCURAT-Demo/
[4]: https://docs.djangoproject.com/en/1.4/topics/templates/