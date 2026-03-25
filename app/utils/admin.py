# Admin 
# PDF report upload kare
# Title, description, year add kare
# File static/reports/ me save ho
# Entry Report table me store ho
# Sirf admin hi access kar sake

from flask import session, redirect, url_for, flash

def admin_required():
    #Ager user login nhi h ya admin nhi h
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Admin access required", "danger")
        return False
    return True
