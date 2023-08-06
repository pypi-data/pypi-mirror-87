import itertools
import random
import os
import unittest
import pytest

from mavis.assemble import assemble, Contig, DeBruijnGraph, filter_contigs, kmers
from mavis.constants import DNA_ALPHABET

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestModule(unittest.TestCase):
    """
    test class for functions in the validate namespace
    that are not associated with a class
    """

    def test_alphabet_matching(self):
        self.assertTrue(DNA_ALPHABET.match('N', 'A'))
        self.assertTrue(DNA_ALPHABET.match('A', 'N'))

    def test_kmers(self):
        k = kmers('ABCDEFG', 2)
        self.assertEqual(['AB', 'BC', 'CD', 'DE', 'EF', 'FG'], k)
        k = kmers('ABCDEFG', 3)
        self.assertEqual(['ABC', 'BCD', 'CDE', 'DEF', 'EFG'], k)

    def test_assemble(self):
        sequences = ['ABCD', 'BCDE', 'CDEF', 'ABCDE', 'DEFG']
        c = assemble(sequences, 3, min_edge_trim_weight=1, remap_min_exact_match=1)
        self.assertEqual(1, len(c))
        self.assertEqual('ABCDEFG', c[0].seq)
        self.assertEqual(5, c[0].remap_score())

    def test_assemble_empty_list(self):
        self.assertEqual([], assemble([], 1))

    def test_repeat_region_assembly(self):
        rep = 'ABCDEF'
        seqs = kmers(rep + rep, len(rep))
        contigs = assemble(seqs, len(rep) - 1, remap_min_exact_match=1)
        self.assertEqual(0, len(contigs))


class TestFilterContigs(unittest.TestCase):
    def test_drop_reverse_complement(self):
        c1 = Contig('atcgatcgatcgatcgatcgatcgatatagggcatcagc', 1)
        c2 = Contig('gctgatgccctatatcgatcgatcgatcgatcgatcgat', 1)
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(1, len(result))
        self.assertEqual(c1.seq, result[0].seq)

    def test_drop_alt_allele_alphabetically(self):
        c1 = Contig('atcgatcgatcgatcgatcgatcgatatagggcatcagc', 1)
        c2 = Contig('atcgatcgatcgatcgatctatcgatatagggcatcagc', 1)
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(1, len(result))
        self.assertEqual(c1.seq, result[0].seq)

    def test_drop_alt_allele_by_score(self):
        c1 = Contig('atcgatcgatcgatcgatcgatcgatatagggcatcagc', 2)
        c2 = Contig('atcgatcgatcgatcgatctatcgatatagggcatcagc', 1)
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(1, len(result))
        self.assertEqual(c1.seq, result[0].seq)

    def test_retain_disimilar(self):
        c1 = Contig('atcgatcgatcgatcgatcgatcgatatagggcatcagc', 2)
        c2 = Contig('atcgadatcgatcgatcgatctgtdstcgatatagggca', 1)
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(2, len(result))

    def test_retain_disimilar_different_lengths(self):
        c1 = Contig('atcgatcgatcgatcgatcgatcgatatagggcatcagc', 2)
        c2 = Contig('atcgatcgatcgatcgatcgatcccgtgatatagggcatcagc', 1)
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(2, len(result))

    def test_drop_similar_different_lengths(self):
        c1 = Contig(
            'atcgatcgatcgatcgatatcgatcgatcgatcgatatcgatcgatcgatcgatatcgatcgatcgatcgatcgatcgatatgggcatcagc',
            2,
        )
        c2 = Contig(
            'atcgatcgatcgatcgatatcgatcgatcgatcgatatcgatcgatcgatcgatatcgatcgatcgatcgatcgatcgatagggcatcagc',
            1,
        )
        result = filter_contigs([c2, c1], 0.10)
        self.assertEqual(1, len(result))
        self.assertEqual(c1.seq, result[0].seq)


