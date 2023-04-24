import mysql.connector
import bootkeys


class sqlServer:
    _sql = None

    # TODO make this table from file

    _path = ""
    _cur = None

    def insertRecord(self, sql, value):
        try:
            self._cur.execute(sql, value)
            self._sql.commit()
        except mysql.connector.Error as err:
            print("Failed to insert record: {}".format(err))

    def retrieveRecord(self, sql, value):
        try:
            self._cur.execute(sql, value)
            return self._cur.fetchall()
        except mysql.connector.Error as err:
            print("Failed to retrieve record: {}".format(err))



    def connectServer(self, h='localhost'):
        try:
            self._sql = mysql.connector.connect(
                host=h,
                user="root",
                password=bootkeys.db_password,
                database="mydb"
            )
            self._cur = self._sql.cursor()

            print("connected to database")
        except:
            print("failed to connect to  server")

    def __init__(self):
        self.connectServer()
