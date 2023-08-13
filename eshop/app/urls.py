from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path

from . import views
from .forms import LoginForm, ChangeMyPassword, MySetPasswordForm

urlpatterns = [
                  path("", views.home),
                  path("home/", views.home, name="home"),
                  path("about/", views.about, name="about"),
                  path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
                  path("product-detail/<int:pk>", views.DetailProduct.as_view(), name="product-detail"),
                  path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
                  path("profile/", views.ProfileView.as_view(), name='profile'),
                  path("add_to_cart/", views.add_to_cart, name='add_to_cart'),
                  path("cart/", views.show_cart, name='showcart'),
                  path("checkout/", views.checkout.as_view(), name='checkout'),
                  path('paymentdone/', views.payment_done, name='paymentdone'),
                  path('orders/', views.orders, name='orders'),

                  path('search/', views.search, name='search'),

                  path('new_wishlist/', views.new_wishlist, name='new_wishlist'),
                  path('wishlist/', views.show_wishlist, name='show_wishlist'),


                  # login authentication
                  path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
                  path('accounts/login/',
                       auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm),
                       name='login'),
                  path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/change_password.html',
                                                                               form_class=ChangeMyPassword,
                                                                               success_url='/passwordchangedone'),
                       name='passwordchange'),
                  path('passwordchangedone/',
                       auth_view.PasswordChangeDoneView.as_view(template_name='app/change_password_done.html'),
                       name='passwordchangedone'),
                  path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

                  path('password_reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'),
                       name='password_reset'),

                  path('password_reset/done/',
                       auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
                       name='password_reset_done'),

                  path('password_reset_confirm/<uidb64>/<token>',
                       auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
                                                                  form_class=MySetPasswordForm),
                       name='password_reset_confirm'),

                  path('password_reset_complete/',
                       auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
                       name='password_reset_complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
