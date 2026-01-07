from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    if request.method == "POST":
        # 獲取表單數據
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        doctor_email = request.POST['doctor_email']
        
        # 檢查用戶是否已認證並避免重複提交
        if request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, 
                user_id=user_id
            ).exists()
            
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('listings:listing', listing_id=listing_id)
        
        # 創建新聯繫記錄
        contact = Contact(
            listing=listing, 
            listing_id=listing_id, 
            name=name, 
            email=email, 
            phone=phone, 
            message=message, 
            user_id=user_id,
        )
        contact.save()
        
        # 發送電子郵件
        send_mail(
            'Clinic Inquiry',    # 電子郵件標題
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info', # 電子郵件內容
            'jackywan2026@gmail.com', # self email  From email address
            [doctor_email], # To email address
            fail_silently=False,     # 防止發送失敗
        )   

        # 顯示成功消息
        messages.success(request, 'Your request has been submitted, a clinic representative will get back to you soon.')
        
        # 重定向回列表頁面
        return redirect('listings:listing', listing_id=listing_id)
    
    # 如果不是 POST 請求，重定向到列表頁面
    return redirect('listings:index')

def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return redirect('accounts:dashboard')

def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = (ContactForm(request.POST, instance=contact))
        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard")
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit_contact.html', 
                    {"form":form, "contact":contact})



