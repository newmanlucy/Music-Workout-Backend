import MySQLdb
import sys
import json

# Helper functions for dealing with the database

def open_operate_close(operation):
    """
    Handle database operations
    """
    # open connection and use the music_workout table
    conn = MySQLdb.connect(host="localhost", 
        user="root",
        passwd="",
        db="music_workout")
    cur = conn.cursor()
    cur.execute("USE music_workout")
    print('opened')

    # perform the operation
    ret = operation(cur)
    count = cur.rowcount

    # close the connection
    conn.commit()
    print('committed')
    conn.close()
    return ret, count

def op_execute_command(cur, cmd):
    """
    Execute a command
    """
    cur.execute(cmd)

def fetchonedict(cur):
    """
    return one result in dictionary
    """
    data = cur.fetchone()
    if data is None:
        return None
    desc = cur.description

    ret = {}

    for (name, value) in zip(desc, data):
        ret[name[0]] = value

    return ret


# Show columns in a table

def op_show_columns(cur, table):
    cmd = "SHOW COLUMNS FROM %s" % table
    op_execute_command(cur, cmd)
    cols = cur.fetchall()
    for col in cols:
        print("    %s: %s" % (col[0], col[1]))

def show_columns(table):
    open_operate_close(lambda cur: op_show_columns(cur, table))


# Show rows in table

def op_show_rows(cur, table):
    cmd = "SELECT * FROM %s" % table
    op_execute_command(cur, cmd)
    rows = cur.fetchall()
    for row in rows:
        row = map(str, row)
        rowstr = ", ".join(row)
        print(rowstr)

def show_rows(table):
    open_operate_close(lambda cur: op_show_rows(cur, table))

# List key facts about the database:
# - tables
# - table columns

def op_check_db(cur):
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    for ret_list in tables:
        print("---------")
        table = ret_list[0]
        print(table)
        show_columns(table)
        print("---")
        show_rows(table)

def check_db():
    open_operate_close(op_check_db)


# Create users table

def op_create_users_table(cur):
    cmd = """
        CREATE TABLE `users` (
        `user_id` int(11) NOT NULL AUTO_INCREMENT,
        `username` varchar(50) DEFAULT NULL,
        `age` int(11) DEFAULT NULL,
        PRIMARY KEY (`user_id`),
        UNIQUE KEY `username` (`username`)
    );"""
    op_execute_command(cur, cmd)

def create_users_table():
    open_operate_close(op_create_users_table)


# Create patterns table

def op_create_patterns_table(cur):
    cmd = """
        CREATE TABLE `patterns` (
        `pattern_id` int(11) NOT NULL AUTO_INCREMENT,
        `user_id` int(11) DEFAULT NULL,
        `pattern_vector` varchar(258) DEFAULT NULL,
        `def` tinyint(1) DEFAULT NULL,
        PRIMARY KEY (`pattern_id`),
        KEY `user_id` (`user_id`),
        CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
    );"""
    op_execute_command(cur, cmd)

def create_patterns_table():
    open_operate_close(op_create_patterns_table)


# Create workout-settings table

def op_create_workouts_table(cur):
    # id, pattern_id, date, min, max, duration, user_id
    cmd = """
          CREATE TABLE `workouts` (
          `workout_id` int(11) NOT NULL AUTO_INCREMENT,
          `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
          `min_hr` decimal(3,2) DEFAULT NULL,
          `max_hr` decimal(3,2) DEFAULT NULL,
          `duration` int(11) DEFAULT NULL,
          `pattern_id` int(11) DEFAULT NULL,
          `users_id_wk` int(11) DEFAULT NULL,
          PRIMARY KEY (`workout_id`),
          KEY `pattern_id` (`pattern_id`),
          KEY `users_id_wk` (`users_id_wk`),
          CONSTRAINT `pattern_id` FOREIGN KEY (`pattern_id`) REFERENCES `patterns` (`pattern_id`),
          CONSTRAINT `users_id_wk` FOREIGN KEY (`users_id_wk`) REFERENCES `users` (`user_id`)
    );"""
    op_execute_command(cur, cmd)

def create_workouts_table():
    open_operate_close(op_create_workouts_table)


# Add a column to a table

def op_add_column(cur, table, col_name, col_type, after):
    cmd = """
        ALTER TABLE %s
        ADD COLUMN %s %s
    """ % (table, col_name, col_type)
    if after is not None:
        cmd += "AFTER %s" % after
    op_execute_command(cur, cmd)

