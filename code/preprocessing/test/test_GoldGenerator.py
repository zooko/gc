# L. Amber Wilcox-O'Hearn 2013
# test_GoldGenerator.py

from code.preprocessing import GoldGenerator
import unittest, StringIO

class GoldTest(unittest.TestCase):

    def test_correct_sentence(self):

        input_file_obj = StringIO.StringIO()
        output_file_obj = StringIO.StringIO()
        gg = GoldGenerator.GoldGenerator(input_file_obj, output_file_obj)

        sentence = "S Our current population is 6 billion people and it is still growing exponentially ."
        corrections = []
        corrected = gg.correct_sentence(sentence, corrections)
        self.assertEqual(corrected, "Our current population is 6 billion people and it is still growing exponentially .", corrected)

        sentence = "S This will , if not already , caused problems as there are very limited spaces for us ."
        corrections = ["A 7 8|||Vform|||cause|||REQUIRED|||-NONE-|||0", 
                       "A 14 15|||Nn|||space|||REQUIRED|||-NONE-|||0",
                       "A 11 12|||SVA|||is|||REQUIRED|||-NONE-|||0"]
        corrected = gg.correct_sentence(sentence, corrections)
        self.assertEqual(corrected, "This will , if not already , cause problems as there is very limited space for us .", corrected)


        sentence = "S It is also important to create a better material that can support the buildings despite any natural disaster like earthquakes ."
        corrections = ["A 6 7|||ArtOrDet||||||REQUIRED|||-NONE-|||0",
                       "A 12 13|||ArtOrDet||||||REQUIRED|||-NONE-|||0",
                       "A 17 18|||Nn|||disasters|||REQUIRED|||-NONE-|||0"]
        corrected = gg.correct_sentence(sentence, corrections)
        self.assertEqual(corrected, "It is also important to create better material that can support buildings despite any natural disasters like earthquakes .", corrected)

if __name__ == '__main__':
    unittest.main()
