#!/usr/bin/env python3
"""Exercise the blog against a disposable SQLite copy, never the source database."""
import argparse
from contextlib import redirect_stdout
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
import tempfile
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True, help="Local SQLite snapshot")
    args = parser.parse_args()
    source = args.database.resolve(strict=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="blog-runtime-validation-") as directory:
        target = Path(directory) / "blog.db"
        with sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as original:
            with sqlite3.connect(target) as copy:
                original.backup(copy)
                assert copy.execute("PRAGMA quick_check").fetchone()[0] == "ok"
        os.environ["BLOG_VALIDATION_DB"] = str(target)
        os.chdir(ROOT)
        import django
        from django.conf import settings

        base = importlib.import_module("MK_dream.settings")
        config = {name: getattr(base, name) for name in dir(base) if name.isupper()}
        config.update(
            DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(target)}},
            SECRET_KEY=secrets.token_urlsafe(48),
            NEVERCACHE_KEY=secrets.token_urlsafe(48),
            DEBUG=False,
            ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"],
            CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
            CACHE_MIDDLEWARE_SECONDS=0,
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        )
        settings.configure(**config)
        django.setup()
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser
        from django.core.management import call_command
        from django.db import connection
        from django.test import Client
        from mezzanine.blog.models import BlogPost
        from mezzanine.core.models import CONTENT_STATUS_DRAFT

        assert Path(connection.settings_dict["NAME"]).resolve() == target.resolve()
        with redirect_stdout(sys.stderr):
            call_command("check", verbosity=0)
            call_command("migrate", check=True, verbosity=0)
        published = BlogPost.objects.published(for_user=AnonymousUser()).order_by("-publish_date")
        post = published.first()
        assert post is not None, "Snapshot must contain a published blog post"
        client = Client()
        routes = [
            ("/", 200), ("/blog/", 200), (post.get_absolute_url(), 200),
            ("/search/?q=agent", 200), ("/zh-hans/admin/login/", 200),
            ("/en/admin/login/", 200), ("/sitemap.xml", 200),
            ("/feeds/rss/", 200), ("/amp/" + post.slug + "/", 200),
            ("/local-runtime-probe-does-not-exist/", 404),
        ]
        failures = 0
        for route, expected in routes:
            try:
                response = client.get(route, follow=expected == 404)
                assert response.status_code == expected, (response.status_code, expected)
                if expected == 200:
                    assert len(response.content) > 500
                    if route == post.get_absolute_url():
                        assert post.title in response.content.decode()
                    if route in ["/sitemap.xml", "/feeds/rss/"]:
                        ElementTree.fromstring(response.content)
                results.append({"route": route, "status": response.status_code, "passed": True})
            except Exception as error:
                failures += 1
                results.append({"route": route, "passed": False, "error": type(error).__name__ + ": " + str(error)})
        try:
            en = Client()
            response = en.post("/i18n/setlang/", {"language": "en", "next": "/blog/"})
            assert response.status_code == 302
            response = en.get("/blog/")
            assert response.status_code == 200 and response.headers["Content-Language"] == "en"
            assert b"Recent Posts" in response.content
            user = get_user_model().objects.create_superuser(
                username="local-runtime-probe-" + secrets.token_hex(6),
                email="validation@example.invalid", password=secrets.token_urlsafe(24),
            )
            client.force_login(user)
            for route in ["/zh-hans/admin/", "/zh-hans/admin/blog/blogpost/%s/change/" % post.id]:
                response = client.get(route)
                assert response.status_code == 200
            response = client.post("/pagedown/preview", {"text": "# Runtime probe\n\n**Bold**\n\n> Quote\n\n| A | B |\n| - | - |\n| 1 | 2 |"})
            assert response.status_code == 200
            for expected in [b'<h1 id="runtime-probe">', b"<strong>Bold</strong>", b"<blockquote>", b"<table>"]:
                assert expected in response.content
            count = published.count()
            draft = BlogPost.objects.create(
                title="Local runtime validation draft", slug="local-runtime-validation-" + secrets.token_hex(6),
                content="Validation only", user=user, status=CONTENT_STATUS_DRAFT, site_id=settings.SITE_ID,
            )
            assert not BlogPost.objects.published(for_user=AnonymousUser()).filter(pk=draft.pk).exists()
            draft.title = "Updated local runtime validation draft"
            draft.save()
            draft.refresh_from_db()
            assert draft.title.startswith("Updated") and published.count() == count
            results.append({"check": "language switch, authenticated admin/edit, Markdown preview, draft create/update and visibility", "passed": True})
        except Exception as error:
            failures += 1
            results.append({"check": "language/admin/Markdown/draft", "passed": False, "error": type(error).__name__ + ": " + str(error)})
        report = {
            "python": sys.version.split()[0], "django": django.get_version(),
            "mezzanine": importlib.metadata.version("Mezzanine"),
            "database": "disposable local copy", "checks": results, "failures": failures,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
