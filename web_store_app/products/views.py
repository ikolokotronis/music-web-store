from django.shortcuts import render
from django.views import View
from main.models import Category, ShoppingCart, SubCategory
from products.models import Product, SubCategoryProduct
from users.models import WebsiteUser


class ProductView(View):
    def get(self, request, product_id):
        """
        Displays information about a specific product, with the option to add it to the shopping cart
        :param request:
        :param product_id:
        :return product details page:
        """
        all_categories = Category.objects.all()
        all_subcategories = SubCategory.objects.all().order_by('name')
        product = Product.objects.get(id=product_id)
        shopping_cart = ShoppingCart.objects.all()
        subcategory = SubCategoryProduct.objects.filter(product_id=product_id)[0]
        last_viewed_products = ""
        # response = render(request, 'product/product_details.html', {'product': product,
        #                                                         'shopping_cart_list': shopping_cart,
        #                                                         'subcategory': subcategory,
        #                                                         'last_viewed_products': last_viewed_products,
        #                                                             'all_categories': all_categories,
        #                                                             'all_subcategories': all_subcategories,
        #                                                             }
        #               )
        result = []
        result2 = ""
        if request.session.get('last_viewed_products'):
            last_viewed_products = request.session.get('last_viewed_products').split(',')
            request.session['last_viewed_products'] += f'{product.name},'
            for p in last_viewed_products:
                result2 = p

        else:
            request.session['last_viewed_products'] = f'{product.name},'

        return render(request, 'product/product_details.html', {'all_categories': all_categories,
                                                                'all_subcategories': all_subcategories,
                                                                'product': product,
                                                                'shopping_cart_list': shopping_cart,
                                                                'subcategory': subcategory,
                                                                'last_viewed_products': last_viewed_products,
                                                                'result': result2}
                      )

    def post(self, request, product_id):
        all_categories = Category.objects.all()
        all_subcategories = SubCategory.objects.all().order_by('name')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        user = WebsiteUser.objects.get(id=request.user.id)
        shopping_cart = ShoppingCart.objects.all()
        ShoppingCart.objects.create(product=product, user=user, quantity=quantity)
        return render(request, 'product/product_details.html', {'all_categories': all_categories,
                                                                'all_subcategories': all_subcategories,
                                                                'product': product,
                                                                'success_text': 'Product added to cart',
                                                                'shopping_cart_list': shopping_cart}
                      )