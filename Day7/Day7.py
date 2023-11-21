"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /.
You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a).
These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
To do this, you need to determine the total size of each directory.
The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly.
(Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes.
In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
(As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
"""



# Reconstruction de l'arborescence

class Root:
    def __init__(self):
        self.name = "/"
        self.contenu = {}
        self.parent = None
        self.size = 0

    def ls(self, start:int, end:int):
        files = historique[start:end]
        print(files)
        for lfile in files:
            lfile = lfile.strip('\n')
            if not lfile.split(" ")[1] in self.contenu.keys():
                if lfile.split(" ")[0] == "dir":
                    file = Dir(lfile.split(" ")[1], self)
                else:
                    file = File(lfile.split(" ")[1], self, int(lfile.split(" ")[0]))
                self.contenu[file.name] = file

    def calculer_taille(self):
        for nffile, ffile in self.contenu.items():
            if type(ffile) is File:
                self.size += ffile.size
            elif type(ffile) is Dir:
                print(f'CALCUL {nffile} dans {self.name}...')
                print(self.size, ffile.calculer_taille())
                self.size += ffile.calculer_taille()[1]
                print(f'CALCUL {nffile} dans {self.name} TERMINE: {self.size}')
        return self.name, self.size


class Dir(Root):
    def __init__(self, name:str, parent:object):
        super().__init__()
        self.name = name
        self.parent = parent
        self.contenu = {}

class File:
    def __init__(self, name:str, parent, size:int):
        self.name = name
        self.parent = parent
        self.size = size


with open("input", "r") as f:
    historique = f.readlines()[1:]



ls = False
lsstart = None
ROOT = Root()
curdir = ROOT
i = 0
for line in historique:
    entr = line.strip("\n").split(" ")
    sym_com = entr[0]
    commande = entr[1]
    print(entr)
    if sym_com == "$": # Commande
        if ls:
            curdir.ls(lsstart,i)
            print(curdir.name, curdir.contenu)
            ls = False
            lsstart = None
        if commande == "cd":
            arg = entr[2]
            print("entering " + arg)
            if arg == "/":
                curdir = ROOT
            elif arg == "..":
                curdir = curdir.parent
            else:
                curdir = curdir.contenu[arg]
            print("now in " + curdir.name)
        elif commande == "ls":
            print("listing " + curdir.name + "\t|||\tCommande:", entr)
            ls = True
            lsstart = i+1
    i+=1

if ls:
    curdir.ls(lsstart, i)
    ls = False
    lsstart = None

nb = 2

def aff_recurs(dir:Dir, nb, total_rep_1):

    for nff, ff in dir.contenu.items():
        print("\t" * nb + "-" + nff, type(ff))
        if ff.size <= 100000 and (type(ff) == Dir or type(ff) == Root):
            total_rep_1.append((ff.size, ff.name))
        if type(ff) is Dir:
            nb += 1
            aff_recurs(ff, nb, total_rep_1)
            nb -= 1






# Affichage:
print("\n\nAffichage de l'arborescence: \n\n")
print(ROOT.calculer_taille())
total_rep_1 = []
for fichier in ROOT.contenu.values():
    print("\t-" + fichier.name, type(fichier))
    if type(fichier) is Dir:
        aff_recurs(fichier, nb, total_rep_1)

print(total_rep_1)

print(sum([x[0] for x in total_rep_1]))













