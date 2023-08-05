.. _Version_History:

===============
Version History
===============

v2.2.0
------

Backwards-incompatible changes:

* Rename the following enum modules to match changes in ts_xml 7:

    * Rename ``Dome`` to ``MTDome``.
    * Rename ``Hexapod`` to ``MTHexapod``.
    * Rename ``Rotator`` to ``MTRotator``.

Other changes:

* Add this version history.

v2.1.0
------

Changes:

* Add ``MTM1M3`` enums.
* Update ``Jenkinsfile.conda`` to prevent artifacts from piling up.

v2.0.0
------

Backwards-incompatible changes:

* Overhaul the DDS quality of service file:

    * Rename it to ``qos/QoS.xml``
    * Include a named profile for each topic category.
    * Set telemetry durability to VOLATILE instead of TRANSIENT

* Remove deprecated misspelled ``ApplicationStatus`` enum from ``Hexapod`` and ``Rotator``.

Other changes:

* Add documentation.
* Add ``LinearStage`` enums.
* Update ``Dome`` enums for changes in ts_xml 6.2.
* Remove unnecessary ``__init__.py`` files from ``idl`` and ``qos`` folders and update ``setup.py`` accordingly.
* Add ``Jenkinsfile``.

v1.4.0
------

Changes:

* Correct spelling of one ``Hexapod`` and ``Rotator`` ``ApplicationStatus`` enum to ``SAFETY_INTERLOCK``,
  while leaving the old spelling for backwards compatibility.

v1.3.1
------

Changes:

* Modify ``Jenkinsfile.conda`` to use ``yum clean all``.

v1.3.0
------

Changes:

* Add ``MTM2`` enums.
* Add ``Dome`` enums.
* Modify the build files.
