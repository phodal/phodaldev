#Person's Blog

For more see in: [https://www.phodal.com/](https://www.phodal.com/)

Basis On Mezzanine CMS

##More Than Mezzanine

- Sitemap with Category & day
- More SEO
- Less feed articles length
- AutoSuggest
- API
- Mobile APP API
- Event & Ads
- Homepage Blog

##Ru

Python 2.7

1.VirtualEnv 

2.Install Deps

    pip install -r requirements.txt

3.Createdb

    python manage.py createdb

4.Run

    python manage.py runserver

Server

    gunicor. MK_dream.wsgi

##APP 

代码: [https://github.com/phodal/app](https://github.com/phodal/app)

<a href="https://play.google.com/store/apps/details?id=com.phodal.designiot">
  <img alt="Get it on Google Play"
       src="https://developer.android.com/images/brand/zh-cn_generic_rgb_wo_60.png" />
</a>

##Migrate to Django 1.8
    
    ALTER TABLE django_content_type RENAME TO content_type_old;
    
    CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
    );
    
    INSERT INTO django_content_type(id, app_label,model)
    SELECT id, app_label,model
    FROM content_type_old;
    
    DROP TABLE content_type_old;
##License

© 2015 [Phodal Huang][phodal]. This code is distributed under the MIT license.
[phodal]:http://www.phodal.com/
