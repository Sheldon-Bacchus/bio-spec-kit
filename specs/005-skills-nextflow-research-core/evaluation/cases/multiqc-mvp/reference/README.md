# MultiQC representative reference

The expected observable set is intentionally small and fixture-derived:

- one FastQC report is parsed;
- sample `test_R1` is present;
- total sequences is `10000`, sequence length is `100`, and GC is `48`;
- parsed data, source mapping, log, input/artifact manifests and review note are
  present;
- the wrapper/content check is execution evidence only; scientific QC and human
  release remain `not-verified` and `pending`.

The exact output is generated under a fresh run directory and is not committed
as a gold scientific result.
