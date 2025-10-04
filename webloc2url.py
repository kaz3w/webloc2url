import plistlib
import os

def convert_webloc_to_url(webloc_path, output_dir=None):
    with open(webloc_path, 'rb') as f:
        data = plistlib.load(f)
        url = data.get('URL')

    if not url:
        raise ValueError("URL not found in .webloc file")

    filename = os.path.splitext(os.path.basename(webloc_path))[0] + '.url'
    output_path = os.path.join(output_dir or os.path.dirname(webloc_path), filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('[InternetShortcut]\n')
        f.write(f'URL={url}\n')

    print(f'✅ Converted: {webloc_path} → {output_path}')

# フォルダ内のすべての .webloc を変換
import glob

for webloc_file in glob.glob("*.webloc"):
    convert_webloc_to_url(webloc_file)
