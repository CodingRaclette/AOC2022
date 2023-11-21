"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships.
Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps.
After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure,
but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top.
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack;
in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

"""

def cratemover9000(nb, src, dst):
    for i in range(1, nb+1):
        gestion_piles[dst].append(gestion_piles[src][-1])
        gestion_piles[src].pop(-1)

def cratemover9001(nb, src, dst):
    print(gestion_piles[src], gestion_piles[src][-nb:], nb)
    gestion_piles[dst] = gestion_piles[dst] + gestion_piles[src][-nb:]
    gestion_piles[src] = gestion_piles[src][:-nb]

with open("input", "r", encoding='utf-8') as f:
    all_lines = f.readlines()

blank_line_index = all_lines.index("\n") # Index de la ligne de séparation entre le schema et la procédure

# Assimilation des piles de crates
piles = all_lines[blank_line_index-1]
piles_propre = piles.replace(" ", "").strip("\n")
gestion_piles = {}
for pile in piles_propre:
    gestion_piles[pile] = []
largeur = (len(piles) * 4) - 1

crates = all_lines[:blank_line_index-1]

for line in reversed(crates):
    print(line)
    cursor = 0
    for char in line:
        if char not in ["["," ","]","\n"]:
            gestion_piles[piles[cursor]].append(char)
        cursor+=1


# Application de la procédure
procedure = all_lines[blank_line_index+1:]

for etape in procedure:
    # Décomposition de l'étape
    nb_crates = int(etape.split(" ")[1])
    src_pile = etape.split(" ")[3]
    dst_pile = etape.split(" ")[5].strip("\n")
    cratemover9001(nb_crates, src_pile,dst_pile)

answer = ""
for pile in gestion_piles.values():
    answer = answer + pile[-1]
print(answer)





