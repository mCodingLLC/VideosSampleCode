# Example Flake8 Plugin

(Activate your virtualenv)

Install dependencies:
```
pip install -r requirements.txt
```

Run the plugin on a file:
```
flake8 cool_module.py
```

Run the tests:
```
pytest
```

Note: If you are following the video,
`flake8` introduced breaking changes in version `5`,
so that the original plugin prefix `MCOD` is now invalid.
The maximum allowed letter prefix length is now 3,
(the allowed regex is `^[A-Z]{1,3}[0-9]{0,3}` at the time of writing)
so the prefix has been changed to `MC` in this repository.
