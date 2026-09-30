# Blog Python upgrade validation — 2026-09-30

Python 3.12 runs this blog with Mezzanine 6.1.1 and Django 4.2.30.
Python 3.14 fails real page rendering with the same application dependencies.
Granian 2.8.3 successfully serves the Python 3.12 WSGI application over HTTP.
This checkout is an upgrade candidate; the production blog Python environment
has not been replaced.

## Source and data

- Repository: https://github.com/phodal/phodaldev
- Cloned revision: `0234cc11f441de6fd828851fc8d099af61176b74`.
- Production source revision observed: `1d90909648c496ea96df028c005e39a1a3686997`.
- Production runtime observed: Python 3.9.10, Django 4.0.4, Mezzanine 6.0.0,
  Gunicorn 20.1.0. The requirements file is not evidence of installed versions.
- The effective live database is SQLite, not MySQL.
- A consistent SQLite backup was obtained with SQLite's backup API and an
  explicitly read-only source connection. It contains 1,108 blog posts.
  The local backup is private and excluded from Git. Credentials from the
  production settings were not copied.
- Validation always creates another disposable database copy. Staff accounts,
  sessions, and draft writes used for testing never touch the original snapshot
  or production database. Emails use an in-memory backend.

## Dependency changes

The cloned requirements cannot resolve: they request Django 5.2.16 while
Mezzanine 6.1.1 declares `django>=2.2,<5`. The candidate uses Django 4.2.30,
which supports Python 3.12, and updates `django-widget-tweaks` to 1.5.1,
`django-compressor` to 4.6.0, and New Relic's Python agent to 13.6.1.
The old widget-tweaks import depended on `pkg_resources`, which is absent
from the current setuptools installation. Granian is an optional dependency
in `requirements-granian.txt`; Gunicorn remains available for comparison.
`requirements-python312.lock.txt` records all 49 packages actually installed
in this validation environment. `uv pip check` passes.

Django 4.2 ended official support on April 7, 2026. This combination validates
Python/runtime compatibility but does not complete a supported Django upgrade.
A production modernization must resolve Mezzanine's Django 5 compatibility
constraint and validate that supported stack separately. Do not bypass the
constraint with `--no-deps` and treat the result as supported.

Sources: [Mezzanine package metadata](https://pypi.org/project/Mezzanine/),
[Django 4.2.8 Python 3.12 support](https://docs.djangoproject.com/en/5.2/releases/4.2.8/),
[Django support table](https://www.djangoproject.com/download/),
[Granian documentation](https://github.com/emmett-framework/granian).

## Results

| Environment | Result |
| --- | --- |
| Python 3.12.11 / Django 4.2.30 / Mezzanine 6.1.1 | All runtime checks pass |
| Python 3.14.7 / same dependencies | Django system check passes, 6 runtime checks fail |
| Python 3.12.11 / Granian 2.8.3 WSGI | Nine public HTTP routes return 200; feed and sitemap XML parse |

The runtime probe checks system configuration and applied migrations, homepage,
blog list, a real article and title, search, Chinese/English admin login, sitemap,
RSS, AMP, and final 404 handling after the existing language redirect. It also
checks the language-switch POST, authenticated admin/dashboard and article-edit
form, Markdown headings/bold/blockquote/table preview, and draft creation/update
with unpublished visibility preserved. Draft tests use the ORM; a complete
browser editing/upload workflow was not exercised.

Python 3.14 page rendering fails with:

```text
AttributeError: 'super' object has no attribute 'dicts' and no __dict__ for setting new attributes
```

Affected checks include blog list, article, search, Chinese admin login, 404
handling, and the language/admin test group. Startup alone would have missed
these failures. The probe exits nonzero when any assertion or request fails.

The real local browser rendered the blog list through Granian with its existing
styles and switched to English successfully (navigation, dates, sidebar labels).
No theme/UI changes were made. The private reports are in `.validation/`.
This is macOS validation, not acceptance on the Linux production host, and it
contains no claim of a measured production memory or throughput improvement.

## Reproduce

From the checkout, create a Python 3.12 environment and install the candidate:

```sh
uv venv --python 3.12 .venv312
uv pip install --python .venv312/bin/python -r requirements-python312.lock.txt
.venv312/bin/python scripts/validate_runtime.py --database /absolute/path/to/local-snapshot.db
```

The probe configures its own isolated settings, so no production local-settings
file or credentials are required. It emits a JSON result and returns a nonzero
exit status for failures. Use a current Python 3.12 security patch for an eventual
deployment; 3.12.11 was the already available managed local test interpreter.

For a local HTTP/browser check, use a separately copied database and an ignored
`MK_dream/local_settings.py` with a random local secret, SQLite pointing at that
copy, a locmem cache, `CACHE_MIDDLEWARE_SECONDS = 0`, and an in-memory email
backend. Bind to loopback only:

```sh
.venv312/bin/granian --interface wsgi --host 127.0.0.1 --port 19997 \
  --workers 1 --blocking-threads 2 --backpressure 8 \
  --static-path-route /static --static-path-mount static \
  --static-path-route /media --static-path-mount media \
  MK_dream.wsgi:application
```

The static mounts were for local validation. Production static/media serving
remains a separate Nginx responsibility. Before deployment, validate on Linux
in an isolated environment and port, measure PSS and response behavior, and
retain the original environment for rollback. The host currently has glibc 2.17;
Granian's cp312 x86_64 wheel supports manylinux 2.17, but the Pillow 12.3.0 wheel
resolved locally requires manylinux 2.27/2.28. The local lock therefore does not
prove an installation on this old host; a newer container userspace or compatible
build is required. Do not replace the server's system Python.
