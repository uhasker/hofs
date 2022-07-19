import argparse

import hofs as fs

parser = argparse.ArgumentParser(description="Get project statistics.")
parser.add_argument("--dir", type=str, required=True, help="Project directory.")
parser.add_argument(
    "--globs", type=str, required=True, help="Globs to look for (separated by comma)."
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--include", type=str, help="Directories to include (should be split by comma)."
)
group.add_argument(
    "--exclude", type=str, help="Directories to exclude (should be split by comma)."
)
args = parser.parse_args()

project_dir = args.dir
globs = args.globs.split(",")
print(args.include, args.exclude)
if args.include is not None:
    include = True
    included_or_excluded_dirs = [
        fs.expand_path(path) for path in args.include.split(",")
    ]
else:  # elif args.exclude is not None
    include = False
    included_or_excluded_dirs = [
        fs.expand_path(path) for path in args.exclude.split(",")
    ]

files = (
    fs.Dir(project_dir)
    .files.include_or_exclude(included_or_excluded_dirs, include)
    .filter_path_glob(globs)
    .text_file_iterator()
)

table = fs.Table(cols=["Path", "Total lines", "Source lines", "Blank lines"])

total_lines_all, source_lines_all, blank_lines_all = 0, 0, 0

for file in files:
    total_lines = file.line_count
    blank_lines = file.lines.filter(lambda line: line == "" or line.isspace()).len()
    source_lines = total_lines - blank_lines

    total_lines_all += total_lines
    blank_lines_all += blank_lines
    source_lines_all += source_lines

    table.add_row(
        {
            "Path": fs.relative_path(file.path, project_dir),
            "Total lines": str(total_lines),
            "Source lines": str(source_lines),
            "Blank lines": str(blank_lines),
        }
    )

table.add_row(
    {
        "Path": "TOTAL",
        "Total lines": str(total_lines_all),
        "Source lines": str(source_lines_all),
        "Blank lines": str(blank_lines_all),
    }
)

print(table)
