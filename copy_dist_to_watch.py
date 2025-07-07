import shutil
import os

src = "watch-frontend/dist"
dest = "watch"

# Remove existing destination folder (optional, for clean copy)
if os.path.exists(dest):
    shutil.rmtree(dest)

# Copy entire dist folder to watch/
shutil.copytree(src, dest)

print("✅ Copied dist/ to watch/ successfully.")
