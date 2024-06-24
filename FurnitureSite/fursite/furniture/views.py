from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, ListView
from furniture.models import *
from furniture.token import account_activation_token
from fursite.forms import *
from django.contrib import messages
from django.contrib.auth import login, logout


def index(request):
    products_sorted = Product.objects.all().order_by('-views')
    context = {
        'products_sorted': products_sorted,
    }
    return render(request, 'furniture/index.html', context)


def contacts(request):
    return render(request, 'furniture/contacts.html')


def about_us(request):
    return render(request, 'furniture/about_us.html')


def catalog(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'furniture/catalog.html', context=context)


class ProductByCategory(ListView):
    template_name = 'furniture/products_by_category.html'
    context_object_name = 'product_by_category'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(Category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class ViewProduct(DetailView):
    model = Product
    template_name = 'furniture/view_product.html'
    context_object_name = 'product_item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        return context


class AddReview(DetailView):

    def post(self, request, slug):
        if request.user.is_authenticated == False:
            return user_login(request)
        else:
            form = ReviewForm(request.POST)
            product_item = get_object_or_404(Product, slug=slug)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.product = product_item
                form.save()
                return redirect('view_product', str(slug))


def cart(request):
    if request.user.is_authenticated == False:
        return user_login(request)
    else:
        products_in_cart = request.user.cart.all()
        total_price = 0
        for item in products_in_cart:
            total_price += item.price

        context = {
            'products_in_cart': products_in_cart,
            'total_price': total_price,
        }

        return render(request, 'furniture/cart.html', context)


def add_to_cart_view_product(request, slug):
    if request.user.is_authenticated == False:
        return user_login(request)
    else:
        product_item = get_object_or_404(Product, slug=slug)
        if request.user not in product_item.cart.all():
            product_item.cart.add(request.user)
        return redirect('cart')


def add_to_cart_favorite(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user not in product_item.cart.all():
        product_item.cart.add(request.user)
    return redirect('cart')


def remove_from_cart_view_product(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user in product_item.cart.all():
        product_item.cart.remove(request.user)
    return redirect('view_product', str(slug))


def remove_from_cart_favorite(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user in product_item.cart.all():
        product_item.cart.remove(request.user)
    return redirect('favorites')


def remove_from_cart_cart(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user in product_item.cart.all():
        product_item.cart.remove(request.user)
    return redirect('cart')


def favorites(request):
    if request.user.is_authenticated == False:
        return user_login(request)
    else:
        favorite_products = request.user.favorite.all()
        paginator = Paginator(favorite_products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'favorite_products': favorite_products,
            "page_obj": page_obj,
        }

        return render(request, 'furniture/favorites.html', context)


def add_to_favorite(request, slug):
    if request.user.is_authenticated == False:
        return user_login(request)
    else:
        product_item = get_object_or_404(Product, slug=slug)
        if request.user not in product_item.favorite.all():
            product_item.favorite.add(request.user)
        return redirect('favorites')


def remove_from_favorite_view_product(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user in product_item.favorite.all():
        product_item.favorite.remove(request.user)
    return redirect('view_product', str(slug))


def remove_from_favorite_favorite(request, slug):
    product_item = get_object_or_404(Product, slug=slug)
    if request.user in product_item.favorite.all():
        product_item.favorite.remove(request.user)
    return redirect('favorites')


class Search(ListView):
    template_name = 'furniture/search.html'
    context_object_name = 'product'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации аккаунта'
            message = render_to_string('furniture/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, "Ссылка для активации аккаунта была отправлена на ваш email")
            return redirect('Home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'furniture/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Регистрация завершена успешно!")
        return redirect('Home')
    else:
        messages.error(request, 'Ошибка регистрации')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Home')
    else:
        form = UserLoginForm()
    return render(request, 'furniture/login.html', {"form": form})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    #Представление по сбросу пароля по почте
    form_class = UserForgotPasswordForm
    template_name = 'furniture/password_change_request.html'
    success_url = reverse_lazy('Home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    email_template_name = 'furniture/password_change_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    #Представление установки нового пароля
    form_class = UserSetNewPasswordForm
    template_name = 'furniture/password_changing.html'
    success_url = reverse_lazy('Home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


def user_logout(request):
    logout(request)
    return redirect('Home')




