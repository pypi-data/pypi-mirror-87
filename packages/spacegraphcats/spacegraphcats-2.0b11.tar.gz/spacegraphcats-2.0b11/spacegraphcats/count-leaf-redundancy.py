#! /usr/bin/env python
import argparse
import os
from khmer import MinHash
import parser


KSIZE = 31


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catlas_dir")
    p.add_argument("-r", "--catlas-radius", type=int, default=5)
    p.add_argument("-l", "--level", type=int, default=1)
    args = p.parse_args()

    mxtfile = ".catlas.%d.mxt" % args.catlas_radius
    mxtfile = os.path.basename(args.catlas_dir) + mxtfile
    mxtfile = os.path.join(args.catlas_dir, mxtfile)

    gxtfile = ".catlas.%d.gxt" % args.catlas_radius
    gxtfile = os.path.basename(args.catlas_dir) + gxtfile
    gxtfile = os.path.join(args.catlas_dir, gxtfile)

    print("reading gxt file")
    leaves = {}
    level_nodes = []

    def add_vertex(node_id, size, names, vals):
        assert names[0] == "vertex"
        assert names[1] == "level"
        vertex, level = vals

        if int(level) == args.level:
            level_nodes.append(node_id)

        if level == "0":
            leaves[node_id] = 0

    edges = {}

    def add_edge(a, b, *extra):
        x = edges.get(a, [])
        x.append(b)
        edges[a] = x

    parser.parse(open(gxtfile), add_vertex, add_edge)

    def recurse_from(node_id):
        x = []

        beneath = edges.get(node_id, [])
        if beneath:
            for y in beneath:
                x += recurse_from(y)
            return x
        else:
            assert node_id in leaves
            return [node_id]

    for node_id in level_nodes:
        Lnodes = set(recurse_from(node_id))
        for Lnode in Lnodes:
            leaves[Lnode] += 1

    x = list(leaves.values())
    x.sort()
    print(x)


if __name__ == "__main__":
    main()
