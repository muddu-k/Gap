import cx_Oracle
import getpass
db_user=input("Enter CAWA DB user:")
db_passwd=getpass.getpass("CAWA DB password")
cawadbconn=cx_Oracle.connect()