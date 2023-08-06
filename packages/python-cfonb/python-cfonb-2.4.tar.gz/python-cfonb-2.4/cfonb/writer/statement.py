# coding: UTF-8

"""
This file is part of CFONB.

CFONB is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with CFONB.  If not, see <http://www.gnu.org/licenses/>.

 Coryright 2020, Dhatim
 Créer un fichier d'opérations bancaires avec
  - l'entête (01)
  - ligne détail (04)
  - ligne total (facultative)

"""
from cfonb.writer.common import write, date_format, save, BR_LINE

LAST_LETTER_NUMBER = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I',
                 '-1': 'J', '-2': 'K', '-3': 'L', '-4': 'M', '-5': 'N', '-6': 'O', '-7': 'P', '-8': 'Q', '-9': 'R',
                 '0': '{', '-0': '}'}


class Statement(object):
    def __init__(self):
        self._header = {}
        self._content = []
        self._footer = {}

    def header(self, bank_code, agency_code, currency, account_number, date, amount):
        self._header['bank_code'] = bank_code
        self._header['agency_code'] = agency_code
        self._header['currency'] = currency
        self._header['account_number'] = account_number
        self._header['date'] = date
        self._header['amount'] = amount
        return self

    def footer(self, bank_code, agency_code, currency, account_number, date, amount):
        self._footer['bank_code'] = bank_code
        self._footer['agency_code'] = agency_code
        self._footer['currency'] = currency
        self._footer['account_number'] = account_number
        self._footer['date'] = date
        self._footer['amount'] = amount
        return self

    def add(self, bank_code, operation_code, agency_code, currency,
            account_number, date, label, amount, reference):
        line = write('04', 2)
        line += write(bank_code, 5)
        line += write(operation_code, 4)
        line += write(agency_code, 5)
        line += write(currency, 3)
        line += write('2', 1) # number of decimal
        line += write(' ', 1) # SIT code
        line += write(account_number, 11)
        line += write('08', 2) # interbank code
        line += write(date_format(date), 6)
        line += write('  ', 2) # rejected code
        line += write(date_format(date), 6)
        line += write(label, 31)
        line += write('  ', 2) # reserve zone
        line += write('       ', 7) # entry writing code
        line += write(' ', 1) # exoneration code
        line += write(' ', 1)  # reserve zone
        line += write(number_format(amount), 14, rpad=True, fill_char='0')
        line += write(reference, 16)
        self._content.append(line)
        return self

    def render(self, filename=None):
        return save(self._render_header(), BR_LINE.join(self._content) + BR_LINE, self._render_footer(), filename)

    def _render_header(self):
        if self._header:
            line = write('01', 2)
            line += write(self._header['bank_code'], 5)
            line += write('    ', 4) # reserved zone
            line += write(self._header['agency_code'], 5)
            line += write(self._header['currency'], 3)
            line += write('2', 1) # number of decimal
            line += write(' ', 1)  # reserved zone
            line += write(self._header['account_number'], 11)
            line += write('  ', 2)  # reserved zone
            line += write(date_format(self._header['date']), 6)
            line += write(' ', 50)  # reserved zone
            line += write(number_format(self._header['amount']), 14, rpad=True, fill_char='0')
            line += write(' ', 16)  # reserved zone
            return line + BR_LINE
        return ''

    def _render_footer(self):
        if self._footer:
            line = write('07', 2)
            line += write(self._footer['bank_code'], 5)
            line += write('    ', 4) # reserved zone
            line += write(self._footer['agency_code'], 5)
            line += write(self._footer['currency'], 3)
            line += write('2', 1) # number of decimal
            line += write(' ', 1)  # reserved zone
            line += write(self._footer['account_number'], 11)
            line += write('  ', 2)  # reserved zone
            line += write(date_format(self._footer['date']), 6)
            line += write(' ', 50)  # reserved zone
            line += write(number_format(self._footer['amount']), 14, rpad=True, fill_char='0')
            line += write(' ', 16)  # reserved zone
            return line + BR_LINE
        return ''


def number_format(number):
    if not number:
        return ''

    _number = str(number).replace('.', '')
    _number = _number.replace('-', '')
    last_number = _number[-1]
    if number < 0:
        last_number = '-' + last_number
    return _number[0:len(_number) - 1] + LAST_LETTER_NUMBER.get(last_number)