class TestDeBruijnGraph(unittest.TestCase):
    @pytest.mark.skipif(os.environ.get('RUN_FULL', '0') != '1', reason='running short tests only')
    def test_trim_tails_by_freq_forks(self):
        g = DeBruijnGraph()
        for s, t in itertools.combinations([1, 2, 3, 4, 5, 6], 2):
            g.add_edge(s, t)
            print('s => t', s, t)
        g.add_edge(6, 1)
        g.add_node(10)  # singlet
        g.add_edge(7, 6)
        g.add_edge(8, 7)
        g.add_edge(9, 8)
        g.trim_tails_by_freq(2)
        self.assertEqual([1, 2, 3, 4, 5, 6], sorted(g.nodes()))

        g = DeBruijnGraph()
        for s, t in itertools.combinations([1, 2, 3, 4, 5, 6], 2):
            g.add_edge(s, t)
        g.add_node(10)  # singlet
        g.add_edge(6, 1)
        g.add_edge(7, 6)
        g.add_edge(7, 8)
        g.add_edge(8, 7)
        g.add_edge(9, 8)
        g.trim_tails_by_freq(2)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], sorted(g.nodes()))

        g = DeBruijnGraph()
        for s, t in itertools.combinations([1, 2, 3, 4, 5, 6], 2):
            g.add_edge(s, t)
        g.add_node(10)  # singlet
        g.add_edge(6, 1)
        g.add_edge(7, 6)
        g.add_edge(7, 8)
        g.add_edge(9, 8)
        g.trim_tails_by_freq(2)
        self.assertEqual([1, 2, 3, 4, 5, 6], sorted(g.nodes()))

    def test_add_edge(self):
        g = DeBruijnGraph()
        g.add_edge(1, 2)
        self.assertEqual(1, g.get_edge_freq(1, 2))
        g.add_edge(1, 2)
        self.assertEqual(2, g.get_edge_freq(1, 2))
        g.add_edge(1, 2, 5)
        self.assertEqual(7, g.get_edge_freq(1, 2))

    def test_trim_noncutting_paths_by_freq_degree_stop(self):
        g = DeBruijnGraph()
        for s, t in itertools.combinations([1, 2, 3, 4], 2):
            g.add_edge(s, t, freq=4)
        for s, t in itertools.combinations([5, 6, 7, 8], 2):
            g.add_edge(s, t, freq=4)
        path1 = [5, 9, 10, 11, 12, 1]
        for s, t in zip(path1, path1[1:]):
            g.add_edge(s, t)
        for edge in g.edges():
            print(edge)
        g.trim_noncutting_paths_by_freq(3)
        self.assertEqual(list(range(1, 9)) + path1[1:-1], g.nodes())

        # add an equal weight path to force namesorting
        path2 = [5, 13, 14, 15, 16, 1]
        for s, t in zip(path2, path2[1:]):
            g.add_edge(s, t)

        g.trim_noncutting_paths_by_freq(3)
        self.assertEqual(list(range(1, 9)) + path2[1:-1], g.nodes())

        # add back the original path with a higher (but still low) weight
        for s, t in zip(path1, path1[1:]):
            g.add_edge(s, t, freq=2)

        g.trim_noncutting_paths_by_freq(3)
        self.assertEqual(list(range(1, 9)) + path1[1:-1], g.nodes())

        # add the second path with 1 high weight edge
        path2 = [5, 13, 14, 15, 16, 1]
        for s, t in zip(path2, path2[1:]):
            g.add_edge(s, t)
        g.add_edge(14, 15, freq=6)

        g.trim_noncutting_paths_by_freq(3)
        self.assertEqual(list(range(1, 9)) + path2[1:-1], g.nodes())


class TestFullAssemly(unittest.TestCase):
    def setUp(self):
        # load the sequences
        with open(os.path.join(DATA_DIR, 'test_assembly_sequences.txt')) as fh:
            self.seq = [i.strip() for i in fh.readlines()]

    @pytest.mark.skipif(os.environ.get('RUN_FULL', '0') != '1', reason='running short tests only')
    def test_deterministic_assembly(self):
        contig_sequences = set()
        for i in range(20):
            random.shuffle(self.seq)
            contigs = assemble(
                self.seq,
                111,
                min_edge_trim_weight=3,
                assembly_max_paths=8,
                assembly_min_uniq=0.1,
                min_complexity=0.1,
            )
            self.assertEqual(1, len(contigs))
            contig_sequences.add(contigs[0].seq)
        self.assertEqual(1, len(contig_sequences))
