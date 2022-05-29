from sqlite import cur


def get_number_day(day_name):
    return cur.execute('''SELECT id FROM days WHERE day = ?''', (day_name,)).fetchone()[0]