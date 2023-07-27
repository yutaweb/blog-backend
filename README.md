# [WIP] ブログ投稿サイト

## 概要
ブログ投稿を行い、そこに対してリアクション（コメント、いいね）をできるような一般的なブログサイトです。

## 目次
1. 使用言語
2. リポジトリ説明
3. インフラ環境
4. システム構成
5. 使用方法

## 使用言語
Django, Angular
```
asgiref==3.6.0
autopep8==2.0.2
backports.zoneinfo==0.2.1
beautifulsoup4==4.11.1
cachetools==5.3.0
certifi==2022.12.7
charset-normalizer==3.1.0
Django==4.1.5
django-extensions==3.2.1
django-livereload-server==0.4
django-storages==1.13.2
flake8==6.0.0
google-api-core==2.11.0
google-auth==2.17.3
google-cloud-core==2.3.2
google-cloud-storage==2.8.0
google-crc32c==1.5.0
google-resumable-media==2.4.1
googleapis-common-protos==1.59.0
gunicorn==20.1.0
idna==3.4
mccabe==0.7.0
mysqlclient==2.1.1
payjp==0.2.0
Pillow==9.5.0
protobuf==4.22.3
pyasn1==0.5.0
pyasn1-modules==0.3.0
pycodestyle==2.10.0
pydotplus==2.0.2
pyflakes==3.0.1
pyparsing==3.0.9
PyYAML==6.0
requests==2.28.2
rsa==4.9
six==1.16.0
soupsieve==2.3.2.post1
sqlparse==0.4.3
tomli==2.0.1
tornado==6.2
urllib3==1.26.15
```

## リポジトリ構成

## 構成図
![ブログサイトの構成図 drawio](https://github.com/yutaweb/blog/assets/64781052/637349e9-4140-47fb-91d7-fc3e0a9b5f42)

## ER図
![ブログサイトのER図 drawio](https://github.com/yutaweb/blog/assets/64781052/96aac1df-532d-4dd3-91f8-96c0095d978b)


## 使用方法
TODO
```
# 静的ファイルを集める
python manage.py collectstatic

# GAEへデプロイ
gcloud app deploy --project blog-site-384200

# Cloud SQLへ接続
./secrets/cloud-sql-proxy --port 3306 blog-site-384200:us-central1:blog-site-test-instance
※コスト削減の為、停止している。
```

## メモ
```
pycacheを削除したい場合
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

requirements.txtを作成したい場合
pip freeze >requirements.txt
```
