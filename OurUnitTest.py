import unittest
from datetime import datetime
from Business.Customer import Customer
from Business.Order import Order
from Business.Dish import Dish
from Business.OrderDish import OrderDish
from Solution import *

class TestYummy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

    @classmethod
    def tearDownClass(cls):
        drop_tables()

    def setUp(self):
        clear_tables()

    def test_add_customer(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        result = add_customer(customer)
        self.assertEqual(result, ReturnValue.OK)

    def test_add_customer_invalid(self):
        customer = Customer(1, "John Doe", "123456789", "12")
        result = add_customer(customer)
        self.assertEqual(result, ReturnValue.BAD_PARAMS)

    def test_get_customer(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        retrieved_customer = get_customer(1)
        self.assertEqual(retrieved_customer.get_cust_id(), 1)
        self.assertEqual(retrieved_customer.get_full_name(), "John Doe")

    def test_delete_customer(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        result = delete_customer(1)
        self.assertEqual(result, ReturnValue.OK)
        retrieved_customer = get_customer(1)
        self.assertIsInstance(retrieved_customer, BadCustomer)

    def test_add_order(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        result = add_order(order)
        self.assertEqual(result, ReturnValue.OK)

    def test_get_order(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        retrieved_order = get_order(1)
        self.assertEqual(retrieved_order.get_order_id(), 1)
        self.assertEqual(retrieved_order.get_datetime(), datetime(2023, 5, 6, 14, 30, 0))

    def test_delete_order(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        result = delete_order(1)
        self.assertEqual(result, ReturnValue.OK)
        retrieved_order = get_order(1)
        self.assertIsInstance(retrieved_order, BadOrder)

    def test_add_dish(self):
        dish = Dish(1, "Pizza", 10.0, True)
        result = add_dish(dish)
        self.assertEqual(result, ReturnValue.OK)

    def test_get_dish(self):
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        retrieved_dish = get_dish(1)
        self.assertEqual(retrieved_dish.get_dish_id(), 1)
        self.assertEqual(retrieved_dish.get_name(), "Pizza")

    def test_update_dish_price(self):
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        result = update_dish_price(1, 12.0)
        self.assertEqual(result, ReturnValue.OK)
        retrieved_dish = get_dish(1)
        self.assertEqual(retrieved_dish.get_price(), 12.0)

    def test_update_dish_active_status(self):
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        result = update_dish_active_status(1, False)
        self.assertEqual(result, ReturnValue.OK)
        retrieved_dish = get_dish(1)
        self.assertFalse(retrieved_dish.get_is_active())

    def test_customer_placed_order(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        result = customer_placed_order(1, 1)
        self.assertEqual(result, ReturnValue.OK)

    def test_get_customer_that_placed_order(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        customer_placed_order(1, 1)
        retrieved_customer = get_customer_that_placed_order(1)
        self.assertEqual(retrieved_customer.get_cust_id(), 1)

    def test_order_contains_dish(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        result = order_contains_dish(1, 1, 2)
        self.assertEqual(result, ReturnValue.OK)

    def test_order_does_not_contain_dish(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        order_contains_dish(1, 1, 2)
        result = order_does_not_contain_dish(1, 1)
        self.assertEqual(result, ReturnValue.OK)

    def test_get_all_order_items(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        order_contains_dish(1, 1, 2)
        order_contains_dish(1, 2, 1)
        items = get_all_order_items(1)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].get_dish_id(), 1)
        self.assertEqual(items[1].get_dish_id(), 2)

    def test_customer_likes_dish(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        result = customer_likes_dish(1, 1)
        self.assertEqual(result, ReturnValue.OK)

    def test_customer_dislike_dish(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        dish = Dish(1, "Pizza", 10.0, True)
        add_dish(dish)
        customer_likes_dish(1, 1)
        result = customer_dislike_dish(1, 1)
        self.assertEqual(result, ReturnValue.OK)

    def test_get_all_customer_likes(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        customer_likes_dish(1, 1)
        customer_likes_dish(1, 2)
        likes = get_all_customer_likes(1)
        self.assertEqual(len(likes), 2)
        self.assertEqual(likes[0].get_dish_id(), 1)
        self.assertEqual(likes[1].get_dish_id(), 2)

    def test_get_order_total_price(self):
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        order_contains_dish(1, 1, 2)
        order_contains_dish(1, 2, 1)
        total_price = get_order_total_price(1)
        self.assertEqual(total_price, 32.0)

    def test_get_max_amount_of_money_cust_spent(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        self.assertEqual(add_customer(customer), ReturnValue.OK)

        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 30, 0))
        self.assertEqual(add_order(order1), ReturnValue.OK)
        self.assertEqual(add_order(order2), ReturnValue.OK)

        self.assertEqual(customer_placed_order(1, 1), ReturnValue.OK)
        self.assertEqual(customer_placed_order(1, 2), ReturnValue.OK)

        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        self.assertEqual(add_dish(dish1), ReturnValue.OK)
        self.assertEqual(add_dish(dish2), ReturnValue.OK)

        self.assertEqual(order_contains_dish(1, 1, 2), ReturnValue.OK)
        self.assertEqual(order_contains_dish(2, 2, 1), ReturnValue.OK)

        max_spent = get_max_amount_of_money_cust_spent(1)
        self.assertEqual(max_spent, 20.0)

    def test_get_most_expensive_anonymous_order(self):
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 30, 0))
        add_order(order1)
        add_order(order2)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        order_contains_dish(1, 1, 2)
        order_contains_dish(2, 2, 1)
        most_expensive_order = get_most_expensive_anonymous_order()
        self.assertEqual(most_expensive_order.get_order_id(), 1)

    def test_get_most_expensive_anonymous_order2(self):
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order1)
        most_expensive_order = get_most_expensive_anonymous_order()
        self.assertEqual(most_expensive_order.get_order_id(), 1)

    def test_is_most_liked_dish_equal_to_most_purchased(self):
        customer = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        customer_likes_dish(1, 1)
        customer_likes_dish(1, 2)
        order = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        add_order(order)
        order_contains_dish(1, 1, 2)
        order_contains_dish(1, 2, 1)
        self.assertTrue(is_most_liked_dish_equal_to_most_purchased())

    def test_get_customers_ordered_top_5_dishes(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        customer2 = Customer(2, "Jane Doe", "987654321", "456 Main St")
        add_customer(customer1)
        add_customer(customer2)

        # Create dishes
        dishes = [
            Dish(i, f"Dish{i}", 10.0 + i, True) for i in range(1, 7)
        ]
        for dish in dishes:
            add_dish(dish)

        # Customer 1 likes the first 5 dishes
        for dish_id in range(1, 6):
            customer_likes_dish(1, dish_id)

        # Customer 2 likes some of the dishes, but not all top 5
        customer_likes_dish(2, 1)
        customer_likes_dish(2, 2)
        customer_likes_dish(2, 6)

        # Create orders
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 7, 14, 30, 0))
        add_order(order1)
        add_order(order2)

        #connect orders to customers
        customer_placed_order(1,1)
        customer_placed_order(2,2)

        # Customer 1 orders the first 5 dishes
        for dish_id in range(1, 6):
            order_contains_dish(1, dish_id, 1)

        # Customer 2 orders some dishes, but not all top 5
        order_contains_dish(2, 1, 1)
        order_contains_dish(2, 2, 1)
        order_contains_dish(2, 6, 1)

        # Get customers who ordered all top 5 dishes
        customers = get_customers_ordered_top_5_dishes()

        # Assert that only customer 1 is returned
        self.assertEqual(customers, [1])

    def test_get_non_worth_price_increase(self):
        dish = Dish(1, "Pizza", 50.0, True)
        add_dish(dish)
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 30, 0))
        add_order(order1)
        add_order(order2)
        order_contains_dish(1, 1, 1)
        order_contains_dish(2, 1, 2)
        update_dish_price(1, 40.0)
        order3 = Order(3, datetime(2023, 5, 6, 16, 30, 0))
        add_order(order3)
        order_contains_dish(3, 1, 2)
        result = get_non_worth_price_increase()
        self.assertEqual(result, [])

    def test_get_total_profit_per_month(self):
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 6, 6, 15, 30, 0))
        add_order(order1)
        add_order(order2)
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 12.0, True)
        add_dish(dish1)
        add_dish(dish2)
        order_contains_dish(1, 1, 2)
        order_contains_dish(2, 2, 1)
        profits = get_total_profit_per_month(2023)
        self.assertEqual(profits, [(12,0.0), (11,0.0), (10,0.0), (9,0.0), (8,0.0), (7,0.0), (6, 12.0), (5, 20.0), (4,0.0), (3,0.0), (2,0.0), (1,0.0)])

    def test_get_total_profit_per_month_2(self):
        # Add orders
        order1 = Order(1, datetime(2023, 1, 15, 12, 0, 0))
        order2 = Order(2, datetime(2023, 2, 15, 12, 0, 0))
        order3 = Order(3, datetime(2023, 3, 15, 12, 0, 0))
        self.assertEqual(add_order(order1), ReturnValue.OK)
        self.assertEqual(add_order(order2), ReturnValue.OK)
        self.assertEqual(add_order(order3), ReturnValue.OK)

        # Add dishes
        dish1 = Dish(1, "Pizza", 10.0, True)
        dish2 = Dish(2, "Burger", 20.0, True)
        self.assertEqual(add_dish(dish1), ReturnValue.OK)
        self.assertEqual(add_dish(dish2), ReturnValue.OK)

        # Add order contents
        self.assertEqual(order_contains_dish(1, 1, 2), ReturnValue.OK)  # 2 Pizzas at 10 each
        self.assertEqual(order_contains_dish(2, 2, 1), ReturnValue.OK)  # 1 Burger at 20 each

        # Call the function
        profits = get_total_profit_per_month(2023)

        # Check results
        expected_profits = [(12, 0.0), (11, 0.0), (10, 0.0), (9, 0.0), (8, 0.0), (7, 0.0), (6, 0.0), (5, 0.0), (4, 0.0), (3, 0.0), (2, 20.0), (1, 20.0),]

        self.assertEqual(profits, expected_profits)

    def test_get_potential_dish_recommendations(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        customer2 = Customer(2, "Jane Doe", "987654321", "456 Main St")
        customer3 = Customer(3, "Jim Beam", "555666777", "789 Main St")
        add_customer(customer1)
        add_customer(customer2)
        add_customer(customer3)

        # Create dishes
        dishes = [
            Dish(i, f"Dish{i}", 10.0 + i, True) for i in range(1, 7)
        ]
        for dish in dishes:
            add_dish(dish)

        # Add likes for customer 1
        customer_likes_dish(1, 1)
        customer_likes_dish(1, 2)
        customer_likes_dish(1, 3)

        # Add likes for customer 2
        customer_likes_dish(2, 1)
        customer_likes_dish(2, 2)
        customer_likes_dish(2, 4)

        # Add likes for customer 3
        customer_likes_dish(3, 1)
        customer_likes_dish(3, 2)
        customer_likes_dish(3, 3)
        customer_likes_dish(3, 4)

        # Expected: Customer 1 should get recommendations for dish 4 since Customer 3 is a similar customer who has liked dish 4
        recommendations = get_potential_dish_recommendations(1)
        self.assertEqual(recommendations, [4])


    def test_get_potential_dish_recommendations_example(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        customer2 = Customer(2, "Jane Doe", "987654321", "456 Main St")
        customer3 = Customer(3, "Jim Beam", "555666777", "789 Main St")
        customer4 = Customer(4, "Jack Daniels", "222333444", "101 Main St")
        add_customer(customer1)
        add_customer(customer2)
        add_customer(customer3)
        add_customer(customer4)

        # Create dishes
        dishes = [
            Dish(1, "Dish1", 11.0, True),
            Dish(2, "Dish2", 12.0, True),
            Dish(3, "Dish3", 13.0, True),
            Dish(4, "Dish4", 14.0, True),
            Dish(5, "Dish5", 15.0, True),
            Dish(6, "Dish6", 16.0, True),
            Dish(7, "Dish7", 17.0, True)
        ]
        for dish in dishes:
            add_dish(dish)

        # Add likes for customer 1
        customer_likes_dish(1, 2)
        customer_likes_dish(1, 3)
        customer_likes_dish(1, 4)
        customer_likes_dish(1, 6)

        # Add likes for customer 2
        customer_likes_dish(2, 1)
        customer_likes_dish(2, 2)
        customer_likes_dish(2, 3)
        customer_likes_dish(2, 4)
        customer_likes_dish(2, 5)

        # Add likes for customer 3
        customer_likes_dish(3, 3)
        customer_likes_dish(3, 4)
        customer_likes_dish(3, 5)
        customer_likes_dish(3, 6)
        customer_likes_dish(3, 7)

        # Add likes for customer 4
        customer_likes_dish(4, 2)
        customer_likes_dish(4, 6)
        customer_likes_dish(4, 7)

        # Get recommendations for customer 1
        recommendations = get_potential_dish_recommendations(1)
        self.assertEqual(recommendations, [1, 5, 7])


    def test_get_non_worth_price_increase_example(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer1)

        # Create dish
        dish1 = Dish(1, "Dish1", 50.0, True)
        add_dish(dish1)

        # Create orders
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 0, 0))
        order3 = Order(3, datetime(2023, 5, 6, 16, 0, 0))
        order4 = Order(4, datetime(2023, 5, 6, 17, 0, 0))
        add_order(order1)
        add_order(order2)
        add_order(order3)
        add_order(order4)


        # customer placed order
        customer_placed_order(1, 1)
        customer_placed_order(1, 2)
        customer_placed_order(1, 3)
        customer_placed_order(1, 4)

        # Orders contain dishes
        order_contains_dish(1, 1, 1)
        order_contains_dish(2, 1, 2)
        update_dish_price(1, 40)
        order_contains_dish(3, 1, 2)
        order_contains_dish(4, 1, 2)
        update_dish_price(1, 50)

        # Get non-worth price increase dishes
        non_worth_price_increase_dishes = get_non_worth_price_increase()
        self.assertEqual(non_worth_price_increase_dishes, [1])


    def test_get_total_profit_per_month_example(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer1)

        # Create dishes
        dish1 = Dish(1, "Dish1", 50.0, True)
        dish2 = Dish(2, "Dish2", 30.0, True)
        add_dish(dish1)
        add_dish(dish2)

        # Create orders
        order1 = Order(1, datetime(2023, 1, 15, 14, 30, 0))
        order2 = Order(2, datetime(2023, 2, 10, 15, 0, 0))
        order3 = Order(3, datetime(2023, 3, 20, 16, 0, 0))
        order4 = Order(4, datetime(2023, 3, 25, 17, 0, 0))
        add_order(order1)
        add_order(order2)
        add_order(order3)
        add_order(order4)

        # Customer places orders
        customer_placed_order(1, 1)
        customer_placed_order(1, 2)
        customer_placed_order(1, 3)
        customer_placed_order(1, 4)

        # Orders contain dishes
        order_contains_dish(1, 1, 2)
        order_contains_dish(2, 2, 1)
        order_contains_dish(3, 1, 1)
        order_contains_dish(4, 2, 3)

        # Get total profit per month for 2023
        total_profit_per_month = get_total_profit_per_month(2023)
        expected_profit = [(12,0.0), (11,0.0), (10,0.0), (9,0.0), (8,0.0), (7,0.0), (6,0.0), (5,0.0), (4,0.0), (3, 140.0), (2, 30.0), (1, 100.0)]
        self.assertEqual(total_profit_per_month, expected_profit)


    def test_get_potential_dish_recommendations_1(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        customer2 = Customer(2, "Jane Doe", "987654321", "456 Main St")
        customer3 = Customer(3, "Jim Beam", "555666777", "789 Main St")
        customer4 = Customer(4, "Jack Daniels", "222333444", "101 Main St")
        add_customer(customer1)
        add_customer(customer2)
        add_customer(customer3)
        add_customer(customer4)

        # Create dishes
        dishes = [
            Dish(1, "Dish1", 11.0, True),
            Dish(2, "Dish2", 12.0, True),
            Dish(3, "Dish3", 13.0, True),
            Dish(4, "Dish4", 14.0, True),
            Dish(5, "Dish5", 15.0, True),
            Dish(6, "Dish6", 16.0, True),
            Dish(7, "Dish7", 17.0, True)
        ]
        for dish in dishes:
            add_dish(dish)

        # Add likes for customer 1
        customer_likes_dish(1, 2)
        customer_likes_dish(1, 3)
        customer_likes_dish(1, 4)
        customer_likes_dish(1, 6)

        # Add likes for customer 2
        customer_likes_dish(2, 1)
        customer_likes_dish(2, 2)
        customer_likes_dish(2, 3)
        customer_likes_dish(2, 4)
        customer_likes_dish(2, 5)

        # Add likes for customer 3
        customer_likes_dish(3, 3)
        customer_likes_dish(3, 4)
        customer_likes_dish(3, 5)
        customer_likes_dish(3, 6)
        customer_likes_dish(3, 7)

        # Add likes for customer 4
        customer_likes_dish(4, 2)
        customer_likes_dish(4, 6)
        customer_likes_dish(4, 7)

        # Get recommendations for customer 1
        recommendations = get_potential_dish_recommendations(1)
        self.assertEqual(recommendations, [1, 5, 7])

    def test_get_non_worth_price_increase_example_2(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer1)

        # Create dish
        dish1 = Dish(1, "Dish1", 50.0, True)
        add_dish(dish1)

        # Create orders
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 0, 0))
        order3 = Order(3, datetime(2023, 5, 6, 16, 0, 0))
        order4 = Order(4, datetime(2023, 5, 6, 17, 0, 0))
        add_order(order1)
        add_order(order2)
        add_order(order3)
        add_order(order4)

        # Customer places orders
        customer_placed_order(1, 1)
        customer_placed_order(1, 2)
        customer_placed_order(1, 3)
        customer_placed_order(1, 4)

        # Orders contain dishes
        order_contains_dish(1, 1, 1)
        order_contains_dish(2, 1, 2)
        order_contains_dish(3, 1, 2)
        update_dish_price(1, 40)
        order_contains_dish(4, 1, 2)
        update_dish_price(1, 50)

        # Get non-worth price increase dishes
        non_worth_price_increase_dishes = get_non_worth_price_increase()
        self.assertEqual(non_worth_price_increase_dishes, [])


    def test_get_non_worth_price_increase_2(self):
        # Create customers
        customer1 = Customer(1, "John Doe", "123456789", "123 Main St")
        add_customer(customer1)

        # Create dishes
        dish2 = Dish(2, "Dish2", 50.0, True)
        add_dish(dish2)
        dish1 = Dish(1, "Dish1", 50.0, True)
        add_dish(dish1)

        # Create orders
        order1 = Order(1, datetime(2023, 5, 6, 14, 30, 0))
        order2 = Order(2, datetime(2023, 5, 6, 15, 0, 0))
        order3 = Order(3, datetime(2023, 5, 6, 16, 0, 0))
        order4 = Order(4, datetime(2023, 5, 6, 17, 0, 0))
        add_order(order1)
        add_order(order2)
        add_order(order3)
        add_order(order4)

        # Customer places orders
        customer_placed_order(1, 1)
        customer_placed_order(1, 2)
        customer_placed_order(1, 3)
        customer_placed_order(1, 4)

        # Orders contain dish 2
        order_contains_dish(1, 2, 1)
        order_contains_dish(2, 2, 2)
        order_contains_dish(3, 2, 1)
        update_dish_price(2, 40)
        order_contains_dish(4, 2, 2)
        update_dish_price(2, 50)

        # Orders contain dish 1
        order_contains_dish(1, 1, 1)
        order_contains_dish(2, 1, 2)
        order_contains_dish(3, 1, 1)
        update_dish_price(1, 40)
        order_contains_dish(4, 1, 2)
        update_dish_price(1, 50)

        # Get non-worth price increase dishes
        non_worth_price_increase_dishes = get_non_worth_price_increase()
        self.assertEqual(non_worth_price_increase_dishes, [1,2])



if __name__ == "__main__":
    unittest.main()
