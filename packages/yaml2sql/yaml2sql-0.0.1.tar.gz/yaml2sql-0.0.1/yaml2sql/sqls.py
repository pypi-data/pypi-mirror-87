#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: yaml2sqlit.cli
.. moduleauthor:: Bit-a-Bit <github@bit-a-bit.info>
"""
from ruamel.yaml import YAML

class StatementSQL():
    """Object that handles SQL statements."""

    def __init__(self, datamodel, sqldialect='sqlite'):
        """Create a new instance."""
        yaml = YAML(typ='safe')
        # TODO: multi-document
        self.datamodel = yaml.load(datamodel)
        self.sqldialect = sqldialect

    def __field_options_sql(self, foptions):
        """Translate field options to SQL."""
        s = ''
        if len(foptions) > 1:
            if 'autoincrement' in foptions:
                if foptions['autoincrement']:
                    s += ' IDENTITY(1,1)'
            if 'allows_null' in foptions:
                if not foptions['allows_null']:
                    s += ' NOT NULL'
            if 'is_primary_key' in foptions:
                if foptions['is_primary_key']:
                    s += ' PRIMARY KEY'
        return s

    @property
    def create_tables(self):
        """Creates the data model's SQL statement (CREATE TABLE ...)."""
        newline = '\n'
        doc = '-- CREATE TABLES\n'
        for tname, fields in self.datamodel.items():
            if not tname.startswith('.'):
                str_sql = 'CREATE TABLE {} ('.format(tname)
                inner_sql = '{fname} {dtype}{s}'
                s = [inner_sql.format(fname=field_name, dtype=foptions['data_type'],
                                    s=self.__field_options_sql(foptions))
                                    for field_name, foptions in fields['fields'].items()]
                s = ', '.join(s)
                str_sql += s + ');'
                doc += str_sql + newline
        return doc

    def add_datamodel(self, datamodel):
        """Adds a data model."""
        #TODO: multi-document
        pass
