from typing import List, Tuple
from psycopg2 import sql
from datetime import date, datetime
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish

def execute_sql(query):
    conn = None
    try:
        conn = Connector.DBConnector()
        rows, result = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        return ReturnValue.ERROR, None, None
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS, None, None
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS, None, None
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS, None, None
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.NOT_EXISTS, None, None
    except Exception as e:
        print(e)
        return ReturnValue.ERROR, None, None
    finally:
        conn.close()
    return ReturnValue.OK, rows, result

# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions

def create_tables() -> None:
    drop_tables()
    query = sql.SQL(
        """CREATE TABLE Customers
        (
            cust_id INTEGER PRIMARY KEY CHECK(cust_id > 0),
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL CHECK(LENGTH(address) > 2)
        );
        CREATE TABLE Orders
        (
            order_id INTEGER PRIMARY KEY CHECK(order_id > 0),
            date TIMESTAMP(0)
        );
        CREATE TABLE Order_Makers
        (   
            order_id INTEGER PRIMARY KEY,
            cust_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (cust_id) REFERENCES Customers(cust_id)
        );
        CREATE TABLE Dishes 
        (
            dish_id INTEGER PRIMARY KEY CHECK(dish_id > 0),
            name TEXT NOT NULL CHECK(LENGTH(name) >= 3),
            price DECIMAL NOT NULL CHECK(price > 0),
            is_active BOOLEAN NOT NULL
        );
        CREATE TABLE Order_Dishes
        (   
            order_id INTEGER,
            dish_id INTEGER,
            PRIMARY KEY (order_id, dish_id),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
            price DECIMAL NOT NULL CHECK(price > 0),
            amount INTEGER NOT NULL CHECK(amount > 0)
        );
        CREATE TABLE Likes
        (
            cust_id INTEGER,
            dish_id INTEGER,
            PRIMARY KEY (cust_id, dish_id),
            FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
            FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id)
        );
        CREATE VIEW Order_Total_Price AS
            SELECT order_id, SUM(price) as total_price
            FROM Order_Dishes
            GROUP BY order_id;
        """)
    rv, _, _ =  execute_sql(query)
    return rv


def clear_tables() -> None:
    query = sql.SQL("""DELETE FROM Customers;
                    DELETE FROM Orders;
                    DELETE FROM Dishes;
                    DELETE FROM Order_Makers;
                    DELETE FROM Order_Dishes;
                    DELETE FROM Likes;""")
    rv, _, _ = execute_sql(query)
    return rv


def drop_tables() -> None:
    query = sql.SQL("""DROP TABLE IF EXISTS Customers, Orders, Dishes, Order_Makers, Order_Dishes, Likes CASCADE;
                    DROP VIEW IF EXISTS my_cust_id, dish_price, Order_Total_Price;""")
    rv, _, _ = execute_sql(query)
    return rv


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    query = sql.SQL("INSERT INTO Customers(cust_id, full_name, phone, address) VALUES({0},{1},{2},{3})")
    query = query.format(
        sql.Literal(customer.get_cust_id()),
        sql.Literal(customer.get_full_name()),
        sql.Literal(customer.get_phone()),
        sql.Literal(customer.get_address())
    )
    rv, _, _ = execute_sql(query)
    return rv

def get_customer(customer_id: int) -> Customer:
    query = sql.SQL("SELECT * FROM Customers WHERE cust_id={0}").format(sql.Literal(customer_id))
    rv, rows, result  = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return BadCustomer()
    return Customer(
        cust_id=result['cust_id'][0],
        full_name=result['full_name'][0],
        phone=result['phone'][0],
        address=result['address'][0]
    )

def delete_customer(customer_id: int) -> ReturnValue:
    query = sql.SQL(
        """DELETE FROM Likes WHERE cust_id={0};
        DELETE FROM Order_Makers WHERE cust_id={0};
        DELETE FROM Customers WHERE cust_id={0};
        """).format(sql.Literal(customer_id))
    rv, rows,_ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def add_order(order: Order) -> ReturnValue:
    query = sql.SQL("INSERT INTO Orders(order_id, date) VALUES({0},{1})")
    query = query.format(
        sql.Literal(order.get_order_id()),
        sql.Literal(order.get_datetime().strftime("%Y-%m-%d %H:%M:%S")),
    )
    rv, _, _ = execute_sql(query)
    return rv

