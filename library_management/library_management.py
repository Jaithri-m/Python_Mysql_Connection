import mysql.connector

class LibraryManager:

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="JAITHRIm2005@7736",
                database="library_management"
            )

            print("Connected successfully..!")

        except mysql.connector.Error as e:
            print(e)
            self.connection = None


    def create_table(self):
        cursor = None
        try:
            cursor = self.connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS books (
            book_id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR(100) NOT NULL,author VARCHAR(100),category VARCHAR(100),total_copies INT NOT NULL,available_copies INT NOT NULL
            )
            """

            cursor.execute(query)
            print("Table created successfully..!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()



    def post(self, **kwargs):
        cursor = None
        try:

            cursor = self.connection.cursor()

            query = """
                INSERT INTO books(title, author, category, total_copies, available_copies)VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                kwargs["title"],
                kwargs["author"],
                kwargs["category"],
                kwargs["total"],
                kwargs["available"],
            )

            cursor.execute(query, values)
            self.connection.commit()

            print("Book added successfully..!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()





    def get(self):
        cursor = None
        try:
            cursor = self.connection.cursor()

            query = """select * from books where available_copies >= 1 order by title ASC limit 20
            """

            cursor.execute(query)

            records = cursor.fetchall()

            if records:
                for record in records:
                    print(record)
            else:
                print("No available books found..!")

            return records

        except Exception as e:
            print(e)
            return []

        finally:
            if cursor:
                cursor.close()




    def search(self, search_text=None, category=None):
        cursor = None
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT * FROM books
                WHERE (
                cast(book_id as char) = %s or title like %s or author like %s
                )
            """

            search_value = f"%{search_text}%"

            values = [
                str(search_text),
                search_value,
                search_value
            ]

            if category:
                query += " AND category = %s"
                values.append(category)

            cursor.execute(query, values)

            records = cursor.fetchall()

            if records:
                for record in records:
                    print(record)
            else:
                print("no matching books found..!")

            return records

        except Exception as e:
            print(e)
            return []

        finally:
            if cursor:
                cursor.close()

    def put(self, book_id=None, **kwargs):
        cursor = None

        try:
            allowed_fields = {
                "title", "author", "category",
                "total_copies", "available_copies"
            }

            if not kwargs or not set(kwargs).issubset(allowed_fields):
                print("Invalid or empty update data..!")
                return

            cursor = self.connection.cursor()

            query = "SELECT total_copies FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))

            record = cursor.fetchone()

            if record is None:
                print("Book not found..!")
                return

            total_copies = kwargs.get("total_copies", record[0])
            available_copies = kwargs.get("available_copies")

            if available_copies is not None:
                if available_copies < 0:
                    print("Available copies cannot be negative..!")
                    return

                if available_copies > total_copies:
                    print("Available copies cannot exceed total copies..!")
                    return

            if total_copies < 0:
                print("Total copies cannot be negative..!")
                return

            placeholder = ""

            for k in kwargs.keys():
                placeholder += k + " = %s, "

            placeholder = placeholder.rstrip(", ")

            query = f"UPDATE books SET {placeholder} WHERE book_id = %s"

            values = list(kwargs.values())
            values.append(book_id)

            cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                print("Book updated successfully..!")
            else:
                print("No changes made..!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()


    def delete(self, book_id=None):
        cursor = None
        try:
            cursor = self.connection.cursor()

            query = "delete from books where book_id = %s"
            cursor.execute(query, (book_id,))
            self.connection.commit()

            if cursor.rowcount > 0:
                print("book deleted successfully..!")
            else:
                print("book not found..!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()



    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("connection closed..!")





library_instance = LibraryManager()


library_instance.create_table()

library_instance.post(title="php",author="json",category="Programming",total_copies=30,available_copies=25)

library_instance.get()

library_instance.search(search_text="java")

library_instance.search(search_text="php",category="Programming")

library_instance.put(book_id=1,title="Django",category="Programming",total_copies=50,available_copies=30)

library_instance.delete(book_id=14)

library_instance.close()
