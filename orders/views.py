from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
#from .tasks import order_created
from mydrone import models

# thư viện cho việc sử dụng email
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives


category_list = models.Category.objects.all()


def order_create(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    if username:
        user = models.User.objects.get(username=username)
        user_profile = models.UserProfileInfo.objects.get(user=user)
        order = Order()
        order.username = user.username
        order.first_name = user.first_name
        order.last_name = user.last_name
        order.email = user.email
        order.phone = user_profile.phone
        order.address = user_profile.address
    else:
        order = Order()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, order)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         drone=item['drone'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # Gửi email
            email_address = form.cleaned_data['email']
            subject = 'Confirmation on your purchase order ' + str(order.id)
            message = 'Thank you <b>' + order.last_name + \
                ' ' + order.first_name + '</b> for your order and your trust to DROPHUT,'
            recepient = str(email_address)

            html_content = '''
            <p style="margin:4px 0;font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;font-weight:normal;">DROPHUT kindly announce that ''' + \
                str(order.id) + \
                '''your purchase order has been received and processed  . </p>									
			<h3 style="font-size:13px;font-weight:bold;color:#02acea;text-transform:uppercase;margin:20px 0 0 0;border-bottom:1px solid #ddd;">Thông tin đơn hàng:</h3>''' + \
                '''<h5>Họ và tên: ''' + \
                order.last_name + \
                ''' ''' + \
                order.first_name + \
                '''</h5> ''' + \
                '<h5>Phone: ' + \
                str(order.phone) + \
                '''</h5><h5>Address: ''' + \
                order.address + \
                '''</h5> ''' + \
                '''<h2 style="text-align:left;margin:10px 0;border-bottom:1px solid #ddd;padding-bottom:5px;font-size:13px;color:#02acea;">ORDER DETAIL</h2>''' + \
                '''<table border="0" cellpadding="0" cellspacing="0" style="background:#f5f5f5;" width="100%">''' + \
                ''' <thead>
											<tr>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Product</th>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Unit price</th>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Quantity</th>
												<th align="right" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">TOTAL BILL</th>
											</tr>
										</thead>
                                        <tbody style="font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;">
            '''
            for item in cart:
                html_content += '''
                <tr>
					<td align="left" style="padding:3px 9px;" valign="top"><span class="yiv1530170030name">''' + \
                    str(item['drone']) + \
                    '''</td>''' + \
                    '''<td align="left" style="padding:3px 9px;" valign="top"><span>''' + \
                    str("{:0,.0f}".format(item['price'])) + \
                    '''</span></td>''' + \
                    ''' <td align="left" style="padding:3px 9px;" valign="top">''' + \
                    str(item['quantity']) + \
                    '''</td>''' + \
                    '''<td align="right" style="padding:3px 9px;" valign="top"><span>''' + \
                    str("{:0,.0f}".format(item['total_price'])) + \
                    '''</span></td></tr>'''
            html_content += '''<tr><td colspan="4" style="text-align:right">Tổng đơn hàng:''' + \
                str("{:0,.0f}".format(cart.get_total_price())) + \
                '''đ</td></tr>'''
            html_content += '''</table>

            <p style="margin:0;font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;font-weight:normal;">Incase you still have something wondered or consufused , please phone us at 9999999999</b></p>'''

            msg = EmailMultiAlternatives(
                subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # clear the cart
            cart.clear()

            return render(request,
                          'orders/order/created.html',
                          {'order': order, 'categories': category_list, 'username': username})
    else:
        form = OrderCreateForm(instance=order)
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'categories': category_list, 'username': username})
