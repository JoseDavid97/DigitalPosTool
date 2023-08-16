import mysql.connector, configparser

class PDO:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('source/settings.ini')
        dbconfig = config['DBConfig']
        
        self.mydb = mysql.connector.connect(
                                        host=dbconfig['dbhost'],
                                        user=dbconfig['dbuser'],
                                        password=dbconfig['dbpswd'],
                                        database=dbconfig['dbname'],
                                        )

    def saveBill(self, price, date):
        cursor = self.mydb.cursor()

        Y, M, D, H, Mi, S = date.year, date.month, date.day, date.hour, date.minute, date.second
        PK = f"{Y}-{M}-{D} {H}:{Mi}:{S}"
        setBill = f"INSERT INTO transactions (trsid, trsdate, trsvalue) VALUES ('{PK}', '{date}', {price})"

        cursor.execute(setBill)
        self.mydb.commit()

    def getRecords(self, fromStr, toStr):
    
        cursor = self.mydb.cursor()
        sql = f"SELECT * FROM transactions WHERE trsdate BETWEEN '{fromStr}' AND '{toStr}'"
        cursor.execute(sql)
        fData = cursor.fetchall()
        return fData
    
    def getGroupedRecords(self, fromStr, toStr):

        cursor = self.mydb.cursor()
        sql = f"""SELECT SUM(trsvalue), date_format(trsdate, '%d / %M / %Y  %h %p') as dtf 
                  FROM transactions WHERE trsdate BETWEEN '{fromStr}' AND '{toStr}'
                  GROUP BY DATE(trsdate), HOUR(trsdate) ORDER BY trsdate"""
        
        cursor.execute(sql)
        fData = cursor.fetchall()
        return fData
    
    def editRecord(self, PK, newvalue):
        cursor = self.mydb.cursor()
        sql = f"UPDATE transactions SET trsvalue={newvalue} WHERE trsid='{PK}'"
        cursor.execute(sql)
        self.mydb.commit()

    def delRecord(self, PK):
        cursor = self.mydb.cursor()
        sql = f"DELETE FROM transactions WHERE trsid='{PK}'"
        cursor.execute(sql)
        self.mydb.commit()