#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
A script to run the clustering analyses.
"""

# Future #
from __future__ import division

# Don't run it #
import sys
sys.exit("Copy paste the commands you want in ipython, don't run this script.")

# Modules #
import illumitag

###############################################################################
# Get the cluster #
cluster = illumitag.clustering.favorites.jerome

# Stuff #
cluster.otu_uparse.taxonomy_silva.make_filtered_centers()

# Run seqenv #
cluster.run(steps=[{'otu_uparse.seqenv.run': dict(threads=False)}])
cluster.run_slurm(steps=[{'otu_uparse.seqenv.run': dict(threads=False)}], time="1-00:00:00")
"bash -x /home/lucass/share/seqenv/SEQenv_v0.8/SEQenv_samples.sh -f /home/lucass/ILLUMITAG/views/clusters/jerome/otus/uparse/taxonomy_silva/centers.fasta -s /home/lucass/ILLUMITAG/views/clusters/jerome/otus/uparse/seqenv/abundances.csv -n 1000 -p -c 16"