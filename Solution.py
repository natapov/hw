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

def i(val):
    if val is None:
        return 'NULL'
    return sql.Literal(int(val))

def s(val):
    if val is None:
        return 'NULL'
    return sql.Literalstr(val)

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
        )""")
    rv, _, _ =  execute_sql(query)
    return rv


def clear_tables() -> None:
    # TODO: implement
    pass


def drop_tables() -> None:
    query = sql.SQL("DROP TABLE IF EXISTS Customers, Orders CASCADE")
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
    query = sql.SQL("DELETE FROM Customers WHERE cust_id={0}").format(sql.Literal(customer_id))
    rv, rows,_ = execute_sql(query)
    if rows == 0:
        return ReturnValue.NOT_EXISTS
    return rv

def add_order(order: Order) -> ReturnValue:
    # TODO: implement
    pass

def get_order(order_id: int) -> Order:
    # TODO: implement
    pass

def delete_order(order_id: int) -> ReturnValue:
    # TODO: implement
    pass

def add_dish(dish: Dish) -> ReturnValue:
    # TODO: implement
    pass

def get_dish(dish_id: int) -> Dish:
    # TODO: implement
    pass

def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    # TODO: implement
    pass

def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    # TODO: implement
    pass

def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    # TODO: implement
    pass

def get_customer_that_placed_order(order_id: int) -> Customer:
    # TODO: implement
    pass


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    # TODO: implement
    pass


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass


def get_all_order_items(order_id: int) -> List[OrderDish]:
    # TODO: implement
    pass


def customer_likes_dish(cust_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass


def customer_dislike_dish(cust_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass

def get_all_customer_likes(cust_id: int) -> List[Dish]:
    # TODO: implement
    pass
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    # TODO: implement
    pass


def get_max_amount_of_money_cust_spent(cust_id: int) -> float:
    # TODO: implement
    pass


def get_most_expensive_anonymous_order() -> Order:
    # TODO: implement
    pass


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
