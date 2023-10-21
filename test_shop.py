import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(product.quantity)
        assert not product.check_quantity(product.quantity + 1)
        assert product.check_quantity(product.quantity - 1)

    def test_product_buy(self, product):
        product.buy(100)
        assert product.quantity == 900

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


class TestCart:

    def test_cart_add_new_product(self, cart, product):
        cart.add_product(product, 5)
        assert cart.products == {product: 5}
        assert len(cart.products) == 1

    def test_cart_add_same_product(self, cart, product):
        cart.add_product(product, 5)
        cart.add_product(product, 3)
        assert cart.products == {product: 8}
        assert len(cart.products) == 1

    def test_cart_remove_product_one_item(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 3)
        assert cart.products == {product: 2}
        assert len(cart.products) == 1

    def test_cart_remove_product_all_items(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert cart.products == {}

    def test_cart_remove_product_exceeding_item(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 8)
        assert cart.products == {}

    def test_cart_remove_product_none_item(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert cart.products == {}

    def test_cart_clear(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert cart.products == {}

    def test_cart_total_price(self, cart, product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == product.price * 5

    def test_buy_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.buy()
        assert cart.products == {}
        assert product.quantity == 995

    def test_buy_cart_exceeding_items(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)
            cart.buy()
