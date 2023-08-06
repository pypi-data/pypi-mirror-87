.. :changelog:

History
-------

0.1.0 (2018-05-25)
++++++++++++++++++

* First release on PyPI.

1.0.0 July 3 2018
+++++++++++++++++

* First production ready release.

1.1 July 28 2018
++++++++++++++++
* Refined permissions on viewsets, models and views.  Supports
  DjangoModelPermissions as a project-level default setting on all APIs.
* Convenience management commands for default group creation.
* Added the ability to analyze SBDH sender/receiver info and dynamically
  forward data based on that.  Added ability to forward data on the
  output task by specifying a "Forward Data" parameter.

Patches
+++++++
* Added unique name requirements to output criteria and endpoints.
* Added the ability to analyze SBDH sender/receiver info and dynamically
  forward data based on that.
* Added ability to forward data on the
  output task by specifying a "Forward Data" parameter.
* Fixed error with top level EPCs not being pulled within the
  AddCommissioningDataStep.

2.0+
++++
* Added a helper function to the output step to allow implementers to
  override the step to provide a different EPCPyYes document type and
  or to override the default template provided by the EPCPyYes document
  within the EPCPyYes output step.

2.1+
++++
* Added a new step that will take all EPCs in a given message and look
  up the commissioning events for those EPCs.

2.2+
++++
* Added email steps for output along with an email mixin that understands and
  can parse `mailto` URLs.  New unit tests and documentation to support.

2.3
+++
* Added new dynamic template mixin in the steps module to support implementers
  implementing classes that need to override the default templates for
  EPCPyYes during output.  This allows for customized EPCIS output generation
  using custom Jinja2 templates defined on the python path and/or configured
  in the quartet_templates package.
* Added a Skip Parsing step parameter to the OutputParsingStep to allow the
  step to just filter events using output criterion without having to parse the
  inbound message/data.
