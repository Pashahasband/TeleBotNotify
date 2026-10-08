import zipfile, os, sys

zip_path = '/tmp/tools.zip'
if not os.path.exists(zip_path):
    print(f"ERROR: {zip_path} does not exist!")
    sys.exit(1)

print(f"Zip file size: {os.path.getsize(zip_path)} bytes")

with zipfile.ZipFile(zip_path, 'r') as z:
    names = z.namelist()
    print("Files in zip:")
    for name in names[:10]:
        print(f"  {name}")
    
    z.extractall('/tmp/')

print("\nAfter extraction:")
if os.path.exists('/tmp/cmdline-tools'):
    print("cmdline-tools exists!")
    print(os.listdir('/tmp/cmdline-tools'))
    if os.path.exists('/tmp/cmdline-tools/bin'):
        print("bin exists:", os.listdir('/tmp/cmdline-tools/bin'))
    else:
        print("ERROR: bin directory not found!")
        sys.exit(1)
else:
    print("cmdline-tools does not exist!")
    print("Contents of /tmp:", os.listdir('/tmp'))
    sys.exit(1)

print("\nExtraction successful!")
