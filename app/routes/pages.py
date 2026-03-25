from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash #importing password hashing function
from flask import current_app, send_from_directory, abort
from app.models import Prediction, Report, User, reportRequest
from app.models import ContactMessage
from app.utils import admin
from app.utils.admin import admin_required
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
# from app.forms import CitySearchForm

pages_bp = Blueprint('pages', __name__)




#--------------------------Admin-only Route----------------------------
#Ab hum ek admin dashboard route banayenge.
@pages_bp.route('/admin/dashboard')
def admin_dashboard():

    #Admin check
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    #Ager Admin verify ho jaye to esko admin dashboard pe bhej do
    # return render_template('admin/admin_dashboard.html')
    return render_template(
        "admin/admin_dashboard.html",
        total_reports=Report.query.count(),
        total_messages=ContactMessage.query.count(),
        total_users=User.query.count(),
        total_predictions=Prediction.query.count()
    )


# ----------------------------- USER UPLOAD THEIR IMAGE FOR PROFILE PICTURE----------------------

UPLOAD_FOLDER = 'app/static/uploads/profile'

@pages_bp.route('/profile', methods=['GET', 'POST'])
def profile():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)

    # 🔥 IMAGE UPLOAD
    if request.method == 'POST':

        file = request.files.get('profile_image')

        if file and file.filename != "":
            filename = secure_filename(file.filename)

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            user.profile_image = filename
            db.session.commit()

            flash("Profile updated successfully!", "success")

        return redirect(url_for('pages.profile'))

    return render_template('user/profile.html', user=user)




#--------------------------------------ABOUT AQI ROUTE----------------------------------------------

#ABOUT US ROUTE----------------
@pages_bp.route('/about-us', methods=['GET'])
def about_us():
    """Route to render the About Us page."""
    return render_template('about/about_us.html')


#CONTACT US ROUTE------------------
@pages_bp.route('/contact-us', methods=["POST", "GET"])
def contact_us():
    user_id = session.get('user_id')
    if 'user_id' not in session:
        flash('Please log in to contact us.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        #Save to DB
        contact = ContactMessage(
            name=name,
            email=email,
            message=message
        )

        from app import db
        db.session.add(contact)
        db.session.commit()

        # Here, you would typically process the contact form data,
        # such as saving it to a database or sending an email.

        flash("Thank you for contacting us! We will get back to you soon.", "success")
        return redirect(url_for('pages.contact_us'))
    """Route to render the Contact Us page."""
    return render_template('about/contact_us.html')


#aqi monitoring route---------------------
@pages_bp.route('/aqi-monitor', methods=["GET"])
def aqi_monitor():
    """Route to render the AQI Monitoring page."""
    return render_template('about/aqi_monitor.html')


#CLIMATE CHANGE ROUTE------------------------
@pages_bp.route('/climate-change', methods=["GET"])
def climate_change():
    """Route to render the Climate Change page."""
    return render_template('about/climate_change.html')


#WORLD AIR QUALITY REPORT ROUTE---------------------
@pages_bp.route('/world-air-quality-report', methods=["GET"])   
def world_air_quality_report():
    
    if 'user_id' not in session:
        flash('Please log in to access the World Air Quality Report.', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('about/world_air_quality_report.html')

    # if request.method == "POST":
    #     name = request.form.get('name')
    #     email = request.form.get('email')
    #     organization = request.form.get('organization')

    #     # Here, you would typically fetch and process the report data for the specified year.
    #     flash(f"Displaying World Air Quality Report for the year {year}.", "info")
    #     return redirect(url_for('pages.world_air_quality_report'))
    # """Route to render the World Air Quality Report page."""
    # return render_template('about/world_air_quality_report.html')


#DOWNLOAD REPORT ROUTE---------------------
@pages_bp.route('/reports/download/<int:report_id>', methods=["GET", "POST"])
def download_report(report_id):

    # login check
    if 'user_id' not in session:
        flash('Please log in to download the report.', 'warning')
        return redirect(url_for('auth.login'))
    

    # Form data
    name = request.form.get('name')
    email = request.form.get('email')
    organization = request.form.get('organization')

    if not name or not email:
        flash("Nme and Email are required.", "danger")
        return redirect(url_for('pages.report_detail', report_id=report_id))
    


    #DB se report uthao
    report = Report.query.get_or_404(report_id)


    #Save user request in reportRequest table
    req = reportRequest(
        name = name,
        email = email,
        organization = organization,
        report_id = report.id
    )


    #ab esko db me add krte hain
    from app import db
    db.session.add(req)
    db.session.commit()


    #static/reports foldeer ka absolute path bnao
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), #Getting the project root directory
        'static', 'reports'
    )

    # “I used current_app.root_path to avoid path issues”
    #PDF file download karwao
    return send_from_directory(
        directory = reports_dir,
        path = report.file_name,
        as_attachment = True
    )


    # if not name or not email:
    #     flash("Please field in all required fields.", "danger")
    #     return redirect(url_for('pages.world_air_quality_report'))
    
    # report = Report.query.filter_by(year=2024).first() # Fetch report for year 2024
    



    # # Prepare the file path for sending the report
    # # Flask app ka working directory project root hota hai
    # reports_dir = os.path.join(
    #     current_app.root_path,
    #     'static', 'reports'
    # )
    

