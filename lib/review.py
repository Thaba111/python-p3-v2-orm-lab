

class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value):
        if isinstance(value, int) and value >= 2000:
            self._year = value
        else:
            raise ValueError("Year must be an integer greater than or equal to 2000.")

    @property
    def summary(self):
        return self._summary
    
    @summary.setter
    def summary(self, value):
        if isinstance(value, str) and value.strip():
            self._summary = value
        else:
            raise ValueError("Summary must be a non-empty string.")

    @property
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self, value):
        if isinstance(value, int):
            self._employee_id = value
        else:
            raise ValueError("Employee ID must be an integer.")
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review

   
    @classmethod
    def instance_from_db(cls, row):
        """Return a Review instance having the attribute values from the table row."""
        # Create a Review instance with attribute values from the provided row
        review = cls(row[1], row[2], row[3], id=row[0])

        # Return the Review instance
        return review

   
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        # Perform a database query to retrieve the review with the specified ID
        sql = "SELECT * FROM reviews WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()

        # If a row is found, create a Review instance with the attribute values from the row
        if row:
            return cls.instance_from_db(row)
        else:
            return None  # If no row is found, return None

            

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        # Update the table row with the current attribute values of the Review instance
        sql = """
            UPDATE reviews
            SET year = ?,
                summary = ?,
                employee_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        # Delete the table row corresponding to the current Review instance from the database
        sql = "DELETE FROM reviews WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Remove the corresponding entry from the 'all' dictionary
        if self.id in self.all:
            del self.all[self.id]

        # Reassign the 'id' attribute to None
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        reviews = []

        # Retrieve all rows from the 'reviews' table
        sql = "SELECT * FROM reviews"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()

        # Create a Review instance for each row and add it to the list
        for row in rows:
            review = cls.instance_from_db(row)
            reviews.append(review)

        return reviews
        

from __init__ import CURSOR, CONN
from department import Department
from employee import Employee
