=======
History
=======

0.2.1 (01-12-2020)
------------------

* Fixed get_awg_waveforms for Pulsar QCM.
* Renamed get_acquisition_status to get_acquisition_state.
* Added optional blocking behaviour and timeout to get_sequencer_state.
* Corrected documentation on Read The Docs.
* Added value mapping for reference_source and trigger mode parameters.
* Improved readability of version mismatch.

.. note::

    * No Pulsar device firmware compatibility changes.

0.2.0 (21-11-2020)
------------------

* Added support for floating point temperature readout.
* Renamed QCoDeS parameter sequencer#_nco_phase to sequencer#_nco_phase_offs.
* Added support for Pulsar QCM input gain control.
* Significantly improved documentation on Read The Docs.

.. note::

    * Compatible with Pulsar QCM device firmware v0.4.0 and Pulsar QRM device firmware v0.3.0.

0.1.2 (22-10-2020)
------------------

* Fixed Windows assembler for dummy Pulsar
* Fixed MacOS assembler for dummy Pulsar

.. note::

    * No Pulsar device firmware compatibility changes.

0.1.1 (05-10-2020)
------------------
* First release on PyPI

.. note::

    * Compatible with Pulsar QCM device firmware v0.3.0 and Pulsar QRM device firmware v0.2.0.