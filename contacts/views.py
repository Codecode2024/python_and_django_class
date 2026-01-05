from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages

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
            user_id=user_id
        )
        contact.save()
        
        # 顯示成功消息
        messages.success(request, 'Your request has been submitted, a clinic representative will get back to you soon.')
        
        # 重定向回列表頁面
        return redirect('listings:listing', listing_id=listing_id)
    
    # 如果不是 POST 請求，重定向到列表頁面
    return redirect('listings:index')

def delete_contact(request, contact_id):
    return redirect('accounts:dashboard')

def edit_contact(request, contact_id):
    return redirect('accounts:dashboard')

