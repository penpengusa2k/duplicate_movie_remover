# duplicate_movie_remover

指定ディレクトリ配下にある重複した動画を削除するツール

## 初期環境構築

```sh
brew install go-task/tap/go-task
task setup
```

## 実行

```sh
# 例: task run dir=/Users/Videos
task run dir=<動画が入っているディレクトリ>
```