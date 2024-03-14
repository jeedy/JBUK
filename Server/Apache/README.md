# Apache 설정 관련

## httpd -V
아파치가 올라가 있다면 현재 아파치 환경설정들을 볼수있다.

##  –with-mpm=worker 혹은 –with-mpm=prefrork
*MPM(Multi-Processing Module) 다중처리모듈

## Rewrite (redirect)
- [Apache rewrite 가이드 지침서](https://httpd.apache.org/docs/2.2/ko/misc/rewriteguide.html)
- [Test htaccess rewrite rules 1](https://htaccess.madewithlove.com/)
- [Test htaccess rewrite rules 2](https://technicalseo.com/tools/htaccess/)

```sh
RewriteEngine On
RewriteRule ^/$ /m/main [R=301,L]
RewriteCond %{REQUEST_URI} !^/mobile/appDownload
RewriteCond %{HTTP_USER_AGENT} TOURVIS_ANDROID_APP_Ver1.1.3 [OR]
RewriteCond %{HTTP_USER_AGENT} TOURVIS_ANDROID_APP_Ver1.1.2 [OR]
RewriteCond %{HTTP_USER_AGENT} TOURVIS_ANDROID_APP_Ver1.1.1 [OR]
RewriteCond %{HTTP_USER_AGENT} TOURVIS_ANDROID_APP_Ver1.1.0 [OR]
RewriteCond %{HTTP_USER_AGENT} TOURVIS_ANDROID_APP_Ver1.0. [OR]
RewriteCond %{HTTP_USER_AGENT} TOURVIS_IOS_APP_Ver1.0.
RewriteRule (.*) https://m.tourvis.com/mobile/appDownload [R]
```