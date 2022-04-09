from mysql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT * from product"
    query2= "SELECT product.product_id, product.name, product.uom_id, product.price_per_unit, uom.uom_name FROM product INNER JOIN uom ON product.uom_id = uom.uom_id"
    cursor.execute(query2)
    
    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                'product_id':product_id,
                'name':name,
                'uom_id':uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            }
        )

    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO product (name, uom_id, price_per_unit) VALUES (%s,%s,%s)")
    data = (product['product_name'],product['uom_id'],product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM product WHERE product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()
    
if __name__=='__main__':
    connection = get_sql_connection()
    #print(get_all_products(connection))
    #print(insert_new_product(connection, {
    #    'product_name': 'corn',
    #    'uom_id': '1',
    #    'price_per_unit': '1'
    #}))
    print(delete_product(connection, 6))