# Phodal's Blog

Powered by Mezzanine CMS & Django & [Mifa](https://github.com/phodal/mifa) & Material Design Lite

## More Than Mezzanine

- Sitemap with Category & Date
- Limit  RSS feed articles length
- Blogposts Search API
- Mobile APP API
- Event & Ads Module
- Homepage News
- Wechat Support
- Google AMP Support (Blog Page)
- Google Micro Data

## APP 

项目代码: [https://github.com/phodal/app](https://github.com/phodal/app)

下载

<a href="https://play.google.com/store/apps/details?id=com.phodal.designiot">
  <img alt="Get it on Google Play"
       src="https://developer.android.com/images/brand/zh-cn_generic_rgb_wo_60.png" />
</a>

## Run

Python 3.5

1.VirtualEnv 

2.Install Deps

```
pip install -r requirements.txt
```

3.Createdb

````
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
