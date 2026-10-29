# Phodal's Blog

Powered by Mezzanine CMS & Django & [Mifa](https://github.com/phodal/mifa) & Material Design Lite

**More Than Mezzanine**

- Sitemap with Category & Date
- Limit RSS feed Length
- BlogPosts Search API
- Mobile APP API
- Event & Ads Module
- Wechat Support
- Google AMP Support (Blog Page)
- Google Micro Data

Setup
---

Python 3.5

1.VirtualEnv 

```
sudo pip install virtualenv
virtualenv -p python3 ~/env/phodaldev
```

2.Install Deps

```
pip install -r requirements.txt
```

3.Createdb

```
python manage.py createdb
```

4.Run

```
python manage.py runserver
```

Server

```
gunicorn MK_dream.wsgi
```

?

``
pip3 install pysqlite3
pip3 install pysqlite3-binary
``

Production cache recovery
---

The 2026-10-29 recovery changes are versioned here; deploy files do not apply themselves.

- Restore the configured Memcached service. On the existing Amazon Linux server,
  `deploy/memcached.sysconfig` belongs at `/etc/sysconfig/memcached`; start
  `memcached` and enable it at boot. It binds only to loopback, disables UDP,
  and limits cached data to 32 MiB. Confirm a Django cache write can be read back.
- Template compilation caching is configured in `MK_dream/settings.py`. Reload
  Gunicorn after deployment. Reassess host-specific template isolation before
  configuring multiple `HOST_THEMES` in the same worker process.
- `deploy/blog-cache.conf` is a location snippet for the `www.phodal.com` HTTPS
  server. Include it before other regex locations; retain the fallback proxy
  location. It requires the existing `tmpcache` zone. For a fresh installation,
  declare `proxy_cache_path /home/cache levels=1:2 max_size=256m keys_zone=tmpcache:16m;`
  in the Nginx `http` block with a writable cache directory. Validate with
  `nginx -t` before reloading. Anonymous home/list pages and public feeds use
  a 60-second cache with background refresh; home/list requests with cookies
  or authorization bypass it.
- `deploy/blog-deny.conf` records the source blocked during the incident. Include
  it in both blog server blocks to retain the Nginx deny rule. The temporary
  host firewall rule is not installed by these files.
- The deployed Mezzanine package also has a keyword-query optimization. Reapply
  `deploy/mezzanine-keywords.patch` after reinstalling Mezzanine, from its
  site-packages directory using `patch --forward -p1`. A failed hunk requires
  checking upstream code; do not force an incompatible patch.
- Markdown HTML is cached by a content fingerprint for one hour. Editing the
  source creates a new cache key. Bump the `markdown:v1:` prefix when changing
  the renderer or its extensions.
- Feed XML cleanup applies only to generated values. Stored article text remains
  untouched; category/tag/author feeds keep full content and the main feed keeps
  summaries.

Verify with `python manage.py check` and `python manage.py test feed playdown`.
Then check anonymous and cookie-bearing pages, RSS/Atom XML parsing, cache hits,
upstream queue depth and recent 5xx logs. CPU steal on the original EC2 instance
remains a separate capacity constraint.

License
---

© 2014~2022 [Phodal Huang][phodal]. This code is distributed under the MIT license.

[phodal]:http://www.phodal.com/
