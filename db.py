import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="cis3368summer.ct0yuaeka9ej.us-east-1.rds.amazonaws.com",
        user="admin",
        password="1234567890",
        database="senior_facility"
    )
