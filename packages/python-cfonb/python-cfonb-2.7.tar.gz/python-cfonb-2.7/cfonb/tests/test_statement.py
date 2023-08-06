# python import - http://docs.python.org/library/unittest.html
import unittest
from datetime import date
from io import StringIO

from nose.tools import assert_is_not_none, assert_equal, assert_true

from parser.statement import StatementReader
from writer.statement import number_format, Statement


class TestStatement(unittest.TestCase):

    def test_render_parse_cfonb(self):
        content = Statement().header('20002', '90005', 'EUR', '01717651230', date(2011, 10, 14), 12345.67)\
                             .add('20002', '1234567', '90005', 'EUR', '01717651230', date(2011, 10, 14), 'label 1', 1234.56, 'reference1')\
                             .add('20002', '1234567', '90005', 'EUR', '01717651230', date(2011, 10, 13), 'label 2', 123.45, 'reference2')\
                             .render()
        print('content: {}'.format(content))
        reader = StatementReader()
        result = reader.parse(StringIO(content))
        for account in result:
            assert_is_not_none(account.account_nb)
            assert_equal(account.header.get('account_nb'), '01717651230')
            assert_equal(account.header.get('currency_code'), 'EUR')
            assert_equal(account.header.get('nb_of_dec'), '2')
            assert_equal(account.header.get('bank_code'), '20002')

    def test_number_format(self):
        assert_equal(number_format(123), '12C')
        assert_equal(number_format(123.45), '1234E')
        assert_equal(number_format(-123.45), '1234N')
        assert_equal(number_format(-12340), '1234}')
        assert_equal(number_format(12340), '1234{')
        assert_equal(number_format(None), '')
        assert_equal(number_format(''), '')

    def test_parse_with_original_content(self):
        content = '''0115589    29701EUR2 01717651230  220620AAAA BB CCCCC KERHHHH                             0000000352431O0000            
0415589    29701EUR2E01717651230B1230620  220620PRLV AAAAAA                             0 0000000000315}VOTRE ABONNEMENT
0515589    29701EUR2E01717651230B1230620     YYYXXXXXX                                                                  
0515589    29701EUR2E01717651230B1230620     LCCVOTRE ABONNEMENT FIXE  02XXXXX896 (FACTURE: XXXXX8960E2) - P            
0515589    29701EUR2E01717651230B1230620     ABC683551768 777888999E111E                                                
0515589    29701EUR2E01717651230B1230620     LIBPRELEVEMENTS SEPA DOMICILIES  
0715589    29701EUR2 01717651230  230620                                                  0000000352746O                '''
        reader = StatementReader()
        result = reader.parse(StringIO(content))
        assert_equal(len(result[0].lines), 1)
        assert_true(result[0].lines[0].get('origin').startswith('0415589    29701EUR2E01717651230B1230620  220620PRLV AAAAAA                             0 0000000000315}VOTRE ABONNEMENT'))
        assert_true(result[0].lines[0].get('origin').endswith('0515589    29701EUR2E01717651230B1230620     LIBPRELEVEMENTS SEPA DOMICILIES  '))
        assert_true(len(result[0].lines[0].get('origin').splitlines()) == 5)
        assert_true(len(result[0].lines[0].get('comment').splitlines()) == 4)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestStatement('test_render_parse_cfonb'))
    suite.addTest(TestStatement('test_number_format'))
    suite.addTest(TestStatement('test_parse_with_original_content'))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())
