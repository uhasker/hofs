import argparse

import hofs as fs

parser = argparse.ArgumentParser(description="Get project statistics.")
parser.add_argument("--dir", type=str, required=True, help="Project directory.")
parser.add_argument(
    "--ext", type=str, required=True, help="File extension to look for."
)
parser.add_argument(
    "--exclude", type=str, required=True, help="Directories to exclude."
)
args = parser.parse_args()

project_dir = args.dir
ext = args.ext
excluded_dirs = [fs.expand_path(path) for path in args.exclude.split(",")]

files = (
    fs.Dir(project_dir)
    .files.exclude(excluded_dirs)
    .filter_extension(ext)
    .text_file_iterator()
)

table = fs.Table(cols=["Path", "Total lines", "Source lines", "Blank lines"])

for file in files:
    total_lines = file.line_count
    blank_lines = file.lines.filter(lambda line: line == "" or line.isspace()).len()
    source_lines = total_lines - blank_lines
    table.add_row(
        {
            "Path": fs.relative_path(file.path, project_dir),
            "Total lines": total_lines,
            "Source lines": source_lines,
            "Blank lines": blank_lines,
        }
    )

print(table)
