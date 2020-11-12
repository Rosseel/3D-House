import os
import zipfile

import psycopg2


def unzip():
    for folder, dirs, files in os.walk("/home/techpriest/Desktop/becode/SpaceEYE/DSM", topdown=False):
        for name in files:
            print(name)
            if name.endswith(".zip"):
                # print(os.path.join(folder, name))
                # unzip to folder and delete the zip file
                os.chdir(folder)
                print("folder",folder)
                print("name",name)
                zip_file = zipfile.ZipFile(os.path.join(folder, name))
                zip_file.extractall()
                zip_file.close()
                os.remove(os.path.join(folder, name))


def create_db():
    try:
        connection = psycopg2.connect(user="techpriest",
                                      password="root",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="techpriest")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE mobile
                  (ID INT PRIMARY KEY     NOT NULL,
                  MODEL           TEXT    NOT NULL,
                  PRICE         REAL); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

create_db()