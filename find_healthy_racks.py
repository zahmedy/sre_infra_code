from collections.abc import Iterable
from datetime import datetime
import re
import sqlite3

def find_unhealthy_racks(events: Iterable[str], threshold: int) -> list[str]:
    conn = sqlite3.connect("racks_state.db")
    cursor = conn.cursor()

    # Create an index on host for instantaneous lookups
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hosts (
            host TEXT PRIMARY KEY,
            timestamp INTEGER,
            rack TEXT,
            stat TEXT
        )
    ''')

    cursor.execute("DELETE FROM hosts")
    conn.commit()
    pattern = re.compile(
        r"(?P<date>^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)\s+"
        r"(?P<host>host-[0-9]+)\s+"
        r"(?P<rack>rack-[a-z]+)\s+"
        r"(?P<stat>UP|DOWN)$"
    )

    counter = 0
    for event in events:
        counter += 1
        match = pattern.fullmatch(event)

        date, host, rack, stat = None, None, None, None
        if not match:
            continue

        try:
            date = datetime.fromisoformat(match.group('date'))
            timestamp = int(date.timestamp())
        except ValueError:
            continue
        host = match.group('host')
        rack = match.group('rack')
        stat = match.group('stat')
        
        cursor.execute(
            """
            INSERT INTO hosts (host, timestamp, rack, stat)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(host) DO UPDATE SET
                rack = excluded.rack,
                stat = excluded.stat,
                timestamp = excluded.timestamp
            WHERE excluded.timestamp > hosts.timestamp
            OR (
                excluded.timestamp = hosts.timestamp
                AND excluded.stat = 'DOWN'
                AND hosts.stat = 'UP'
            )
            """,
            (host, timestamp, rack, stat),
        )
        if counter >= 100_000:
            conn.commit()
            counter = 0

    conn.commit()
    cursor.execute('''
        SELECT rack, COUNT(*)
        FROM hosts
        WHERE stat = 'DOWN'
        GROUP BY rack
        HAVING COUNT(*) >= ?
    ''', (threshold,))

    results = [row[0] for row in cursor.fetchall()]

    conn.close()

    return sorted(results)