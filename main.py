"""
このスクリプトは、指定したディレクトリ内の重複する動画ファイルを検出し、
1つを残して他を削除するためのツールです。

動作:
- 指定したディレクトリ内のすべての動画ファイル（拡張子が .mp4、.mkv、.avi、.mov、.flv）を走査します。
- 同じ内容の動画ファイルが複数存在する場合、1つを残して他を削除します。
- ファイルの重複はファイルのハッシュ値を基に判定されます。
"""

import os
import hashlib
import argparse
from pathlib import Path


def get_file_hash(file_path, hash_algorithm=hashlib.md5):
    """
    ファイルのハッシュ値を計算する関数。

    Args:
        file_path (str): ファイルのパス。
        hash_algorithm (callable): ハッシュアルゴリズムの関数（デフォルト: hashlib.md5）。

    Returns:
        str: ファイルのハッシュ値の16進数表現。
    """
    hash_algo = hash_algorithm()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()


def find_and_remove_duplicates(directory):
    """
    指定したディレクトリ内の重複する動画ファイルを検出し、1つを除いて削除する関数。

    Args:
        directory (str or Path): 重複動画を検索するディレクトリのパス。
    """
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 動画ファイルの拡張子を確認（必要に応じて拡張子を追加）
            if not file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".flv")):
                continue

            file_hash = get_file_hash(file_path)

            if file_hash in file_hashes:
                print(f"重複ファイルを発見しました: {os.path.basename(file_path)}")
                os.remove(file_path)
            else:
                file_hashes[file_hash] = file_path


def main():
    """
    引数のパス配下にある重複動画の削除を実行する。
    """
    parser = argparse.ArgumentParser(
        description="指定したディレクトリ内の重複する動画ファイルを削除するスクリプト。"
    )
    parser.add_argument(
        "directory", type=Path, help="重複動画を検索するディレクトリのパス"
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        print("指定されたパスはディレクトリではありません、または存在しません。")
        return

    find_and_remove_duplicates(args.directory)
    print("重複ファイルの削除が完了しました。")


if __name__ == "__main__":
    main()
