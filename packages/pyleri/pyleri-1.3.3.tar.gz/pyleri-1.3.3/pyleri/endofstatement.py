'''end_of_statement Variable.

end_of_statement is an instance of _EndOfStatement and will be added to
an 'expecting' in a node result when an 'End of Statement' is possible.

:copyright: 2018, Jeroen van der Heijden (Transceptor Technology)
'''


class _EndOfStatement:

    def __repr__(self):
        return 'end_of_statement'


end_of_statement = _EndOfStatement()
