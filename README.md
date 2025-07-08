# 🎓 Student Course Manager (Flask App)

A full-stack Flask web app for managing student academic records, calculating GPA, and visualizing performance using charts.

---

## 🚀 Features

- Add new students and course grades
- Automatically calculate GPA based on score
- View all students and their results
- Interactive GPA distribution chart (Chart.js)
- SQLite backend for storage

---

## 🧮 GPA Grading System

| Score Range | Grade Point |
|-------------|-------------|
| 70 – 100    | 4.0         |
| 60 – 69     | 3.0         |
| 50 – 59     | 2.0         |
| 45 – 49     | 1.0         |
| < 45        | 0.0         |

---

## 🖼 Sample Output

| Name       | Matric No | GPA  | Courses                      |
|------------|-----------|------|------------------------------|
| John Doe   | MAT123    | 3.33 | Math – 70, Stats – 60        |
| Jane Smith | CST101    | 2.00 | Physics – 50, Chem – 45      |

![GPA Chart Screenshot](./screenshot.png)

---

## 🛠 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/student-course-manager.git
   cd student-course-manager
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # or source venv/Scripts/activate (Git Bash)
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

---

## 📂 Project Structure

```
student-course-manager/
├── app.py
├── forms.py
├── requirements.txt
├── data.db
├── templates/
│   ├── index.html
│   ├── add_student.html
│   └── students.html
└── static/
```

---

## 🧠 Future Improvements

- Export to Excel or PDF
- User login (admin, student)
- Per-semester breakdown
- React frontend

---

## 👨‍💻 Author

**Oluwole Qwerty**  
📍 Nigeria | 🧮 Stats & Comp Sci  
🔗 [LinkedIn](https://www.linkedin.com/in/oluwole-gaius-962342260/)  
🔗 [GitHub](https://github.com/gaius033)