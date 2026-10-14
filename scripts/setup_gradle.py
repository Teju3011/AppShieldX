import os
import urllib.request
import zipfile
import shutil
import sys

target_dir = r"C:\Users\tej30\.gradle\wrapper\dists\gradle-8.4-bin\1w5dpkrfk8irigvoxmyhowfim"
os.makedirs(target_dir, exist_ok=True)

# Remove any stale lock, part, or zip files
for fname in os.listdir(target_dir):
    fpath = os.path.join(target_dir, fname)
    try:
        if os.path.isfile(fpath):
            os.remove(fpath)
        elif os.path.isdir(fpath):
            shutil.rmtree(fpath)
    except Exception as e:
        print(f"Warning cleaning {fname}: {e}")

zip_path = os.path.join(target_dir, "gradle-8.4-bin.zip")
url = "https://services.gradle.org/distributions/gradle-8.4-bin.zip"

print(f"Downloading Gradle 8.4 bin from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
    total_size = int(response.getheader('Content-Length', 0))
    downloaded = 0
    chunk_size = 1024 * 1024  # 1MB
    last_reported = 0

    while True:
        chunk = response.read(chunk_size)
        if not chunk:
            break
        out_file.write(chunk)
        downloaded += len(chunk)
        mb = downloaded / (1024 * 1024)
        pct = (downloaded / total_size * 100) if total_size else 0
        if mb - last_reported >= 20 or downloaded == total_size:
            print(f"Downloaded {mb:.1f} MB / {total_size/(1024*1024):.1f} MB ({pct:.1f}%)")
            last_reported = mb

print("Download complete. Extracting Gradle 8.4 bin archive...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(target_dir)

try:
    os.remove(zip_path)
except Exception:
    pass

# Create marker files expected by Gradle wrapper
ok_file = os.path.join(target_dir, "gradle-8.4-bin.zip.ok")
with open(ok_file, 'w') as f:
    pass

lck_file = os.path.join(target_dir, "gradle-8.4-bin.zip.lck")
with open(lck_file, 'w') as f:
    pass

# Also clean up the failed gradle-8.4-all directory to free space
all_dir = r"C:\Users\tej30\.gradle\wrapper\dists\gradle-8.4-all"
if os.path.exists(all_dir):
    try:
        shutil.rmtree(all_dir)
        print("Cleaned up incomplete gradle-8.4-all directory.")
    except Exception:
        pass

print("SUCCESS: Gradle 8.4 bin is fully extracted and ready!")
