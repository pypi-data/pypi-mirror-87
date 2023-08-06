# Jij Cloud Interface

Python Interface for Jij-Cloud.

You need a Jij-Cloud account to use it.


# gRPC サーバーへの対応

`tests/test_grpc_post.py` にこのクライアントライブラリの使い方が書かれています。

APIの設定ファイルはTOML形式で以下のように書いてください
```config.toml
[default]
url = "52.188.9.93:80"
token = ""
timeout = 10
```

url にはAPIのエンドポイントを入れてください。timeout はオプションです（今回は対応していません）。



## ローカルでの開発環境をどうにかうまくしたい。

いま問題を投げるサーバーと問題を解くサーバーが違う（違うエンドポイントにいる）ので、開発環境上で揃えるのが難しい。