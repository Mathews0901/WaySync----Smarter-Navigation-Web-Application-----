# 🌐 WaySync Web Application

**WaySync** is a full-stack, role-based web application designed for unified access, intelligent navigation, and seamless interaction across user dashboards, admin tools, and partner centers. It is optimized for scalability, real-time user tracking, modular expansion, and role-based control.

---

## 🎯 Purpose & Vision

WaySync aims to eliminate the clutter of disconnected dashboards and offer a central portal where:
- Users can access tools, track progress, and earn achievements
- Centers can manage item requests and update public profiles
- Admins can verify accounts, oversee platform activity, and handle user governance

WaySync is perfect for universities, smart-city projects, internal SaaS dashboards, and digital service hubs.

---

## ✨ Core Features

### 🔐 Authentication & Role-Based Access
- Secure login/signup for users, centers, and admins
- Password hashing with bcrypt
- Flask-session or JWT token-based auth
- Auto-redirects based on role after login

### 🧭 Sidebar Navigation System
- Responsive vertical sidebar
- Hover-expandable with icon + label
- Blur glass effect with background video support
- Adaptive route highlighting

### 🖥️ User Dashboard
- Tracks XP, level, and earned badges
- Grid-style achievement system
- Auto-updating experience bar
- Interactive progress feedback

### 🏢 Center Dashboard
- View, approve, or reject item connection requests
- Modify item details: material, value, notes
- Profile update system (location, image, info)
- Changes reviewed by admin

### 🧑‍💼 Admin Panel
- Approve new centers
- Review and accept profile update requests
- View platform statistics: total users, XP earned, items processed
- Admin-specific routes protected with session

---

## 🧾 MongoDB Collections Overview

| Collection               | Purpose |
|--------------------------|---------|
| `users`                  | Stores user data (email, password, XP, badges, profile) |
| `recyclingCenters`       | Center name, profile info, status (pending/verified) |
| `center_logins`          | Center login data (hashed passwords) |
| `center_update_requests` | Temp storage for profile updates |
| `item_requests`          | Tracks user-submitted items sent to centers |
| `admin`                  | Stores admin login credentials |
| `achievements`           | XP thresholds and badge logic |

---

## 📁 Project Folder Structure

```
WaySync/
│
├── static/                          # Static files (CSS, JS, Images, Media)
│   ├── css/
│   │   ├── style.css
│   │   └── style2.css
│   ├── js/
│   │   └── script.js
│   ├── media/                       
│   └── images/                      # All UI and branding images
│       ├── 1.jpg
│       ├── 2.jpg
│       ├── 3.jpg
│       ├── admin.png
│       ├── henry-perks.jpg
│       ├── istockphoto.jpg
│       ├── login.png
│       ├── privacy.jpg
│       ├── social-follow.jpg
│       ├── unsplash.jpg
│       └── Waysync.png

├── templates/                       # Jinja2 templates rendered by Flask
│   ├── about.html
│   ├── admin.html
│   ├── dashboard.html
│   ├── features.html
│   ├── get-started.html
│   ├── login.html
│   ├── maps.html
│   ├── register.html
│   ├── signup.html
│   ├── vision.html
│   └── visited.html

├── venv/                            # Python virtual environment (excluded from version control)

├── .env                             # Environment variables (never upload to GitHub)
├── app.py                           # Main Flask application file
├── test_jwt.py                      # Script to test or debug JWT flows
├── requirements.txt                 # Python package requirements
└── README.md                        # Project documentation
```

## 🧠 Internal Functional Flow

### User Journey
1. Registers via `/signup` → stored in `users`
2. Logs in → `session['user_id']` is set
3. Redirected to `/dashboard`
4. Views XP, badges (from `achievements`)
5. Connects item → stored in `item_requests`
6. On approval → XP increases

### Center Journey
1. Registers → stored in `recyclingCenters` (status: Pending)
2. Logs in only if status = Verified
3. Accesses item requests sent by users
4. Updates values or profile → data held in `center_update_requests`
5. Admin reviews changes before applying

### Admin Journey
1. Logs in via `admin` credentials
2. Sees list of pending centers → verifies them
3. Reviews center update requests
4. Views stats and database-level analytics

---

## 🔗 Backend Session Flow

```
┌──────────────┐
│ Registration │
└──────┬───────┘
       ↓
┌────────────────────┐
│ MongoDB Inserts    │
│ users / centers DB │
└────────┬───────────┘
         ↓
  ┌─────────────┐
  │  Login Flow │
  └────┬────────┘
       ↓
┌──────────────────────┐
│ Session Created      │
└────────┬─────────────┘
         ↓
┌────────────────────────────┐
│ Dashboard or Admin Panel   │
└────────┬───────────────────┘
         ↓
┌────────────────────────────┐
│ MongoDB queries + updates  │
└────────────────────────────┘
```

---

## 🧪 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/waysync.git
cd waysync
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` File
```env
MONGO_URI=mongodb+srv://...
SECRET_KEY=your_secret_key
GOOGLE_MAPS_API_KEY=your_api_key (optional)
```

### 4. Run the Application
```bash
python app.py
```
Visit: [http://localhost:5000](http://localhost:5000)

---

## 🧠 Use Cases

- 🎓 College Portals for Student Progress & Badging
- 🏙️ Smart Cities for Center-Based Reporting
- 🧰 Admin Panels with XP/Analytics/Badge Mechanics

---

## 👥 User Role Summary

| Role     | Capabilities |
|----------|--------------|
| **User**   | Register, connect items, gain XP, view dashboard |
| **Center** | Manage requests, edit profiles, respond to items |
| **Admin**  | Approve centers, control updates, see stats |

---

✅ All static assets are organized under `static/`, and template files are neatly stored in `templates/`.

