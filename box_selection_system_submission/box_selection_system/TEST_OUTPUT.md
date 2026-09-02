# Test Run Output

The project includes a GitHub Actions workflow at `.github/workflows/tests.yml` that runs `python manage.py test` on every push and pull request.

The build environment used to prepare this ZIP did not have Django installed and had no network access to install it, so a genuine local Django test run could not be captured here. **Do not claim this file is a successful test run.** After uploading to GitHub, use the Actions run output as the official test-run evidence, or run `python manage.py test` locally and replace this file with the real terminal output.
