# Student-Teacher-Portal

EduHub is a desktop-based **Learning Management System (LMS)** designed to bridge the gap between students and teachers. It provides a centralized platform for managing educational tasks, tracking progress, and submitting assignments through an intuitive graphical interface.

## 🚀 Overview
The system features two primary portals:
- **Teacher Portal:** Allows educators to add students, assign tasks, and monitor submissions.
- **Student Portal:** Enables students to view their specific assignments, submit solutions, and track their academic status.

## 🛠️ Tech Stack
- **Frontend:** `PyQt6` (Modern Desktop GUI).
- **Backend:** `Python` (Object-Oriented Logic).
- **Data Storage:** `JSON` (For lightweight, portable, and persistent data management).

## 📊 Project Workflow
1. **Authentication:** Users log in as either a Teacher or a Student using unique IDs.
2. **Teacher Actions:** Teachers can register new students and broadcast assignments to specific IDs.
3. **Student Actions:** Students log in to see a personalized dashboard of "Pending" and "Completed" tasks.
4. **Data Persistence:** All updates (new students, solved tasks) are automatically saved to `students_data.json` to ensure no data is lost.

## ⚙️ Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/EduHub-LMS.git](https://github.com/YourUsername/EduHub-LMS.git)
   
2. **Install required dependencies:**
   ```bash
   pip install PyQt6
 
3. **Run the Application:**
   ```bash
   python main.py
 
## 📝 Key Features
- **Role-Based Access:** Distinct interfaces and permissions for teachers and students.
- **Dynamic Task Management:** Real-time updating of assignment statuses (Pending 🔴 / Solved 🟢).
- **JSON-Based Database:** Easy to migrate and edit data without needing complex SQL setups.
- **Frameless Modern UI:** Custom-designed windows for a sleek and professional look.
- **Input Validation:** Built-in checks to ensure IDs and data fields are filled correctly
