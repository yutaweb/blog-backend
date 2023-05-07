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
![ブログサイトの構成図 drawio](https://user-images.githubusercontent.com/64781052/230820033-67230c5e-f266-4ee6-b4a7-b4b17ce55f6d.png)

## ER図
![ブログサイトのER図 drawio](https://user-images.githubusercontent.com/64781052/230820058-356ab7e6-163f-4f19-888f-346203ee312d.png)

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