def get_order(order_id: int) -> Order:
    query = sql.SQL("SELECT * FROM Orders WHERE order_id={0}").format(sql.Literal(order_id))
    rv, rows, result  = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return BadOrder()
    return Order(
        order_id=result['order_id'][0],
        date=result['date'][0]
        #date=datetime.strptime(result['date'][0], "%Y-%m-%d %H:%M:%S")
    )
def delete_order(order_id: int) -> ReturnValue:
    q1 = sql.SQL("DELETE FROM Order_Makers WHERE order_id={0};").format(sql.Literal(order_id))
    q2 = sql.SQL("DELETE FROM Order_Dishes WHERE order_id={0};").format(sql.Literal(order_id))
    q3 = sql.SQL("DELETE FROM Orders WHERE order_id={0};").format(sql.Literal(order_id))
    rv, _, _ = execute_sql(q1)
    if rv != ReturnValue.OK:
        return rv
    rv, _, _ = execute_sql(q2)
    if rv != ReturnValue.OK:
        return rv
    rv, rows, _ = execute_sql(q3)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def add_dish(dish: Dish) -> ReturnValue:
    query = sql.SQL("INSERT INTO Dishes(dish_id, name, price, is_active) VALUES({0},{1},{2},{3})")
    query = query.format(
        sql.Literal(dish.get_dish_id()),
        sql.Literal(dish.get_name()),
        sql.Literal(dish.get_price()),
        sql.Literal(dish.get_is_active())
    )
    rv, _, _ = execute_sql(query)
    return rv

def get_dish(dish_id: int) -> Dish:
    query = sql.SQL("SELECT * FROM Dishes WHERE dish_id={0}").format(sql.Literal(dish_id))
    rv, rows, result  = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return BadDish()
    return Dish(
        dish_id=result['dish_id'][0],
        name=result['name'][0],
        price=float(result['price'][0]),
        is_active=result['is_active'][0],
    )

def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    query = sql.SQL(
        """UPDATE Dishes
        SET price = {1}
        WHERE dish_id = {0}
        AND is_active = TRUE;
        """)
    query = query.format(
        sql.Literal(dish_id),
        sql.Literal(price),
        )
    rv, rows,_ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    query = sql.SQL(
        """UPDATE Dishes
        SET is_active = {1}
        WHERE dish_id = {0};
        """)
    query = query.format(
        sql.Literal(dish_id),
        sql.Literal(is_active),
        )
    rv, rows,_ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    query = sql.SQL("INSERT INTO Order_Makers(order_id, cust_id) VALUES({0},{1})").format(
        sql.Literal(order_id),
        sql.Literal(customer_id))
    rv, _, _  = execute_sql(query)
    return rv

