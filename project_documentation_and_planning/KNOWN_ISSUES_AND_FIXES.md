# Known Issues and Fixes

## 1) Hugging Face Space shows "No application file"

**Cause:** Space is initialized but repository code is not connected/pushed yet.

**Fix:** Use Docker Space linked to this repo, or push this repo into Space remote so the root `Dockerfile` is available to the build.

---

## 2) Backend tests fail with `ModuleNotFoundError: No module named 'game'`

**Cause:** `pytest` doesn't include backend root in module path by default.

**Fix:** `backend/pytest.ini` now sets:

```ini
[pytest]
pythonpath = .
```

Run tests from `backend/` with virtualenv active.

---

## 3) Frontend lint scans generated bundle output

**Cause:** ESLint was traversing `frontend/dist/` exported web bundle and reporting thousands of irrelevant errors.

**Fix:** `frontend/.eslintignore` now ignores generated folders including `dist/`, `node_modules/`, and platform build artifacts.
