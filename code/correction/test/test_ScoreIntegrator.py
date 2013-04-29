# L. Amber Wilcox-O'Hearn 2013
# test_ScoreIntegrator.py

from code.correction import ScoreIntegrator
import unittest

class ScoreIntegratorTest(unittest.TestCase):

    def test_precision_recall_fmeasure(self):
        
        p,r,f = ScoreIntegrator.precision_recall_fmeasure(0, 425, 136)
        self.assertAlmostEqual(p, 0, msg=p)
        self.assertAlmostEqual(r, 0, msg=r)
        self.assertAlmostEqual(f, 0, msg=f)

        p,r,f = ScoreIntegrator.precision_recall_fmeasure(10, 20, 10)
        self.assertAlmostEqual(p, 0.5, msg=p)
        self.assertAlmostEqual(r, 1.0, msg=r)
        self.assertAlmostEqual(f, 0.666666666667, msg=f)

        p,r,f = ScoreIntegrator.precision_recall_fmeasure(10, 10, 100)
        self.assertAlmostEqual(p, 1.0, msg=p)
        self.assertAlmostEqual(r, 0.1, msg=r)
        self.assertAlmostEqual(f, 0.181818181818, msg=f)

        p,r,f = ScoreIntegrator.precision_recall_fmeasure(26, 425, 136)
        self.assertAlmostEqual(p, 0.0611764705882353, msg=p)
        self.assertAlmostEqual(r, 0.19117647058823528, msg=r)
        self.assertAlmostEqual(f, 0.09269162210338681, msg=f)

    def test_integrate_scores(self):

        results = ScoreIntegrator.integrate_scores('code/correction/test/score_data/')
        self.assertDictEqual( results, {('5', '0.7', '-1.3'): (0.20454545454545456, 0.1323529411764706, 0.1607142857142857), ('10', '0.7', '-1.3'): (0.20408163265306123, 0.14705882352941177, 0.17094017094017094), ('10', '0.5', '-1.3'): (0.16666666666666666, 0.16176470588235295, 0.16417910447761194), ('5', '0.5', '-1.3'): (0.18333333333333332, 0.16176470588235295, 0.171875)}, results )


if __name__ == '__main__':
    unittest.main()