def get_customer_that_placed_order(order_id: int) -> Customer:
    
    query = sql.SQL("""DROP VIEW IF EXISTS my_cust_id;
                    CREATE VIEW my_cust_id AS 
                        SELECT cust_id 
                        FROM Order_Makers 
                        WHERE order_id={0};
                    SELECT * 
                    FROM Customers
                    WHERE cust_id=(select cust_id from my_cust_id);
                    """).format(sql.Literal(order_id))
    rv, rows, result  = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return BadCustomer()
    return Customer(
        cust_id=result['cust_id'][0],
        full_name=result['full_name'][0],
        phone=result['phone'][0],
        address=result['address'][0]
    )


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    query = sql.SQL(
    """SELECT price
        FROM Dishes
        WHERE dish_id={0} AND is_active=TRUE"""
    )
    query = query.format(sql.Literal(dish_id))
    rv, rows, result  = execute_sql(query)

    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    price = float(result['price'][0])
    query = sql.SQL(
        """INSERT INTO Order_Dishes(order_id, dish_id, amount, price) VALUES({0},{1},{2},{3});""")
    query = query.format(
        sql.Literal(order_id),
        sql.Literal(dish_id),
        sql.Literal(amount),
        sql.Literal(price)
    )
    rv, _, _  = execute_sql(query)
    return rv


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    query = sql.SQL("DELETE FROM Order_Dishes WHERE order_id={0} and dish_id ={0}")
    query = query.format(
        sql.Literal(order_id),
        sql.Literal(dish_id)
    )
    rv, rows, _ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def get_all_order_items(order_id: int) -> List[OrderDish]:
    query = sql.SQL("SELECT dish_id, price, amount FROM ORDER_DISHES WHERE order_id={0} ORDER BY dish_id ASC").format(
        sql.Literal(order_id))
    rv, rows, result = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    dishes = []
    for i in range(rows):
        dish = OrderDish(result[i]['dish_id'], result[i]['amount'], result[i]['price'])
        dishes.append(dish)
    return dishes

def customer_likes_dish(cust_id: int, dish_id: int) -> ReturnValue:
    query = sql.SQL("""INSERT INTO Likes(cust_id, dish_id) VALUES({0}, {1})""").format(
        sql.Literal(cust_id),
        sql.Literal(dish_id)
    )
    rv, _, _ = execute_sql(query)
    return rv

def customer_dislike_dish(cust_id: int, dish_id: int) -> ReturnValue:
    query = sql.SQL("DELETE FROM Likes WHERE cust_id={0} and dish_id={1}").format(
        sql.Literal(cust_id),
        sql.Literal(dish_id)
    )
    rv, rows, _ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def get_all_customer_likes(cust_id: int) -> List[Dish]:
    query = sql.SQL("""SELECT Dishes.dish_id, name, price, is_active 
                    FROM Likes, Dishes
                    WHERE Likes.dish_id=Dishes.dish_id and cust_id={0}""").format(
                    sql.Literal(cust_id))
    dishes = []
    rv, rows, result = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    for i in range(rows):
        liked_dish = Dish(
            result[i]['dish_id'],
            result[i]['name'],
            result[i]['price'],
            result[i]['is_active']
        )
        dishes.append(liked_dish)
    return dishes
    
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    query = sql.SQL("SELECT total_price FROM Order_Total_Price WHERE order_id={id}").format(
                    id=sql.Literal(order_id))
    rv, rows, results = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return 0
    return float(results[0]['total_price'])


def get_max_amount_of_money_cust_spent(cust_id: int) -> float:
    query = sql.SQL("""SELECT total_price FROM Order_Makers, Order_Total_Price
                    WHERE Order_Total_Price.order_id=Order_Makers.order_id
                    and Order_Makers.cust_id={customer_id}
                    ORDER BY total_price ASC""").format(customer_id=sql.Literal(cust_id))
    rv, rows, results = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        return 0
    return float(results[0]['total_price'])
        

def get_most_expensive_anonymous_order() -> Order:
    query = sql.SQL("""SELECT Orders.order_id, date 
                        FROM Orders, Order_Total_Price
                        WHERE Orders.order_id=Order_Total_Price.order_id
                        and Orders.order_id NOT IN ( SELECT order_id FROM Order_Makers )
                        ORDER BY Order_Total_Price.total_price DESC, Orders.order_id ASC""")
    rv, rows, results = execute_sql(query)
    if rv != ReturnValue.OK:
        return rv
    if rows == 0:
        None
    return Order(order_id=results[0]['Orders.order_id'], date=results[0]['date'])


def is_most_liked_dish_equal_to_most_purchased() -> bool:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_ordered_top_5_dishes() -> List[int]:
    # TODO: implement
    pass


def get_non_worth_price_increase() -> List[int]:
    # TODO: implement
    pass


def get_total_profit_per_month(year: int) -> List[Tuple[int, float]]:
    # TODO: implement
    pass


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    # TODO: implement
    pass