def add_column(table, col_name, col_type, after=None):
    open_operate_close(lambda cur: op_add_column(cur, table, col_name, col_type, after))


# Get the id of the last row added

def get_last_id(cur):
    cmd = "SELECT LAST_INSERT_ID()"
    cur.execute(cmd)
    last_id = cur.fetchone()[0]
    return last_id


# Add a user to the database

def op_add_user(cur, username, age):
    cmd = """
        INSERT INTO users
            (username, age)
        VALUES
            ('%s', %s)
        """ % (username, age)
    op_execute_command(cur, cmd)
    return #get_last_id(cur)

def add_user(username, age):
    user_id, count = open_operate_close(lambda cur: op_add_user(cur, username, age))
    return user_id


# Get a user from the database by username

def op_get_user(cur, username):
    cmd = "SELECT * FROM users WHERE username = '%s'" % username
    op_execute_command(cur, cmd)
    user = fetchonedict(cur)
    return user

def get_user(username):
    user, count = open_operate_close(lambda cur: op_get_user(cur, username))
    return user


# Delete a user from the database

def op_delete_user(cur, username):
    # TODO: delete associations with user once those are added
    cmd = "DELETE FROM users WHERE username = '%s'" % username
    op_execute_command(cur, cmd)

def delete_user(username):
    return open_operate_close(lambda cur: op_delete_user(cur, username))


# Add a pattern to the database

def op_add_pattern(cur, pattern, user_id, default):
    cmd = """
        INSERT INTO patterns
            (user_id, def, pattern_vector)
        VALUES
            (%d, %d, '%s')
    """ % (user_id, default, json.dumps(pattern))
    op_execute_command(cur, cmd)

def add_pattern(pattern, user_id, default=0):
    return open_operate_close(lambda cur: op_add_pattern(cur, pattern, user_id, default))


# Remove a pattern from the database

def op_delete_pattern(cur, pattern_id):
    cmd = "DELETE FROM patterns WHERE pattern_id = %d" % pattern_id
    op_execute_command(cur, cmd)

def delete_pattern(pattern_id):
    return open_operate_close(lambda cur: op_delete_pattern(cur, pattern_id))


# Get patterns for a user

def op_get_patterns(cur, user_id):
    cmd = """
        SELECT * FROM patterns
        WHERE user_id = %d
        OR def = TRUE
    """ % user_id
    cur.execute(cmd)
    patterns = cur.fetchall()
    return patterns

def get_patterns(user_id):
    return open_operate_close(lambda cur: op_get_patterns(cur, user_id))

# Add a workout-setting

def op_add_workout(cur, pattern_id, user_id, min_hr, max_hr, duration):
    cmd = """
        INSERT INTO workouts
            (min_hr, max_hr, duration, pattern_id, user_id)
        VALUES
            (%f, %f, %d, %d, %d)
    """ % (min_hr, max_hr, duration, pattern_id, user_id)
    op_execute_command(cur, cmd)

def add_workout(pattern_id, duration, min_hr=0.4, max_hr=0.6):
    return open_operate_close(lambda cur: op_add_pattern(cur, pattern_id, user_id, min_hr, max_hr, duration))

# Remove a workout-setting

def op_delete_workout(cur, workout_id):
    cmd = "DELETE FROM workouts WHERE workout_id = %d" % workout_id
    op_execute_command(cur, cmd)

def delete_workout(workout_id):
    return open_operate_close(lambda cur: op_delete_user(cur, workout_id))

# Get workout settings from user

def op_get_workouts(cur, user_id):
    cmd = """
        SELECT * FROM workouts
        WHERE user_id = %d
    """ % user_id
    cur.execute(cmd)
    workouts = cur.fetchall()
    return workouts

def get_workouts(user_id):
    return open_operate_close(lambda cur: op_get_patterns(cur, user_id))




# TODO:
# - create other tables (can use mysql directly)
# - add music, add music combination, add workout, add workout pattern
# - add music combination to user, add pattern to workout, add workout to user
# - remove music combination, workout
# - work on error messages
# - unit tests?
# - add routes


if __name__ == '__main__':
    check_db()
    # patterns, pattern_count = get_patterns(1)
    # for pattern in patterns:
    #     print("  %s" % json.dumps(pattern))
    # u = add_user("a", 10)
    # print(u, type(u))
    # # v = delete_user("a")
    # print(v, type(v))