# python import
import unittest
from datetime import date

# cfonb import
from cfonb.writer import transfert as w


class TestTransfert(unittest.TestCase):

    def test_empty_file(self):
        d = date(2011,10,14)
        a = w.Transfert()
        a.setEmeteurInfos('2000121','bigbrother','virement de test',503103,2313033,1212,d)
        res = a.render()
        want = '''0302        200012       141011bigbrother              viremen                   E     503102313033                                                   1212       
0802        200012                                                                                    0000000000000000                                          
'''
        assert res == want

    def test_one_line(self):
        d = date(2011,10,14)
        a = w.Transfert()
        a.setEmeteurInfos('2000121','bigbrother','virement de test',503103,2313033,1212,d)
        a.add('un test','littlebrother','credit agricole ile de france',50011,6565329000,100,'un peu d\'argent',6335)
        res = a.render()
        want = '''0302        200012       141011bigbrother              viremen                   E     503102313033                                                   1212       
0602        200012un test     littlebrother           credit agricole ile de f        50011656530000000000010000un peu d'argent                6335       
0802        200012                                                                                    0000000000010000                                          
'''
        assert res == want


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTransfert('test_empty_file'))
    suite.addTest(TestTransfert('test_one_line'))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())
