import MySQLdb
import MySQLdb.cursors
import config


def connect_to_database():
    options = {
        'host': config.env['host'],
        'user': config.env['user'],
        'passwd': config.env['password'],
        'db': config.env['db'],
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    db = MySQLdb.connect(**options)
    db.autocommit(True)
    return db

db = connect_to_database()




# from flask.ext.mysqldb import MySQL
# import MySQLdb.cursors
#
#
# # Create MySQL object. We create it here to avoid
# # circular dependencies that would occur if we created in
# # app.py
# mysql = MySQL()
#
# #converts sql results into python friendly dictionary -vicki
#
# def appQuery( query ):
# 	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cur.execute(query)
# 	result = cur.fetchall()
# 	return result
#
# #stuff that doesn't require a return value, and changes value of the database
# def appExec( query ):
# 	cnx = mysql.connection
# 	cur = cnx.cursor()
# 	cur.execute(query)
# 	cnx.commit()
#
# # def update_user_password(username, password):
# # 	appExec("UPDATE " + current_app.config['MYSQL_DB'] + ".User SET password = '" + password + "' WHERE username = '" + username + "'")
# #
# #
# # def create_new_user(username, firstname, lastname, password, email):
# # 	 appExec("INSERT INTO " + current_app.config['MYSQL_DB'] + ".User (username, firstname, lastname, password, email) VALUES ('" + username + "', '" + firstname +"', '" + lastname + "', '" + password + "', '" + email + "')")
#
