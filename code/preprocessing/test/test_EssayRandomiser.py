# L. Amber Wilcox-O'Hearn 2011
# test_EssayRandomiser.py

from code.preprocessing import EssayRandomiser
import unittest, StringIO, random


class EssayRandomiserTest(unittest.TestCase):

    def test_randomise(self):

        e1 = ["829     0       0       0       CREATING        NNP     3       nn      (ROOT(NP*\n",
              "829     0       0       1       A       NNP     3       nn      *\n",
              "829     0       0       2       HABITABLE       NNP     3       nn      *\n",
              "829     0       0       3       ENVIRONMENT     NNP     -1      root    *))\n",
              "\n",
              "829     1       0       0       Humans  NNS     1       nsubj   (ROOT(S(S(NP*)\n",
              "829     1       0       1       have    VBP     -1      root    (VP*\n",
              "829     1       0       2       many    JJ      4       amod    (NP*\n",
              "829     1       0       3       basic   JJ      4       amod    *\n",
              "829     1       0       4       needs   NNS     1       dobj    *)))\n"]


        e2 = ["830     0       0       0       The     DT      1       det     (ROOT(FRAG(NP*\n",
              "830     0       0       1       Factors NNPS    -1      root    *)\n",
              "830     0       0       2       that    IN      4       complm  (SBAR*\n",
              "830     0       0       3       Shaped  NNP     4       nsubj   (S(NP*)\n",
              "830     0       0       4       Biometrics      VBZ     1       dep     (VP*)))))\n",
              "\n",
              "830     1       0       0       Identification  NNP     3       nsubj   (ROOT(S(NP*)\n",
              "830     1       0       1       has     VBZ     3       aux     (VP*\n",
              "830     1       0       2       become  VBN     3       cop     (VP*\n",
              "830     1       0       3       more    JJR     -1      root    (ADJP(ADJP*)\n",
              "830     1       0       4       and     CC      3       cc      *\n",
              "830     1       0       5       more    RBR     6       advmod  (ADJP*\n",
              "830     1       0       6       important       JJ      3       conj    *))\n",
              "830     1       0       7       in      IN      3       prep    (PP*\n",
              "830     1       0       8       our     PRP$    9       poss    (NP*\n",
              "830     1       0       9       society NN      7       pobj    *))))\n"]

        e3 = ["833     0       0       0       Engineers       NNS     1       nsubj   (ROOT(S(NP*)\n",
              "833     0       0       1       design  VB      -1      root    (VP*\n",
              "833     0       0       2       products        NNS     1       dobj    (NP(NP*\n",
              "833     0       0       3       or      CC      2       cc      *\n",
              "833     0       0       4       systems NNS     2       conj    *)\n",
              "833     0       0       5       that    WDT     6       nsubj   (SBAR(WHNP*)\n",
              "833     0       0       6       meet    VBP     2       rcmod   (S(VP*\n",
              "833     0       0       7       human   JJ      8       amod    (NP*\n",
              "833     0       0       8       needs   NNS     6       dobj    *))))))\n",
              "833     0       0       9       .       .       -       -       *))\n",
              "\n",
              "833     0       1       0       One     CD      3       num     (ROOT(S(NP(NP*\n",
              "833     0       1       1       current JJ      3       amod    *\n",
              "833     0       1       2       human   JJ      3       amod    *\n",
              "833     0       1       3       need    NN      11      nsubj   *)\n",
              "833     0       1       4       that    WDT     7       nsubjpass       (SBAR(WHNP*)\n",
              "833     0       1       5       should  MD      7       aux     (S(VP*\n",
              "833     0       1       6       be      VB      7       auxpass (VP*\n",
              "833     0       1       7       given   VBN     3       rcmod   (VP*\n",
              "833     0       1       8       priority        NN      7       dobj    (NP*)))))))\n",
              "833     0       1       9       is      VBZ     11      cop     (VP*\n",
              "833     0       1       10      the     DT      11      det     (NP(NP*\n",
              "833     0       1       11      search  NN      -1      root    *)\n",
              "833     0       1       12      for     IN      11      prep    (PP*\n",
              "833     0       1       13      renewable       JJ      14      amod    (NP*\n",
              "833     0       1       14      resources       NNS     12      pobj    *))))\n",
              "833     0       1       15      .       .       -       -       *))\n",
              "\n",
              "833     0       2       0       Everywhere      RB      1       advmod  (ROOT(S(PP(ADVP*)\n",
              "833     0       2       1       in      IN      7       prep    *\n",
              "833     0       2       2       the     DT      3       det     (NP*\n",
              "833     0       2       3       world   NN      1       pobj    *))\n",
              "833     0       2       4       ,       ,       -       -       *\n",
              "833     0       2       5       fuel    NN      7       nsubjpass       (NP*)\n",
              "833     0       2       6       is      VBZ     7       auxpass (VP*\n",
              "833     0       2       7       used    VBN     -1      root    (VP*\n",
              "833     0       2       8       extensively     RB      7       advmod  (ADVP*)))\n",
              "833     0       2       9       .       .       -       -       *))\n"]

        e4 = ["837     0       0       0       Title   NNP     -1      root    (ROOT(NP(NP*)\n",
              "837     0       0       1       :       :       -       -       *\n",
              "837     0       0       2       Obstacles       NNP     0       dep     (NP(NP*)\n",
              "837     0       0       3       for     IN      2       prep    (PP*\n",
              "837     0       0       4       engineering     NN      5       nn      (NP(NP*\n",
              "837     0       0       5       design  NN      3       pobj    *)\n",
              "837     0       0       6       in      IN      5       prep    (PP*\n",
              "837     0       0       7       China   NNP     6       pobj    (NP*)))))))\n",
              "\n",
              "837     1       0       0       Engineering     NNP     1       nn      (ROOT(S(NP*\n",
              "837     1       0       1       design  NN      3       nsubjpass       *)\n",
              "837     1       0       2       is      VBZ     3       auxpass (VP*\n",
              "837     1       0       3       defined VBN     -1      root    (VP*\n",
              "837     1       0       4       as      IN      3       prep    (PP*\n",
              "837     1       0       5       a       DT      6       det     (NP(NP*\n",
              "837     1       0       6       process NN      4       pobj    *)\n",
              "837     1       0       7       that    WDT     8       nsubj   (SBAR(WHNP*)\n",
              "837     1       0       8       brings  VBZ     6       rcmod   (S(VP*\n",
              "837     1       0       9       ideas   NNS     8       dobj    (NP*\n",
              "837     1       0       10      or      CC      9       cc      *\n",
              "837     1       0       11      theories        NNS     9       conj    *)\n",
              "837     1       0       12      into    IN      8       prep    (PP*\n",
              "837     1       0       13      physical        JJ      14      amod    (NP(NP*\n",
              "837     1       0       14      representations NNS     12      pobj    *)\n",
              "837     1       0       15      which   WDT     16      nsubj   (SBAR(WHNP*)\n",
              "837     1       0       16      satisfies       VBZ     14      rcmod   (S(VP*\n",
              "837     1       0       17      human   JJ      18      amod    (NP*\n",
              "837     1       0       18      needs   NNS     16      dobj    *)))))))))))))\n",
              "837     1       0       19      .       .       -       -       *))\n"]


        essay_file_obj = e1 + ['\n'] + e2 + ['\n'] + e3 + ['\n'] + e4

        m2_1 = "S CREATING A HABITABLE ENVIRONMENT\n\n" + "S Humans have many basic needs\n"
        m2_2 = "S The Factors that Shaped Biometrics\n\n" + "S Identification has become more and more important in our society .\n"
        m2_3 = "S Engineers design products or systems that meet human needs .\n\n" + "S One current human need that should be given priority is the search for renewable resources .\n\n" + "S Everywhere in the world , fuel is used extensively .\n"
        m2_4 = "S Title : Obstacles for engineering design in China\n\n" + "S Engineering design is defined as a process that brings ideas or theories into physical representations which satisfies human needs .\n" + "A 16 17|||SVA|||satisfy|||REQUIRED|||-NONE-|||0\n" + "\n"

        m2_file_obj = StringIO.StringIO(m2_1 + '\n' + m2_2 + '\n' + m2_3 + '\n' + m2_4)

        expected_train_m2 = m2_1 + '\n' + m2_3 + '\n' + m2_4
        expected_devel_m2 = m2_2 + '\n'

        train_conll_file_obj = StringIO.StringIO()
        train_m2_file_obj = StringIO.StringIO()
        devel_conll_file_obj = StringIO.StringIO()
        devel_m2_file_obj = StringIO.StringIO()

        r = random.Random(1)

        er = EssayRandomiser.Randomiser(essay_file_obj, m2_file_obj, train_conll_file_obj, train_m2_file_obj, devel_conll_file_obj, devel_m2_file_obj, r)
        er.randomise()

        assert train_conll_file_obj.getvalue() == "".join(e1+['\n']+e3+['\n']+e4), "BEGIN\n" + "".join(e1+['\n']+e3+['\n']+e4) + "MID\n" + train_conll_file_obj.getvalue() + "END\n"
        assert train_m2_file_obj.getvalue() == expected_train_m2, "BEGIN\n" + train_m2_file_obj.getvalue() + "MID\n" + expected_train_m2 + "END\n"
        assert devel_conll_file_obj.getvalue() == "".join(e2+['\n']), "".join(e2+['\n']) + devel_conll_file_obj.getvalue()
        assert devel_m2_file_obj.getvalue() == expected_devel_m2, "BEGIN\n" + devel_m2_file_obj.getvalue() + "MID\n" + expected_devel_m2 + "END\n"

if __name__ == '__main__':
    unittest.main()
