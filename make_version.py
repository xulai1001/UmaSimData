#encoding: utf-8
import tomlkit
from tomlkit import parse
import datetime, os
import hashlib

def get_hash(filename):
    sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        sha1.update(f.read())
    ret = sha1.hexdigest()
    print(filename, ret)
    return ret

def get_last_modified(dir):
    files = [f for f in os.listdir(dir)]
    latest_entry = max(files, key=lambda x: os.path.getmtime(f'{dir}/{x}'))
    latest_time = datetime.datetime.fromtimestamp(os.path.getmtime(f'{dir}/{latest_entry}'))
    print(f"{dir}/{latest_entry}: {latest_time}")
    return latest_time

current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("当前时间:", current_date)

version = {}
with open("version.toml", encoding="utf-8") as f:
    version = parse(f.read())

for key in version:
    print(f"[{key}]")
    version[key]["date"] = str(get_last_modified(f"{key}"))
    sha1 = version[key].get("sha1")
    if sha1:
        filename = f"{key}/{version[key]['filelist'][0]}"
        new_sha1 = get_hash(filename)
        version[key]["sha1"] = new_sha1
    package_sha1 = version[key].get("package_sha1")
    if package_sha1:
        filename = f"{key}/{version[key]['package']}"
        new_sha1 = get_hash(filename)
        version[key]["package_sha1"] = new_sha1
        
with open("version.toml", "w", encoding="utf-8") as f:
    tomlkit.dump(version, f)
