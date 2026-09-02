# Trace record

The local runner must record:

- command, wrapper path and resolved MultiQC executable;
- MultiQC and Python versions;
- input file list and aggregate input hash;
- configuration and parameter values;
- artifact paths and hashes;
- execution status, scientific status and release status separately;
- verifier output and any human review decision.

This directory is the trace schema/documentation. A concrete run record is
written to the selected run output directory, not to the source fixture.
