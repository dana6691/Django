from re import L


def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO order")
    


if __name__ = '__main__':
    connection = get_sql_connection()
    print(insert_order(connection,{
        'customer_name':,
        'grand_total': ' 500',
        'datetime': datetime.now(),
        'order_details': [
            {
                'product_id': 1,
                'quantity': 2,
                'total_price': 40
            },
            {
                'product_id': 3,
                'quantity': 5,
                'total_price': 5
            }
        ]
            
    }))