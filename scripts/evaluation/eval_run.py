#!/usr/bin/env python2

"""
A script to run the clustering analyses on the evaluation samlpes.
"""

# Future #
from __future__ import division

# Don't run it #
import sys
sys.exit("Copy paste the commands you want in ipython, don't run this script.")

# Modules #
import illumitag

###############################################################################
# Get vars #
proj = illumitag.projects['evaluation']
samples = [s for pool in proj for s in pool.samples]
cluster = illumitag.clustering.favorites.evaluation

# Load #
proj.load()

# Check bad samples #
s1 = illumitag.runs[1][3][31]
s2 = illumitag.runs[1][2][33]

# Compute Unifrac dist #
illumitag.helper.silvamod.amplify()
illumitag.helper.silvamod.amplified.graphs[1].plot(loglog=True)
cluster.otu_uparse.taxonomy_silva.make_filtered_centers()
cluster.otu_uparse.taxonomy_silva.stats.unifrac.run()

# Make fraction graph #
proj.graphs[-1].plot()