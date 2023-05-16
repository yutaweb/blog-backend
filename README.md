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
```

## メモ
```
pycacheを削除したい場合
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

requirements.txtを作成したい場合
pip freeze >requirements.txt
```
