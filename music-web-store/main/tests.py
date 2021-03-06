from django.test import TestCase, Client
import pytest
from main.models import ShoppingCart, Order, ProductOrder, Complaint, Newsletter


@pytest.mark.django_db
def test_home_page_get():  # homepage test 1
    client = Client()
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_post():  # homepage test 2
    client = Client()
    response = client.post('/', {'key_word': 'a'})
    assert response.status_code == 200
    for product in response.context['product_results']:
        assert 'a' in product.name


@pytest.mark.django_db
def test_category_page_get(client, example_category):  # category page test 1
    client = Client()
    response = client.get(f'/category/{example_category.id}/')
    assert response.status_code == 200
    category = response.context['category']
    assert category.name == 'Category 1'
    assert category.description == 'Category description 1'


@pytest.mark.django_db
def test_category_page_post(client, example_category):  # category page test 2
    client = Client()
    response = client.post(f'/category/{example_category.id}/', {'key_word': 'a'})
    assert response.status_code == 200
    for product in response.context['product_results']:
        assert 'a' in product.name


@pytest.mark.django_db
def test_subcategory_page_get(client, example_subcategory,
                              example_category, example_category_subcategory_relation):  # subcategory page test 1
    client = Client()
    response = client.get(f'/subcategory/{example_subcategory.id}/')
    assert response.status_code == 200
    subcategory = response.context['subcategory']
    assert subcategory.name == 'Subcategory 1'
    assert subcategory.description == 'Subcategory description 1'


@pytest.mark.django_db
def test_subcategory_page_post(client, example_subcategory):  # subcategory page test 2
    client = Client()
    response = client.post(f'/subcategory/{example_subcategory.id}/', {'key_word': 'a'})
    assert response.status_code == 200
    for product in response.context['product_results']:
        assert 'a' in product.name


@pytest.mark.django_db
def test_shopping_cart_page_get(client, example_website_user,
                                example_product, example_shopping_cart):  # shopping cart test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/{example_website_user.id}/')
    assert response.status_code == 200
    assert response.context['products_summary'] == 100
    for shopping_cart in response.context['shopping_cart_list']:
        assert shopping_cart.quantity == 1


@pytest.mark.django_db
def test_shopping_cart_page_post(client, example_website_user,
                                 example_product, example_shopping_cart):  # shopping cart test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post(f'/shopping_cart/{example_website_user.id}/')
    assert response.status_code == 302
    assert ShoppingCart.objects.filter(user=example_website_user).count() == 0


@pytest.mark.django_db
def test_shopping_cart_product_remove_page_get(client, example_website_user,
                                               example_product, example_shopping_cart):  # shopping cart product remove test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/remove/{example_website_user.id}/{example_product.id}/')
    assert response.status_code == 302
    for shopping_cart in ShoppingCart.objects.filter(user=example_website_user):
        assert example_product not in shopping_cart.product


@pytest.mark.django_db
def test_shopping_cart_checkout_page_get(client, example_website_user,
                                         example_product, example_shopping_cart):  # shopping cart checkout test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/{example_website_user.id}/checkout/')
    assert response.status_code == 200
    assert response.context['products_summary'] == 100
    for shopping_cart in response.context['shopping_cart_list']:
        assert shopping_cart.quantity == 1


@pytest.mark.django_db
def test_shopping_cart_checkout_page_post(client, example_website_user, example_product, example_shopping_cart):  # shopping cart checkout test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post(f'/shopping_cart/{example_website_user.id}/checkout/', {'phone_number': 123456789,
                                                                                   'address': 'test_address',
                                                                                   'shipping_type': 'pickup_in_person'})
    assert response.status_code == 302
    assert ProductOrder.objects.filter(user=example_website_user).count() == 1
    order = Order.objects.get(user=example_website_user)
    assert order.shipping_type == 1
    assert order.address == 'test_address'
    assert order.phone_number == 123456789


@pytest.mark.django_db
def test_shopping_cart_payment_page_get(client, example_product, example_website_user,
                                        example_shopping_cart, example_order):  # shopping cart payment page test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/{example_website_user.id}/{example_order.id}/payment/')
    assert response.status_code == 200
    for shopping_cart in response.context['shopping_cart_list']:
        assert shopping_cart.quantity == 1
    assert response.context['order'] == example_order
    assert Order.objects.get(user=example_website_user)


@pytest.mark.django_db
def test_shopping_cart_payment_page_post(client, example_product, example_website_user,
                                        example_shopping_cart, example_order):  # shopping cart payment page test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post(f'/shopping_cart/{example_website_user.id}/{example_order.id}/payment/',
                           {'payment_type': 'cash'})
    assert response.status_code == 302
    order = Order.objects.get(user=example_website_user)
    assert order.payment_type == 1
    assert order.user.id == example_website_user.id


@pytest.mark.django_db
def test_shopping_cart_summary_page_get(client, example_product, example_website_user,
                                        example_shopping_cart, example_order):  # shopping cart summary page test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/{example_website_user.id}/{example_order.id}/summary/')
    assert response.status_code == 200
    assert response.context['products_summary'] == 100
    for shopping_cart in response.context['shopping_cart_list']:
        assert shopping_cart.quantity == 1
    assert response.context['order'] == example_order
    order = Order.objects.get(user_id=example_website_user.id)
    assert order.payment_type == 1
    assert order.shipping_type == 1
    assert order.amount_paid == 100
    assert order.user.id == example_website_user.id


@pytest.mark.django_db
def test_shopping_cart_summary_page_post(client, example_product, example_website_user,
                                        example_shopping_cart, example_order):  # shopping cart summary page test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post(f'/shopping_cart/{example_website_user.id}/{example_order.id}/summary/')
    assert response.status_code == 302
    order = Order.objects.get(user_id=example_website_user.id)
    assert order.amount_paid == 100
    assert order.payment_type == 1
    assert order.shipping_type == 1
    assert order.user.id == example_website_user.id


@pytest.mark.django_db
def test_shopping_cart_success_page_get(client, example_product, example_website_user,
                                        example_shopping_cart, example_order):  # shopping cart success page test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get(f'/shopping_cart/{example_website_user.id}/{example_order.id}/success/')
    assert response.status_code == 200
    assert ShoppingCart.objects.filter(user=example_website_user).count() == 0
    order = Order.objects.get(user_id=example_website_user.id)
    assert order.user.id == example_website_user.id


@pytest.mark.django_db
def test_newsletter_page_get(client, example_website_user):  # newsletter page test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get('/newsletter/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_newsletter_page_post(client, example_website_user):  # newsletter page test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post('/newsletter/', {'email': 'test_email@gmail.com'})
    assert response.status_code == 200
    assert response.context['success_text'] == 'Email sent. Check your inbox for further details'
    assert Newsletter.objects.get(user_id=example_website_user.id)


@pytest.mark.django_db
def test_complaint_page_get(client, example_website_user):  # complaint page test 1
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.get('/complaint/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_complaint_page_post(client, example_website_user):  # complaint page test 2
    client = Client()
    client.login(username='test_user', password='test_password')
    response = client.post('/complaint/', {'subject': 'test_subject', 'content': 'test_content'})
    assert response.status_code == 200
    assert response.context['success_text'] == 'Complaint sent'
    complaint = Complaint.objects.get(user_id=example_website_user.id)
    assert complaint.subject == 'test_subject'
    assert complaint.content == 'test_content'

