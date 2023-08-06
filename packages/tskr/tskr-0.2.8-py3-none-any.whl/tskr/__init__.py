
import os
import sys
import base64
import random
import pickle
from sout import sout
from relpath import rel2abs
from fileinit import fileinit
from .parts.AES_crypt import AESCipher

revived_file_dir = "./__tskr_revived__/"

# 16進数の乱数を生成
def gen_16_rand(n):
	ls16 = "0123456789abcdef"
	ret_ls = [ls16[int(random.random()*16)]
		for _ in range(n)]
	return "".join(ret_ls)

# tskr形式で保存
def tskr_save(org_filename, file_pool_dir, file_size_limit):
	# ファイルのidとkeyを作成
	file_id = gen_16_rand(n = 16)	# 16進数の乱数を生成
	file_key = gen_16_rand(n = 32)	# 16進数の乱数を生成
	# ファイル指定子の決定
	file_acc = "tskr_%s_%s"%(file_id, file_key)
	# 対象の読み込み
	with open(org_filename, "rb") as f:
		org_cont = f.read()
	# 容量制限
	if len(org_cont) > file_size_limit:
		print("[error] ファイル容量が大きすぎます。(容量制限: %d bytes, 今回のファイル: %d bytes)"%(file_size_limit, len(org_cont)))
		return None	# 以降の処理を実行しない
	# ファイル名とコンテンツをバインド
	raw_bind_obj = pickle.dumps({
		"original_filename": os.path.basename(org_filename),
		"contents": org_cont
	})
	# 暗号化
	base64_str = base64.b64encode(raw_bind_obj).decode()
	aesc = AESCipher(file_key)
	bind_obj = aesc.encrypt(base64_str).encode()
	# 対象の保存
	pool_filename = "%s/%s.tskr"%(file_pool_dir, file_id)
	fileinit(pool_filename, overwrite = True)
	with open(pool_filename, "wb") as f:
		f.write(bind_obj)
	return file_acc

# tskr形式のファイルを開く
def tskr_open(file_acc, file_pool_dir):
	# ファイル指定子(file_acc)の解釈
	acc_ls = file_acc.split("_")
	if acc_ls[0] != "tskr": raise Exception("[ERROR] ファイル指定子の形式が不正です")
	file_id, file_key = acc_ls[1:]
	# 対象の読み込み
	pool_filename = "%s/%s.tskr"%(file_pool_dir, file_id)
	with open(pool_filename, "rb") as f:
		bind_obj = f.read()
	# 暗号化
	aesc = AESCipher(file_key)
	base64_str = aesc.decrypt(bind_obj.decode())
	org_bind_obj = base64.b64decode(base64_str.encode())
	# バインドされたコンテンツの解釈
	org_obj = pickle.loads(org_bind_obj)
	org_filename = org_obj["original_filename"]
	org_cont = org_obj["contents"]
	# もとに戻したファイルの保存
	save_filename = "%s/%s"%(revived_file_dir, org_filename)
	fileinit(save_filename, overwrite = True)
	with open(save_filename, "wb") as f:
		f.write(org_cont)

def tskr():
	# ファイル容量制限
	file_size_limit = 10 * (1024**2)	# 10MB
	# コマンドライン引数
	argv_ls = sys.argv
	# 存在しない場合にpath_fileを生成する
	path_file = "./file_pool_path.txt"
	fileinit(rel2abs(path_file), overwrite = False)
	### pool_path書き換えモード
	if len(argv_ls) == 3 and argv_ls[1] == "--poolpath":
		with open(rel2abs(path_file), "w", encoding = "utf-8") as f:
			f.write(argv_ls[2])
		print("file_pool_pathを設定しました")
		return None
	### file_pool_pathの読み込み
	with open(rel2abs(path_file), "r", encoding = "utf-8") as f:
		file_pool_dir = f.read().strip()
	if file_pool_dir == "":
		print("file_pool_pathが設定されていません。オプション引数「--poolpath」を使って設定してください。")
		return None
	### 保存モード
	if len(argv_ls) == 2:
		# 保存対象ファイル名の取得
		org_filename = argv_ls[1]
		# tskr形式で保存
		file_acc = tskr_save(org_filename, file_pool_dir, file_size_limit)
		# ファイル指定子(file_acc)の表示
		if file_acc is not None:
			print("ファイル指定子は以下のとおりです:")
			print("\n%s\n"%file_acc)
			print("【！】忘れずにクリップボード等にコピーしてください")
		input("[Enter] で終了...")
	### 開くモード
	if len(argv_ls) == 1:
		# 対象の入力
		print("※ファイルをtskr形式に変換する際は、コマンドライン引数でファイル名を指定してください")
		file_acc = input("ファイル指定子>")
		# tskr形式のファイルを開く
		tskr_open(file_acc, file_pool_dir)
		return None

# # モジュールオブジェクトと関数を同一視
# sys.modules[__name__] = tskr
