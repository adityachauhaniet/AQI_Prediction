# 🌍 AQI Prediction System

A full-stack web application that predicts **Air Quality Index (AQI)** using machine learning and provides an admin panel for managing users, reports, and predictions.

---

## 🚀 Features

### 👤 User Features

* 🔐 User Authentication (Login/Register)
* 📊 Predict AQI using pollutant inputs:

  * CO
  * NO₂
  * Ozone
  * PM2.5
* 📄 View and download air quality reports
* 👤 User Profile (update info & upload profile photo)

---

### 🛠️ Admin Panel

* 📊 Dashboard with system statistics
* 👥 Manage Users (view & delete)
* 📈 Manage Predictions (view & delete)
* 📁 Manage Reports (upload, view, delete)
* 📩 Manage Report Requests
* 📬 View Contact Messages

---

## 🧠 Machine Learning Model

* Model Used: **RandomForestRegressor**
* Trained on pollutant concentration data
* Inputs:

  * CO, NO₂, Ozone, PM2.5
* Output:

  * Predicted AQI value
* Model is saved using **Pickle (.pkl)** and loaded in the Flask app

---

## 🛠️ Tech Stack

### 🔹 Backend

* Flask
* Flask-SQLAlchemy
* Flask-WTF

### 🔹 Frontend

* HTML, CSS
* JavaScript
* Jinja2 Templates

### 🔹 Machine Learning

* Scikit-learn
* Pandas
* NumPy

### 🔹 Deployment

* Gunicorn
* Render

---

## 📂 Project Structure

```
AQI_Prediction/
│── app/
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   ├── static/
│
│── instance/
│── run.py
│── requirements.txt
│── Procfile
│── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AQI_Prediction.git
cd AQI_Prediction
```

### 2️⃣ Create virtual environment

```bash
python -m venv myenv
myenv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
python run.py
```

---

## 🔐 Default Admin Setup

To create an admin user, run:

```bash
python create_admin.py
```

---

## 🌐 Deployment

This project is deployed using **Render**.

Steps:

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Set build command:

   ```
   pip install -r requirements.txt
   ```
4. Set start command:

   ```
   gunicorn run:app
   ```

---

## 🎨 UI Highlights

* 🌙 Dark Mode Support
* 📱 Fully Responsive Design
* 📊 Mobile-friendly tables (converted to cards)
* 🧭 Admin Sidebar Navigation

---

## 🔒 Security Features

* Password hashing using Werkzeug
* Session-based authentication
* Role-based access control (Admin/User)

---

## 📌 Future Improvements

* 🌍 Real-time AQI using external API
* 📊 Data visualization (charts)
* 📈 AQI trend analysis

---

## 👨‍💻 Author

**Aditya Chauhan**

* GitHub: https://github.com/adityachauhaniet
* Email: [adityachauhanietlko22@gmail.com](mailto:adityachauhanietlko22@gmail.com)
* Available at your primary URL https://aqi-prediction-wkbe.onrender.com

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
