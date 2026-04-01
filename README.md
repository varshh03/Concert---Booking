# 🎟️ Concert Pro: Advanced Event Booking System

A professional, role-based desktop application built with **Python**, **Tkinter**, and **MySQL**. This system provides a seamless interface for users to book tickets and for administrators to manage event inventories with real-time data visualization.

---

## 🌟 Key Features

### 🔐 Secure Role-Based Authentication
* **Integrated Login/Registration:** Users can create accounts and choose roles (Admin or User).
* **Role-Specific Dashboards:** The UI dynamically adapts based on the logged-in user's permissions.

### 🛠️ Admin Dashboard (CRUD Operations)
* **Event Management:** Add new events with detailed parameters (Name, Venue, Date, Price, and Total Tickets).
* **Data Visualization:** Integrated **Matplotlib** analytics to track ticket availability and sales trends visually.
* **Database Control:** Direct synchronization with MySQL for real-time inventory updates.

### 👤 User Dashboard
* **Live Event Feed:** Browse all available events with up-to-date pricing and ticket counts.
* **Smart Booking:** Automated calculation of total costs based on ticket quantity.
* **Email Automation:** Leverages **SMTP (smtplib)** to send instant, automated booking confirmations to the user's registered email address.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.x |
| **Frontend UI** | Tkinter (Custom Modern UI) |
| **Database** | MySQL (Relational Schema) |
| **Visualization** | Matplotlib |
| **Communication** | SMTP / MIME (Gmail API Integration) |

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10 or higher.
* MySQL Server installed and running.
* `pip install mysql-connector-python matplotlib`

### 2. Database Configuration
1. Open your MySQL terminal or Workbench.
2. The application is designed to automatically initialize the `EventDB` and required tables (`users`, `events`, `bookings`) upon the first successful connection.
3. **Important:** Update the `db_config` in the script with your local MySQL password.

### 3. Email Setup
To enable automated emails:
* Use a Gmail account with **2-Factor Authentication** enabled.
* Generate an **App Password** from your Google Account settings and paste it into the `sender_password` variable.

### 4. Run the Application
python concert.py
