# Security Policy

Test Matrix is an offline matrix-generation utility. It reads JSON specifications and does not execute commands from them, access the network, or require credentials.

## Reporting
Please report suspected vulnerabilities privately through GitHub's security reporting features when available. Do not include real secrets in reports or test fixtures.

## Scope
Security-sensitive areas include resource-exhaustion controls, malformed input handling, packaging, and CI configuration. The default 10,000-combination ceiling limits accidental Cartesian explosions; lower it for untrusted input.
