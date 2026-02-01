### Development Guidelines (Project‑Specific)

#### Build and Configuration

Dependency management:

- Use `requirements.txt` to list minimal dependencies.
- Use `pip` for installing dependencies.
- Use virtual environments (e.g., `venv` or `virtualenv`) to isolate project dependencies.

#### Testing

How CI runs tests (from `.github/workflows/unit-test.yml`, if it exists):

- Test runner: `unittest`
- OS: `ubuntu-latest`
- Python: 3.13
- Command: `python -m unittest tests/`

Local test commands (run from repo root):

- Run entire suite:

```
python -m unittest discover tests/
```

#### Development Notes

Code organization:

- Experimental project structure under `src/`:

Style & conventions:

- Follow Sphinx standard for all docstrings and document all modules, classes and methods. Use type hinting for arguments and return statements. Docstrings for methods should offer a one-liner summary and an example of use of the method.
- Add logging statements instead of print statements for better traceability, the level of logging should be appropriate to the context (e.g., debug, info, warning, error), and use the built-in `logging` module. You may ask for help if unsure about logging levels.

CI considerations:

- Keep `requirements.txt` up to date with the minimal set of deps; CI pins Python 3.13 and uses `pip` cache.

Releasing/running:

- For local debugging, you can launch with `python -m src.main`.
