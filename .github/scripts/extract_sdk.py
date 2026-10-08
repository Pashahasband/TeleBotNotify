import zipfile, os

with zipfile.ZipFile('/tmp/tools.zip', 'r') as z:
    z.extractall('/tmp/')

print('Extracted cmdline-tools')
print(os.listdir('/tmp/cmdline-tools/'))
