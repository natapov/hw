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
        conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()

# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions


def create_tables() -> None:
    query = sql.SQL(
        """CREATE TABLE Custumers
        (
            cust_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )""")
    return execute_sql(query)


def clear_tables() -> None:
    # TODO: implement
    pass


def drop_tables() -> None:
    # TODO: implement
    pass


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    query = sql.SQL(
        f"""INSERT INTO Customers(cust_id, full_name, phone, address) 
        VALUES(
            {customer.get_cust_id}, 
            {customer.get_full_name},
            {customer.get_phone},
            {customer.get_address}
        )"""
    )
    return execute_sql(query)


def get_customer(customer_id: int) -> Customer:
    # TODO: implement
    pass


def delete_customer(customer_id: int) -> ReturnValue:
    # TODO: implement
    pass

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
