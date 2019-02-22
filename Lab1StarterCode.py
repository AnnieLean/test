#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python Lab1.py Sample_Song_Dataset.db

import sys
import sqlite3


# The database file should be given as the first argument on the command line
db_file = sys.argv[1]

# We connect to the database using 
with sqlite3.connect('Sample_Song_Dataset.db') as conn:
    # We use a "cursor" to mark our place in the database.
    # We could use multiple cursors to keep track of multiple
    # queries simultaneously.
    cursor = conn.cursor()

    # This query counts the number of tracks from the year 1998
    year = ('1998',)
    cursor.execute('SELECT count(*) FROM tracks WHERE year=?', year)

    # Since there is no grouping here, the aggregation is over all rows
    # and there will only be one output row from the query, which we can
    # print as follows:
    print('Tracks from {}: {}'.format(year[0], cursor.fetchone()[0]))
    # The [0] bits here tell us to pull the first column out of the 'year' tuple
    # and query results, respectively.

    # ADD YOUR CODE STARTING HERE
