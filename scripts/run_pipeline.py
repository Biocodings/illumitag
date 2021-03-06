#!/usr/bin/env python2

"""
A script to contain examples commands
for running the pipeline.

You should run them in ipython:
$ ipython -i -c "import illumitag"
"""

# Don't run it #
import sys
sys.exit("Copy paste the commands you want in ipython, don't run this script.")

# Modules #
import illumitag

###############################################################################
# A full run #
illumitag.projects['test'].run_pools_slurm()

# Just one pool #
pj = illumitag.projects['test']; p = pj[0]; p(threads=False)
# Just one pool via slurm #
pj = illumitag.projects['andrea']; p = pj[2]; p.run_slurm()
num = illumitag.projects['inga'].first.run_slurm()
# Just one function for one pool #
pj = illumitag.projects['test']; p = pj[0]; p(steps=[{'make_pool_plots':{}}], threads=False)
# Regenerate the early exit for one pool #
illumitag.projects['inga'].first.run_slurm([{'make_qiime_output':{}},{'make_mothur_output':{}}])
# Just one graph for one pool #
illumitag.projects['evaluation'][0].load().graphs[-1].plot()
# A few pools #
pj = illumitag.projects['test']; [pool() for pool in pj.pools[1:]]
# One function for several pools in parallel #
import playdoh; playdoh.map(lambda p: p.pool_fastqc(), illumitag.projects['evaluation'].pools, cpu=5)
# All pools via SLURM #
job_ids = [pool.run_slurm() for pool in illumitag.pools]
# And analyses via slurm #
ids = [proj.run_analysis_slurm() for proj in illumitag.projects]

# One project #
pj = illumitag.projects['test']; pj.run_pools()
# One project via slurm #
pj = illumitag.projects['test']; pj.run_pools_slurm()
# Just one statistic for one project #
p = illumitag.projects['evaluation']; p.load(); [pl.good_barcodes.relative_std_dev for pl in p]
# Just one graph for one project #
p = illumitag.projects['evaluation']; p.load(); [illumitag.graphs.pool_plots.AssemblyCounts(pl).plot() for pl in p]
pj = illumitag.projects['evaluation']; pj.load(); pj.graphs[-1].plot()
# Just one function for one project #
pj = illumitag.projects['evaluation']; pj.load(); [x(steps=[{'check_noalign_counts':{}}]) for x in pj]

# Just one function for one object #
pj = illumitag.projects['evaluation']; pj.load(); p = pj.first.load(); [f.extract() for f in p.fractions]
[f.extract() for f in illumitag.projects['evaluation'].first.load().fractions]

# One graphs for one run #
run = illumitag.runs[2]; run.load(); run.graphs[0].plot()
for p in run: p.graphs[0].plot()
# All run graphs #
[r.make_plots() for r in illumitag.runs]

# SLURM Report #
illumitag.aggregate.make_slurm_report()

# Assembly statistics #
pj = illumitag.projects['evaluation']; pj.load(); pj.reporter.size_fraction_chimeras