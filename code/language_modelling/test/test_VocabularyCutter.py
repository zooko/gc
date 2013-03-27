# L. Amber Wilcox-O'Hearn 2013
# test_VocabularyCutter.py

import unittest, StringIO
from code.language_modelling import VocabularyCutter


class VocabularyCutterTest(unittest.TestCase):

    def test_cut_vocabulary(self):

        infile_obj = ["funeral 4\n",
                      "demonstrated 2\n",
                      "direction 3\n",
                      "Ger 8\n",
                      "dependence 3\n",
                      "adequate 4\n",
                      "exhibit 2\n",
                      "extra 4\n",
                      "evocative 1\n",
                      "eves 2\n",
                      "held 15\n",
                      "contact 4\n",
                      "Arkansas 2\n",
                      "divided 6\n",
                      "edge 5\n",
                      "holy 2\n",
                      "educator 1\n",
                      "Swedish 2\n",
                      "focused 6\n",
                      "Western 3\n",
                      "felon 1\n",
                      "abandon 2\n",
                      "Chris 7\n",
                      "being 17\n",
                      "deficits 7\n"]

        outfile_obj = StringIO.StringIO()

        vc = VocabularyCutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(5)

        assert outfile_obj.getvalue() == "being\nheld\nGer\ndeficits\nChris\n", outfile_obj.getvalue()

if __name__ == '__main__':
    unittest.main()
