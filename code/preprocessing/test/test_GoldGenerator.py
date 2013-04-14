# L. Amber Wilcox-O'Hearn 2013
# test_GoldGenerator.py

from code.preprocessing import GoldGenerator
import unittest, StringIO, json

class GoldTest(unittest.TestCase):

    def test_correct_sentence_and_collect_insertables_and_deletables(self):

        sentence = "S Our current population is 6 billion people and it is still growing exponentially .\n"
        corrections = []
        insertables = set([])
        deletables = set([])
        corrected = GoldGenerator.correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables)
        self.assertEqual(corrected, "Our current population is 6 billion people and it is still growing exponentially .\n", corrected)
        self.assertSetEqual(insertables, set([]), insertables)
        self.assertSetEqual(deletables, set([]), deletables)

        sentence = "S This will , if not already , caused problems as there are very limited spaces for us .\n"
        insertables = set([])
        deletables = set([])
        corrections = ["A 7 8|||Vform|||cause|||REQUIRED|||-NONE-|||0", 
                       "A 14 15|||Nn|||space|||REQUIRED|||-NONE-|||0",
                       "A 11 12|||SVA|||is|||REQUIRED|||-NONE-|||0"]
        corrected = GoldGenerator.correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables)
        self.assertEqual(corrected, "This will , if not already , cause problems as there is very limited space for us .\n", corrected)
        self.assertSetEqual(insertables, set([]), insertables)
        self.assertSetEqual(deletables, set([]), deletables)

        sentence = "S It is also important to create a better material that can support the buildings despite any natural disaster like earthquakes .\n"
        insertables = set([])
        deletables = set([])
        corrections = ["A 6 7|||ArtOrDet||||||REQUIRED|||-NONE-|||0",
                       "A 12 13|||ArtOrDet||||||REQUIRED|||-NONE-|||0",
                       "A 17 18|||Nn|||disasters|||REQUIRED|||-NONE-|||0"]
        corrected = GoldGenerator.correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables)
        self.assertEqual(corrected, "It is also important to create better material that can support buildings despite any natural disasters like earthquakes .\n", corrected)
        self.assertSetEqual(insertables, set([]), insertables)
        self.assertSetEqual(deletables, set(['the', 'a']), deletables)

        sentence = "S In this era , Engineering designs can help to provide more habitable accommodation by designing a stronger material so it 's possible to create a taller and safer building , a better and efficient sanitation system to prevent disease , and also by designing a way to change the condition of the inhabitable environment ."
        insertables = set([])
        deletables = set([])
        corrections = ["A 15 16|||ArtOrDet||||||REQUIRED|||-NONE-|||0",
                       "A 24 29|||ArtOrDet|||taller and safer buildings|||REQUIRED|||-NONE-|||0"]
        corrected = GoldGenerator.correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables)
        self.assertEqual(corrected, "In this era , Engineering designs can help to provide more habitable accommodation by designing stronger material so it 's possible to create taller and safer buildings , a better and efficient sanitation system to prevent disease , and also by designing a way to change the condition of the inhabitable environment .\n", corrected)
        self.assertSetEqual(insertables, set([]), insertables)
        self.assertSetEqual(deletables, set(['a', 'building']), deletables)
        


    def test_correct_file(self):

        input_file_obj = ["S However , when the design had been carried out for a few weeks , it was stopped .\n",
             "\n",
             "S The government 's explanation was because of safety consideration for earthquakes and some other disasters .\n",
             "\n",
             "S But such explanation was of non-sense as the engineers did not see such possibility during their designing ; otherwise the design would not be carried out at all .\n",
             "A 4 5|||Prep||||||REQUIRED|||-NONE-|||0\n",
             "A 2 3|||ArtOrDet|||an explanation|||REQUIRED|||-NONE-|||0\n",
             "A 13 14|||ArtOrDet|||a possibility|||REQUIRED|||-NONE-|||0\n",
             "\n",
             "S Some evidences showed that the reason of halt of work was that the higher level of authorities thought an underground traffic system was not necessary for Harbin .\n",
             "A 6 7|||Prep|||for|||REQUIRED|||-NONE-|||0\n",
             "A 7 8|||ArtOrDet|||the halt|||REQUIRED|||-NONE-|||0\n",
             "A 9 10|||ArtOrDet|||the work|||REQUIRED|||-NONE-|||0\n",
             "A 15 16|||ArtOrDet||||||REQUIRED|||-NONE-|||0\n",
             "\n",
             "S In this example , there is nothing wrong with the original design work , but the design still can not be carried out due to political inconsistent between the city government and higher level authorities .\n",
             "\n",
             "S The similarities of political obstacles in both two steps are that such problems can not be easily solved by the engineering group , in other words , the political problems are unavoidable to some degree .\n",
             "\n",
             "S Another problem , financial issue , is quite common during design process .\n",
             "A 10 11|||ArtOrDet|||the design|||REQUIRED|||-NONE-|||0\n",
             "\n",
             "S It affects the analyzing and test step most seriously though it can affect almost every step of design work .\n",
             "A 5 6|||ArtOrDet|||the testing|||REQUIRED|||-NONE-|||0\n",
             "\n",
             "S For most design work , the engineers are always employed by some organizations or companies .\n",
             "A 5 6|||ArtOrDet||||||REQUIRED|||-NONE-|||0\n",
             "\n",
             "S Without financial support , the collection of relative information and research of the various solutions have to be done in a simpler manner , and may lead to the final failure of a design project .\n"]

        expected_output = "However , when the design had been carried out for a few weeks , it was stopped .\nThe government 's explanation was because of safety consideration for earthquakes and some other disasters .\nBut such an explanation was non-sense as the engineers did not see such a possibility during their designing ; otherwise the design would not be carried out at all .\nSome evidences showed that the reason for the halt of the work was that the higher level authorities thought an underground traffic system was not necessary for Harbin .\nIn this example , there is nothing wrong with the original design work , but the design still can not be carried out due to political inconsistent between the city government and higher level authorities .\nThe similarities of political obstacles in both two steps are that such problems can not be easily solved by the engineering group , in other words , the political problems are unavoidable to some degree .\nAnother problem , financial issue , is quite common during the design process .\nIt affects the analyzing and the testing step most seriously though it can affect almost every step of design work .\nFor most design work , engineers are always employed by some organizations or companies .\n"

        output_file_obj = StringIO.StringIO()
        ins_file_obj = StringIO.StringIO()
        del_file_obj = StringIO.StringIO()
        GoldGenerator.correct_file(input_file_obj, output_file_obj, ins_file_obj, del_file_obj)

        self.assertEqual(output_file_obj.getvalue(), expected_output, output_file_obj.getvalue())

        self.assertSetEqual(set(json.loads(ins_file_obj.getvalue())), set(['a', 'the', 'testing', 'an']))
        self.assertSetEqual(set(json.loads(del_file_obj.getvalue())), set(['of', 'the']))

if __name__ == '__main__':
    unittest.main()