#-------------------------------------------AIR QUALITY ROUTES--------------------------------------

#AIR POLLUTION ROUTE---------------------------
@pages_bp.route('/air-pollution', methods=["GET"])
def air_pollution():
    """Route to render the Air Pollution page."""
    return render_template('air/air_pollution.html')


#HEALTH IMPACT ROUTE-------------------------------
@pages_bp.route('/health-impacts', methods=["GET"])
def health_impacts():
    """Route to render the Health Impacts of Air Pollution page."""
    return render_template('air/health_impacts.html')


#AQI STANDARDS ROUTE-----------------------------
@pages_bp.route('/aqi-standards', methods=["GET"])
def aqi_standards():
    """Route to remder the AQI Standards page."""
    return render_template('air/aqi_standards.html')


#POLLUTION SOURCES ROUTE---------------------------
@pages_bp.route('/pollution-sources', methods=["GET"])
def pollution_sources():
    """Route to render the Pollution Sources page."""
    return render_template('air/pollution_sources.html')


#AQI APIS ROUTE-----------------------------
@pages_bp.route('/aqi-apis', methods=["GET"])
def aqi_apis():
    if 'user_id' not in session:
        flash('Please log in to access the AQI APIs.', 'warning')
        return redirect(url_for('auth.login'))
    
    """route to render the AQI APIs page."""
    return render_template('air/aqi_apis.html')
 

#FIND AQI BY CITY ROUTE------------------------------
@pages_bp.route('/find-aqi-by-city', methods=["GET"])
def find_aqi_by_city():
    """route to render the Find AQI by City page."""
    return render_template('air/find_aqi_by_city.html')

# air_quality_bp = Blueprint(
#     "air_quality",
#     __name__,
#     # url_prefix="/air-quality"
# )

# @pages_bp.route("/find-city", methods=["POST", "GET"])
# def find_city():
#     form=CitySearchForm()
#     result=None

#     if form.validate_on_submit():
#         city_name = form.city.data

#         #service call will come here later
#         result = city_name #Placeholder

#     return render_template("air/find_aqi_by_city.html", form=form, result=result)



#FIND AQI BY COUNTRY ROUTE-----------------------------
@pages_bp.route('/find-aqi-by-country', methods=["GET"])
def find_aqi_by_country():
    """Route to render the Find AQI by Country page."""
    return render_template('air/find_aqi_by_country.html')


#GLOBAL AQI MAP ROUTE----------------------------
@pages_bp.route('/global-aqi-map', methods=["GET"])
def global_aqi_map():
    """Route to render the Global AQI Map page."""
    return render_template('air/global_aqi_map.html')




#-------------------------------------------------RANKINGS  ROUTES-------------------------------------------

#CITY RANKINGS ROUTE----------------------------
@pages_bp.route('/city-rankings', methods=["GET"])
def city_rankings():
    """Route to render the City Rankings page."""
    return render_template('rankings/city_rankings.html')


