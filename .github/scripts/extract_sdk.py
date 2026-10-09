import zipfile, os, sys

zip_path = '/tmp/sdk.zip'
if not os.path.exists(zip_path):
    print(f"ERROR: {zip_path} not found")
    sys.exit(1)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall('/tmp/')

print("Extracted SDK tools")
print(os.listdir('/tmp/cmdline-tools/'))
