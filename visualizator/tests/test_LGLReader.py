import unittest

from visualizator.LGLReader import LGLReader

ONE_EDGE_INPUT = \
    """
# 11.11.11.13
203.220.46.206 1
202.154.77.21 1
"""

STARTING_VERTEX = "# start"
VERTEX_WITH_WEIGHT = "vertex_1 1"
VERTEX_WITHOUT_WEIGHT = "vertex_2"


class TestLGLReader(unittest.TestCase):
    def test_given_incorrect_color_entry_returns_none(self):
        self.assertEqual(None, LGLReader.get_edge_color_entry(""))
        self.assertEqual(None, LGLReader.get_edge_color_entry(" "))
        self.assertEqual(None, LGLReader.get_edge_color_entry("# sdf"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2 d"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2 1.0"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2 1.0 d"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2 1.0 0.4"))
        self.assertEqual(None, LGLReader.get_edge_color_entry("v1 v2 1.0 0.4 d"))

    def test_given_correct_color_returns_v1_v2_r_g_b_tuple(self):
        self.assertEqual((('v1', 'v2'), (1.0, 0.4, 0.3)),
                         LGLReader.get_edge_color_entry("v1 v2 1.0 0.4 0.3"))

    def test_given_incorrect_entry_returns_none(self):
        self.assertEqual(None, LGLReader.get_vertex_label_and_weight(''))
        self.assertEqual(None, LGLReader.get_vertex_label_and_weight(' '))

    def test_given_entry_returns_label(self):
        self.assertEqual('vertex', LGLReader.get_vertex_label_and_weight('vertex'))

    def test_given_entry_with_incorrect_etry_exception_raises(self):
        try:
            LGLReader.get_vertex_label_and_weight('vertex d')
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_given_entry_with_weigth_returns_label_weight_list(self):
        self.assertEqual(['vertex', 42.1], LGLReader.get_vertex_label_and_weight('vertex 42.1'))

    def test_given_non_start_vertex_returns_false(self):
        self.assertFalse(LGLReader.is_starting_vertex(''))
        self.assertFalse(LGLReader.is_starting_vertex(' '))
        self.assertFalse(LGLReader.is_starting_vertex('one one'))

    def test_given_start_vertex_returns_true(self):
        self.assertTrue(LGLReader.is_starting_vertex('# the_vertex'))

    def test_given_incorrect_starting_vertex_returns_none(self):
        p_v = LGLReader.get_primary_vertex("")
        self.assertEqual(None, p_v)

    def test_given_starting_vertex_without_hash_returns_none(self):
        p_v = LGLReader.get_primary_vertex("vertex")
        self.assertEqual(None, p_v)

    def test_given_starting_vertex_wit_hash_without_label_returns_none(self):
        p_v = LGLReader.get_primary_vertex("#")
        self.assertEqual(None, p_v)

    def test_given_starting_vertex_wit_hash_and_label_returns_label_tuple(self):
        p_v = LGLReader.get_primary_vertex("# vertex")
        self.assertEqual("vertex", p_v)

    def test_given_starting_vertex_wit_hash_and_long_label_returns_label(self):
        p_v = LGLReader.get_primary_vertex("# the vertex")
        self.assertEqual("the", p_v)


if __name__ == '__main__':
    unittest.main()
