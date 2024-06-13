import unittest
from flask import Flask
from flask_testing import TestCase
from UPDATE2 import create_app, db
from UPDATE2.models import Product

class TestProductRoutes(TestCase):

    def create_app(self):
        app = create_app('testing')  # Ensure you have a testing configuration
        return app

    def setUp(self):
        db.create_all()
        self.product = Product(name="Test Product", description="This is a test product", price=9.99, stock=10)
        db.session.add(self.product)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_update_product(self):
        # Perform a PUT request to update the product
        response = self.client.put(f'/products/{self.product.id}', json={
            'name': 'Updated Test Product',
            'description': 'This is an updated test product',
            'price': 19.99,
            'stock': 20
        })
        self.assertEqual(response.status_code, 200)

        # Verify the update
        updated_product = Product.query.get(self.product.id)
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, 'Updated Test Product')
        self.assertEqual(updated_product.description, 'This is an updated test product')
        self.assertEqual(updated_product.price, 19.99)
        self.assertEqual(updated_product.stock, 20)

if __name__ == '__main__':
    unittest.main()
