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

License
---

© 2014~2018 [Phodal Huang][phodal]. This code is distributed under the MIT license.

[phodal]:http://www.phodal.com/
