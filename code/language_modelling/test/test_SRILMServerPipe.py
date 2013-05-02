# L. Amber Wilcox-O'Hearn 2013
# test_SRILMServerPipe.py

from code.language_modelling import SRILMServerPipe
import unittest

server_pipe = SRILMServerPipe.SRILMServerPipe('code/language_modelling/test/closed_class_order_5.arpa', '5')

class SRILMServerPipeTest(unittest.TestCase):

    def test_srilm_server_pipe(self):
        attested_5_gram = u'JJ NNS WDT would be'
        result = server_pipe.log_probability(attested_5_gram.split())
        self.assertAlmostEqual(result, -1.201582, 5, msg=result)

        result = server_pipe.log_probability(attested_5_gram.split())
        self.assertAlmostEqual(result, -1.201582, 5, msg=result)

        path = u'as a NN were are'
        result = server_pipe.log_probability(path.split())
        self.assertAlmostEqual(result, -4.1546, 5, msg=result)

        # TODO test backoff calculations for a variety of cases.

if __name__ == '__main__':
    unittest.main()

