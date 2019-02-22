#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python Lab1.py Sample_Song_Dataset.db

import sys
import sqlite3
import time


# The database file should be given as the first argument on the command line
# db_file = sys.argv[1]

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
    
    # 1. Find id, name and term of the artist who played the track with id TRMMWLD128F9301BF2
    trackid = ('TRMMWLD128F9301BF2',)
    cursor.execute('SELECT track_id, tracks.artist_id, artists.artist_name, artist_term.term FROM tracks '
                   'INNER JOIN artists ON artists.artist_id = tracks.artist_id '
                   'INNER JOIN artist_term ON artist_term.artist_id = artists.artist_id '
                   'WHERE track_id=?', trackid)
    print(cursor.fetchall())
    
    # 2. Select all the unique tracks with the duration is strictly greater than 3020 seconds.
    second = ('3020',)
    cursor.execute('SELECT DISTINCT * FROM tracks WHERE duration > ?', second)
    print(cursor.fetchall())
    
    # 3. Find the ten shortest (by duration) 10 tracks released between 2010 and 2014 (inclusive), 
    #    ordered by increasing duration.
    start = 2010
    end = 2014
    cursor.execute('SELECT track_id, year, duration FROM tracks '
                   'WHERE year BETWEEN ? and ? '
                   'ORDER BY duration ASC '
                   'LIMIT 10', (start, end))
    print(cursor.fetchall())

    # 4. Find the top 20 most frequently used terms, ordered by decreasing usage.
    cursor.execute('SELECT term, COUNT(term) as cnt FROM artist_term ' 
                   'GROUP BY term '
                   'ORDER BY cnt DESC '
                   'LIMIT 20')
    print(cursor.fetchall())

    # 5. Find the artist name associated with the longest track duration.
    cursor.execute('SELECT artist_name, tracks.duration FROM artists '
                   'INNER JOIN tracks ON artists.artist_id = tracks.artist_id '
                   'WHERE tracks.duration = (SELECT MAX(tracks.duration) FROM tracks)')
    print(cursor.fetchall())

    # 6. Find the mean duration of all tracks.
    cursor.execute('SELECT AVG(duration) FROM tracks')
    print(cursor.fetchall())

    # 7. Using only one query, count the number of tracks whose artists don't have any linked terms.
    cursor.execute('SElECT count(track_id) FROM tracks '
                   'LEFT JOIN artist_term ON artist_term.artist_id = tracks.artist_id '
                   'WHERE artist_term.term IS NULL')
    print(cursor.fetchall())
    
    # 8. Index- Run Question 1 query in a loop for 100 times and note the minimum time taken. 
    #    Now create an index on the column artist_id and compare the time. 
    #    Share your findings in the report.
    time_list = []
    for i in range(100):
        start = time.time()
        trackid = ('TRMMWLD128F9301BF2',)
        cursor.execute('SELECT track_id, tracks.artist_id, artists.artist_name, artist_term.term FROM tracks '
                       'INNER JOIN artists ON artists.artist_id = tracks.artist_id '
                       'INNER JOIN artist_term ON artist_term.artist_id = artists.artist_id '
                       'WHERE track_id=?', trackid)
        end = time.time()
        time_list.append(end-start)
    print('Min time of a round without index: {}'.format(min(time_list)))
    
    cursor.execute('CREATE INDEX idx_tracks ON tracks (artist_id)')
    cursor.execute('CREATE INDEX idx_artists ON artists (artist_id)')
    cursor.execute('CREATE INDEX idx_term ON artist_term (artist_id)')

    time_list_idx = []
    for i in range(100):
        start = time.time()
        trackid = ('TRMMWLD128F9301BF2',)
        cursor.execute('SELECT track_id, tracks.artist_id, artists.artist_name, artist_term.term FROM tracks '
                       'INNER JOIN artists ON artists.artist_id = tracks.artist_id '
                       'INNER JOIN artist_term ON artist_term.artist_id = artists.artist_id '
                       'WHERE track_id=?', trackid)
        end = time.time()
        time_list_idx.append(end-start)
    print('Min time of a round with index: {}'.format(min(time_list_idx)))
    
    # 9. Find all tracks associated with artists that have the tag eurovision winner 
    #    and delete them from the database, then roll back this query using a transaction. 
    #    Hint: you can select from the output of a select!
    cursor.execute('BEGIN ') 
    cursor.execute('SELECT COUNT(*) FROM tracks')
    print('Total rows of tracks table before delete: {}'.format(cursor.fetchall()[0][0]))
    tag = ('eurovision winner',)
    cursor.execute('DELETE FROM tracks '
                   'WHERE artist_id IN (SELECT artist_id FROM artist_term WHERE term=?)', tag)
    cursor.execute('SELECT COUNT(*) FROM tracks')
    print('Total rows of tracks table after delete: {}'.format(cursor.fetchall()[0][0]))
    cursor.execute('ROLLBACK')
    cursor.execute('SELECT COUNT(*) FROM tracks')
    print('Total rows of tracks table after rollback: {}'.format(cursor.fetchall()[0][0]))