# Built-in modules #
import os, json

# Internal modules #
from illumitag.groups.outcomes import BarcodeGroup
from illumitag.groups.assemble import Assembled, Unassembled
from illumitag.groups.samples import Samples
from illumitag.fasta.single import FASTQ
from illumitag.fasta.paired import PairedFASTQ
from illumitag.common.autopaths import AutoPaths, FilePath
from illumitag.helper.primers import TwoPrimers
from illumitag.graphs import outcome_plots
from illumitag.running.presample_runner import PresampleRunner

# Third party modules #

# Constants #
home = os.environ['HOME'] + '/'

###############################################################################
class Presample(BarcodeGroup):
    """A Presample is a clumsy name for a new type of barcoded-sequence files.
    As we updated the lab protocol, sample are not multiplexed with
    our traditional 50 barcodes anymore, but with Illumina specific MIDs.
    The demultiplexing thus happens in their pipeline and we are left with one
    sample per file.
    This object is a bit like a *Pool*, a *BarcodeGroup* and a *Sample*."""

    all_paths = """
    /logs/
    /graphs/
    /quality_reads/
    /info.json
    /assembled/
    /unassembled/
    """

    def __repr__(self): return '<%s object "%s">' % (self.__class__.__name__, self.id_name)
    def __str__(self): return self.id_name
    def __iter__(self): return iter(self.children)
    def __len__(self): return self.count
    def __getitem__(self, key): return self.samples[key]

    def __init__(self, json_path, out_dir):
        # Attributes #
        self.out_dir = out_dir
        self.json_path = FilePath(json_path)
        # Parse #
        with open(json_path) as handle: self.info = json.load(handle)
        # Basic #
        self.account = self.info['uppmax_id']
        self.run_num = self.info['run_num']
        self.run_label = self.info['run_id']
        self.project_short_name = self.info['project']
        self.project_long_name = self.info['project_name']
        self.fwd_name = self.info['forward_reads']
        self.rev_name = self.info['reverse_reads']
        # Own attributes #
        self.num = self.info['sample_num']
        self.label = self.info['sample_id']
        self.short_name = self.info['sample']
        self.long_name = self.info['sample_name']
        self.group = self.info['group']
        self.id_name = "run%03d-sample%02d" % (self.run_num, self.num)
        self.fwd_mid = self.info['forward_mid']
        self.rev_mid = self.info['forward_mid']
        # Special #
        self.primers = TwoPrimers(self)
        # Samples dummy #
        self.info['samples'] = [{"name": self.short_name, "used": 1, "group":self.group, "num": self.num,
                                 "fwd": self.fwd_mid, "rev": self.rev_mid}]
        self.samples = Samples(self)
        # Pool dummy #
        self.pool = self
        # Files #
        self.fwd_path = home + "ILLUMITAG/INBOX/%s/%s/%s" % (self.run_label, self.label, self.fwd_name)
        self.rev_path = home + "ILLUMITAG/INBOX/%s/%s/%s" % (self.run_label, self.label, self.rev_name)
        self.gziped = True if self.fwd_path.endswith('gz') else False
        self.fwd = FASTQ(self.fwd_path)
        self.rev = FASTQ(self.rev_path)
        self.fastq = PairedFASTQ(self.fwd.path, self.rev.path, self)
        # Automatic paths #
        self.base_dir = self.out_dir + self.id_name + '/'
        self.p = AutoPaths(self.base_dir, self.all_paths)
        # Make an alias to the json #
        self.p.info_json.link_from(self.json_path)
        # Assembly files as children #
        self.assembled = Assembled(self)
        self.unassembled = Unassembled(self)
        self.children = (self.assembled, self.unassembled)
        self.first = self.assembled
        # Graphs #
        self.graphs = [getattr(outcome_plots, cls_name)(self) for cls_name in outcome_plots.__all__]
        # Runner #
        self.runner = PresampleRunner(self)

    def make_presample_plots(self):
        for graph in self.graphs: graph.plot()
