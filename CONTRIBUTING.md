# Contributing

Contributions are welcome when they keep Test Matrix deterministic, small, and safe.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e . pytest`.
3. Add or update tests for behavior changes.
4. Run `python -m pytest` and `python -m compileall -q src`.
5. Update both English and Arabic README sections when user-facing behavior changes.
6. Open a pull request explaining the problem, solution, and validation performed.

Please avoid generated artifacts, secrets, unrelated formatting changes, and new runtime dependencies unless they provide clear value.
