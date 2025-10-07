import plistlib
import os
import glob
import argparse
# フォルダ内のすべての .webloc を変換


def make_file_list(args, search_from, file_exts):
    filelist = []
    for file_ext in file_exts:
        # print(f'Search for {file_ext} in {search_from}')
        for root, _, files in os.walk(search_from):
            for file in files:
                if file.endswith(file_ext):
                    filelist.append(os.path.join(root, file))
                    if args.verbose:
                        print("\t" , file)
    return filelist


def create_filelist(args):
    files = {}
    base_dir = args.basedir
    for ext in [".webloc"]:
        if args.verbose:
            print(f"Searching {ext} file(s)")
        files[ext] = make_file_list(args, base_dir, [ext])
    return files



def convert_webloc_to_url(webloc_path, output_dir=None):
    try:
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

        print(f'Converted: {webloc_path} → {output_path}')
    except:
        print(f'Not Converted: "{webloc_path}"')


def main(args):
    files = create_filelist(args)
    for webloc_file in files:
        convert_webloc_to_url(webloc_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--verbose", help="Verbose switch", action="store_true")
    parser.add_argument("--dryrun", help="dryrun switch", action="store_true")
    parser.add_argument("--rescan", help="Rescan files", action="store_true")
    parser.add_argument("--cwd", help="variables")
    parser.add_argument("--basedir", type=str, default=os.getcwd())
    args = parser.parse_args()
    print(args.basedir)
    main(args)
