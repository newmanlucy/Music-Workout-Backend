import MySQLdb


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

    # perform the operation
    operation(cur)

    # close the connection
    conn.commit()
    conn.close()

def op_execute_command(cur, cmd):
    """
    Execute a command
    """
    cur.execute(cmd)


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
# - rowcount
# - tables
# - table columns

def op_check_db(cur):
    numrows = cur.rowcount
    print("numrows: %d" % numrows)

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


# Create user table

def op_create_users_table(cur):
    cmd = """
        CREATE TABLE users (
            user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50)
        );
        """
    op_execute_command(cur, cmd)

def create_users_table():
    open_operate_close(op_create_users_table)


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


# Add a user to the database

def op_add_user(cur, username, age):
    cmd = """
        INSERT INTO users 
            (username, age)
        VALUES
            ('%s', %d) 
        """ % (username, age)
    op_execute_command(cur, cmd)

def add_user(username, age):
    open_operate_close(lambda cur: op_add_user(cur, username, age))


# TODO:
# - create other tables (can use mysql directly)
# - add music, add music combination, add workout, add workout pattern
# - add music combination to user, add pattern to workout, add workout to user
# - remove music combination, workout
# - work on error messages
# - unit tests?
# - add routes


if __name__ == '__main__':
    add_user("cho yin", 21)
    check_db()
