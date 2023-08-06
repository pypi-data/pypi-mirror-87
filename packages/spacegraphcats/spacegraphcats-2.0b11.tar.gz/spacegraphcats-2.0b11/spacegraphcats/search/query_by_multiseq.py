#! /usr/bin/env python
import argparse
import csv
import gzip
import os
import sys
import time

import khmer
import screed
import sourmash
from sourmash import MinHash

from spacegraphcats.utils.logging import notify, error, debug
from spacegraphcats.search import search_utils
from spacegraphcats.search.index import MPHF_KmerIndex
from spacegraphcats.search.catlas import CAtlas


def main(argv):
    """\
    Query a catlas with a sequence (read, contig, or genome), and retrieve
    cDBG node IDs and MinHash signatures for the matching unitigs in the graph.
    """

    p = argparse.ArgumentParser(description=main.__doc__)
    p.add_argument("catlas_prefix", help="catlas prefix")
    #    p.add_argument('output')
    p.add_argument("--query", help="query sequences", nargs="+")
    p.add_argument(
        "-k", "--ksize", default=31, type=int, help="k-mer size (default: 31)"
    )
    p.add_argument(
        "--scaled",
        default=1000,
        type=float,
        help="scaled value for contigs minhash output",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    #    p.add_argument('--cdbg-only', action='store_true',
    #                   help="(for paper eval) do not expand query using domset)")

    args = p.parse_args(argv)
    outdir = args.output

    #    if not args.query:
    #        print('must specify at least one query file using --query.')
    #        sys.exit(-1)

    # make sure all of the query sequences exist.
    #    for filename in args.query:
    #        if not os.path.exists(filename):
    #            error('query seq file {} does not exist.', filename)
    #            sys.exit(-1)

    # create output directory if it doesn't exist.
    #    try:
    #        os.mkdir(outdir)
    #    except OSError:
    #        pass
    #    if not os.path.isdir(outdir):
    #        error('output {} is not a directory', outdir)
    #        sys.exit(-1)

    # load catlas DAG
    catlas = CAtlas(args.catlas_prefix)
    notify("loaded {} nodes from catlas {}", len(catlas), args.catlas_prefix)
    notify("loaded {} layer 1 catlas nodes", len(catlas.layer1_to_cdbg))

    # find the contigs filename
    contigs = os.path.join(args.catlas_prefix, "contigs.fa.gz")

    # ...and kmer index.
    ki_start = time.time()
    kmer_idx = MPHF_KmerIndex.from_catlas_directory(args.catlas_prefix)
    notify(
        "loaded {} k-mers in index ({:.1f}s)",
        len(kmer_idx.mphf_to_kmer),
        time.time() - ki_start,
    )

    # calculate the k-mer sizes for each catlas node.
    catlas.decorate_with_index_sizes(kmer_idx)

    # get a single ksize & scaled
    ksize = int(args.ksize)
    scaled = int(args.scaled)

    # record command line
    with open(os.path.join(outdir, "command.txt"), "wt") as fp:
        fp.write(str(sys.argv))
        fp.write("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
