import os

import hofs as fs

TEST_FILE = fs.File(os.path.realpath(__file__))
print(f"TEST_FILE = {TEST_FILE}")

TEST_DIR = TEST_FILE.dir
TEST_DIR_PATH = TEST_DIR.path
print(f"TEST_DIR_PATH = {TEST_DIR_PATH}")

BASE_DIR = TEST_DIR.dir("base_dir")
BASE_DIR_PATH = BASE_DIR.path

print(f"BASE_DIR_PATH = {BASE_DIR_PATH}")

A_TXT_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "a.txt"))
print(f"A_TXT_PATH = {A_TXT_PATH}")

B_TXT_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "b.txt"))
print(f"B_TXT_PATH = {A_TXT_PATH}")

C_TXT2_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "c.txt2"))
print(f"C_TXT2_PATH = {C_TXT2_PATH}")

EMPTYBIN_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "emptybin"))
print(f"EMPTYBIN_PATH = {EMPTYBIN_PATH}")

RNDBIN1_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "rndbin1"))
print(f"RNDBIN1_PATH = {RNDBIN1_PATH}")

SUB_DIR_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "sub_dir"))
print(f"SUB_DIR_PATH = {SUB_DIR_PATH}")

D_TXT_PATH = fs.expand_path(os.path.join(SUB_DIR_PATH, "d.txt"))
print(f"D_TXT_PATH = {D_TXT_PATH}")

E_TXT_PATH = fs.expand_path(os.path.join(SUB_DIR_PATH, "e.txt"))
print(f"E_TXT_PATH = {E_TXT_PATH}")

EMPTY_TXT_PATH = fs.expand_path(os.path.join(SUB_DIR_PATH, "empty.txt"))
print(f"EMPTY_TXT_PATH = {EMPTY_TXT_PATH}")

RNDBIN2_PATH = fs.expand_path(os.path.join(SUB_DIR_PATH, "rndbin2"))
print(f"RNDBIN2_PATH = {RNDBIN2_PATH}")

BAD_F_TXT_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "f.txt"))
print(f"BAD_F_TXT_PATH = {BAD_F_TXT_PATH}")

BAD_OTHER_DIR_PATH = fs.expand_path(os.path.join(BASE_DIR_PATH, "other_dir"))
print(f"BAD_OTHER_DIR_PATH = {BAD_OTHER_DIR_PATH}")
