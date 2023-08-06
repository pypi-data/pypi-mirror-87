BR_LINE = '\n'


def write(input_, length, rpad=False, fill_char=' '):
    input_ = str(input_)
    if (rpad):
        return input_.rjust(length, fill_char)[:length]
    else:
        return input_.ljust(length, fill_char)[:length]


def save(header, body, footer, filename=None):
    content  = header
    content += body
    content += footer
    if filename is not None:
        f = open(filename,'w')
        f.write(content)
        f.close()
    return content


def date_format(date):
    return date.strftime(format='%d%m') + date.strftime(format='%y')