#COUNTRY RANKINGS ROUTE----------------------------
@pages_bp.route('/country-rankings', methods=["GET"])
def country_rankings():
    """Route to render the Country Rankings page."""
    return render_template('rankings/country_rankings.html')


#Most Polluted Cities RANKINGS ROUTE--------------------
@pages_bp.route('/most-polluted-cities', methods=["GET"])
def most_polluted_cities():
    """route to render the Most Polluted Cities Rankings page."""
    return render_template('rankings/most_polluted_cities.html')


#CLEANEST CITIES RANKINGS ROUTE-------------------
@pages_bp.route('/cleanest-cities', methods=["GET"])
def cleanest_cities():
    """Route to render the Cleanest Cities Ranki9ngs page."""
    return render_template('rankings/cleanest_cities.html')


#HISTORICAL DATA ROUTE----------------------------
@pages_bp.route('/historical-data', methods=["GET"])
def historical_data():
    """Route to render the Historical Data page."""
    return render_template('rankings/historical_data.html')


#WEATHER IMPACT ROUTE-------------------------------
@pages_bp.route('/weather-impact', methods=["GET"])
def weather_impact():
    """Route to render the Weather Rankings page."""
    return render_template('rankings/weather_impact.html')



#----------------------------LOCATION  ROUTES-----------------------



#----------------------------REPORT LIST ROUTE-----------------------
@pages_bp.route('/reports')
def reports_list():
    #Login check
    if 'user_id' not in session:
        flash("Please login to access reports.", "warning")
        return redirect(url_for('auth.login'))
    
    #Db se sare reports fetch krte hain
    reports = Report.query.order_by(Report.year.desc()).all()

    return render_template('reports/reports_list.html', reports=reports)


#----------------------------REPORT DETAIL ROUTE-----------------------
@pages_bp.route('/reports/<int:report_id>')
def report_detail(report_id):
    #Login check
    if 'user_id' not in session:
        flash("Please login to access report details.", "warning")
        return redirect(url_for('auth.login'))
    
    #Db se specific report fetch krte hain
    report = Report.query.get_or_404(report_id)

    return render_template('reports/report_detail.html', report=report)








#-------------------------------------------------ADMIN Upload Report Route (Backend)----------------------
from werkzeug.utils import secure_filename
from app.utils.admin import admin_required
from app import db
from app.models import  ContactMessage
import os

# ------------------------ ADMIN MANAGE REPORTS ----------------
@pages_bp.route('/admin/reports')
def admin_reports():

    #Admin check
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    #fetch all reports
    reports = Report.query.order_by(Report.year.desc()).all()

    return render_template('admin/manage_reports.html', reports=reports)



#--------------Admin ke liye messages dekhne ka page---------------
# ---------------- ADMIN CONTACT MESSAGES ----------------
@pages_bp.route('/admin/contact-messages')
@pages_bp.route('/admin/contact-messages/<int:message_id>')
def contact_messages(message_id=None):

    # Admin check
    if not admin_required():
        return redirect(url_for('auth.login'))

    # All messages (latest first)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()

    selected_message = None

    if message_id:
        selected_message = ContactMessage.query.get_or_404(message_id)

        # Auto mark as read when opened
        if not selected_message.is_read:
            selected_message.is_read = True
            db.session.commit()

    return render_template(
        "admin/contact_messages.html",
        messages=messages,
        selected_message=selected_message,
        timedelta=timedelta
    )


# -----------------------------Admin Mark Message as Read----------------------
@pages_bp.route('/admin/message/read/<int:msg_id>')
def mark_message_read(msg_id):

    if not admin_required():
        flash("Admin login required", "danger")
        return redirect(url_for('auth.login'))
    
    msg = ContactMessage.query.get_or_404(msg_id)

    msg.is_read = True
    db.session.commit()

    return redirect(url_for('pages.contact_messages'))

# -----------------------------ADMIN Message Delete BUtton----------------------
@pages_bp.route('/admin/message/delete/<int:msg_id>', methods=["POST"])
def delete_message(msg_id):

    if not admin_required():
        flash("Admin login required", "danger")
        return redirect(url_for('auth.login'))
    
    msg = ContactMessage.query.get_or_404(msg_id)

    db.session.delete(msg)
    db.session.commit()

    flash("Message deleted successfully", "success")
    return redirect(url_for('pages.contact_messages'))


