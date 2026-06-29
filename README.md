# SlotMate

> **Better Slots, Better Semester**

SlotMate is a Django-based web application that helps open-credit students find their desired class slots and best possible swap matches. Instead of manually searching for students, SlotMate automatically finds compatible swap partners based on opposite needs, multiple academic preferences and allows students to reveal their contact information only after mutual consent.

---
## Motivation

As a university student under an Open Credit System, we often do not get our preferred class schedules because the number of students is much higher than the available seats in each section. This frequently results in inconvenient timetables, such as having one class early in the morning and another several hours later, forcing students to spend long idle hours on campus. In some cases, students even have classes spread across six days a week, making time management even more difficult.

Although section swapping is a common solution, finding a suitable swap partner manually is challenging. Students usually rely on social media posts, messaging groups, or personal networks, which is time-consuming and often unsuccessful.

This real-life experience motivated us to develop SlotMate, a platform that simplifies the section-swapping process by helping students find compatible swap partners more efficiently.


## Table of Contents

* Overview
* Features
* Technology Stack
* System Architecture
* Matching Algorithm
* Project Structure
* Installation
* Usage
* Screenshots of website
* Future Improvements
* Team Members
* License

---

## Overview

University students often face difficulties when trying to change their class sections because of schedule conflicts, preferred faculty members, or personal time preferences.

SlotMate simplifies this process by allowing students to:

* Create slot swap requests
* Find compatible matches automatically
* Compare compatibility scores
* Send reveal requests
* Reveal personal information only after mutual agreement

The system ensures privacy while making the slot swapping process faster, safer, and more organized.


## Features

**1. User Registration & Login**

* Secure registration with university email, system doesn't accept personal emails
* User authentication through mail verification
* Session-based login and Password change support



**2. Student Profile**

* University
* Department
* Profile management



**3. Create Swap Request**

Students can enter:

Current Slot

* Course
* Section
* Faculty
* Time
* Days

Preferred Slot

* Course
* Section
* Faculty
* Time
* Days

Flexible Preferences

* Any Section
* Any Faculty
* Any Time
* Any Day



**4. Intelligent Match System**

Automatically calculates compatibility between requests.

Matching considers:

* Course
* Section
* Faculty
* Time
* Days

Shows:

* Mutual Match Score
* Compatibility Percentage



**5. Match Details**

Displays

* Both student's current slot
* Preferred slot
* Compatibility score
* Matching information



**6. Reveal Request System**

Students can:

* Send reveal request
* Accept request
* Reject request

Personal information remains hidden until both students agree.



**7. Notifications**

Receive notifications for

* New Matches
* New reveal requests
* Accepted requests
* Rejected requests



**8. Dashboard**

Dashboard includes

* Live Match Cards
* Your Swap Snapshot (Personal statistics)
* Graphical Match Insight (Details of top match)



**9. Responsive Design**

Optimized for

* Desktop
* Laptop
* Mobile Devices

---

## Technology Stack

**Backend**

* Python
* Django

**Frontend**

* HTML
* CSS
* JavaScript

**Database**

* SQLite3

**Version Control**

* Git
* GitHub

---

## Matching Algorithm

Each request is evaluated using weighted scores.

| Criteria | Weight |
| -------- | ------ |
| Course   | 35     |
| Section  | 20     |
| Time     | 15     |
| Day      | 15     |
| Faculty  | 15     |

The system calculates:

Score A → B

Score B → A

Then computes

Mutual Score = (A→B + B→A) / 2

This produces a fair compatibility percentage for both students.

---

## System Architecture

  User
   
   ↓ 
    
Django URLs

   ↓
    
 Views
  
   ↓
    
 Models
  
   ↓
    
SQLite Database

   ↓
    
Templates

   ↓
    
 Browser


---

## Project Structure

```
SLOTMATE/
│
└──slotMate_backend/
   │
   ├── slotmate_backend/
   │   ├── settings.py
   │   ├── urls.py
   │   ├── asgi.py
   │   ├── wsgi.py
   │
   ├── slotmate_app/
   │   ├── admin.py
   │   ├── apps.py
   │   ├── models.py
   │   ├── urls.py
   │   ├── views.py
   │   ├── matching.py
   │
   ├── static/
   │   ├── css/
   │   ├── js/
   │   ├── images/
   │
   ├── templates/
   │
   ├── db.sqlite3
   │
   └── manage.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Nusrat-Nawal/SlotMate.git
```

Move into project

```bash
cd SlotMate
```
Move into the Django project directory

```bash
cd slotmate_backend
```

Install dependencies

```bash
pip install django
```

Run migrations

```bash
python manage.py migrate
```

Start server

```bash
python manage.py runserver
```
Open http link

---

## Usage

1. Register an account

2. Complete your profile

3. Create a slot swap request

4. Wait for automatic matches

5. View compatibility score

6. Send reveal request

7. Accept reveal request

8. Contact your matched partner

---

## Screenshots

**Login**


**Register**


**Dashboard**


**Create Request**


**My Requests**


**Matches**


**Match Details**


**Notifications**


**Reveal Request**


---
## Future Improvements

* AI-powered recommendation system
* Chat system
* Admin moderation panel
* PostgreSQL deployment
* Cloud hosting

---

## Team Members

* Nusrat Jahan Nawal
* Nusrat Jahan Rafi

## Academic Information

SlotMate was developed as an academic project for the **Web and Internet Programming Lab** course.

The project was designed and implemented to address a real-world scheduling problem faced by university students under an Open Credit System while applying concepts of Django, HTML, CSS, JavaScript, SQL and responsive web development.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more information.