#--------------------------ADMIN UPLOAD REPORT-----------
@pages_bp.route('/admin/upload-report', methods=["GET", "POST"])
def upload_report():

    #Admin Check
    if not admin_required():
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        year = request.form.get('year')
        file = request.files.get('pdf')

        #Validation 
        if not title or not year or not file:
            flash("All fields are required", "danger")
            return redirect(request.url) # 
        
        #Secure file name
        filename = secure_filename(file.filename)

        #Save path -> static/reports
        reports_dir = os.path.join(
            current_app.root_path,
            'static',
            'reports'
        )
        os.makedirs(reports_dir, exist_ok=True) #

        file.save(os.path.join(reports_dir, filename))

        #Save entry in DB
        report = Report(
            title=title,
            description=description,
            year=int(year),
            file_name=filename
        )

        db.session.add(report)
        db.session.commit()

        flash("Report uploaded successfully", "success")
        return redirect(url_for('pages.admin_reports'))
    
    return render_template('admin/upload_report.html')



#----------------------ADMIN DELETE REPORT----------------------
@pages_bp.route('/admin/report/delete/<int:report_id>', methods=["POST"])
def delete_report(report_id):

    #Admin check
    if not admin_required():
        return redirect(url_for('auth.login'))

    report = Report.query.get_or_404(report_id)

    #PDF file path
    reports_dir = os.path.join(
        current_app.root_path,
        'static', 'reports'
    )

    file_path = os.path.join(reports_dir, report.file_name)

    #Delete PDF file if exist
    if os.path.exists(file_path):
        os.remove(file_path)


    #Delete DB entry
    db.session.delete(report)
    db.session.commit()

    flash("Report deleted successfully", "success")
    return redirect(url_for('pages.admin_reports'))


# ---------------------- ADMIN USERS --------------------------

@pages_bp.route('/admin/users')
def admin_users():

    #admin check
    if session.get('role') != 'admin':
        abort(403) #Forbidden

    users = User.query.all() #Model se sare users fetch krlo

    return render_template('admin/manage_users.html', users=users)



# -----------------------------------DELETE USER (ADMIN) -----------------------
@pages_bp.route('/admin/delete-user/<int:user_id>', methods=["POST"])
def delete_user(user_id):

    # Admin check
    if session.get('role') != 'admin':
        abort(403) #Forbidden

    # User fetch
    user = User.query.get_or_404(user_id)

    # Safety Admin khud ko delete na karke
    if user.role == 'admin':
        flash("Admin users cannot be deleted!", "erroe")
        return redirect(url_for('pages.admin_users'))
    
    # Delete user
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully!", "success")
    return redirect(url_for('pages.admin_users'))


# ---------------------- MANAGE PREDICTION(ADMIN) --------------------------------------
@pages_bp.route('/admin/predictions')
def admin_predictions():

    # Admin check
    if session.get('role') != 'admin':
        abort(403)


    # DB se data fetch
    predictions = Prediction.query.order_by(Prediction.predicted_at.desc()).all()

    return render_template('admin/manage_predictions.html', predictions=predictions)

# ---------------------- DELETE PREDICTION (ADMIN) ----------------------
@pages_bp.route('/admin/delete-prediction/<int:pred_id>', methods=["POST"])
def delete_prediction(pred_id):

    if session.get('role') != 'admin':
        abort(403)

    pred = Prediction.query.get_or_404(pred_id)

    db.session.delete(pred)
    db.session.commit()

    flash("Prediction deleted successfully!", "success")

    return redirect(url_for('pages.admin_predictions'))



# ---------------------- MANAGE REPORT REQUESTS (ADMIN) ----------------------
@pages_bp.route('/admin/report-requests')
def admin_report_requests():

    if session.get('role') != 'admin':
        abort(404)

    request = reportRequest.query.order_by(reportRequest.requested_at.desc()).all()

    return render_template('admin/manage_report_requests.html', requests=request, timedelta=timedelta)






#-------------------------------------END OF FILE-------------------------------------------