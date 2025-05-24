from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import random
from collections import Counter

app = Flask(__name__)
app.secret_key = 'gizli_anahtar_123'

tasks = []
daily_feedbacks = []

def get_weekly_completion_stats(tasks):
    today = datetime.now().date()
    week_start = today - timedelta(days=6)
    dates = [week_start + timedelta(days=i) for i in range(7)]

    completed_dates = [t['completed_at'].date() for t in tasks if t.get('done') and t.get('completed_at')]
    counter = Counter(completed_dates)

    data = {d.strftime('%Y-%m-%d'): counter.get(d, 0) for d in dates}
    return data

@app.route('/')
def index():
    date = datetime.now().strftime("%A, %d %B %Y")
    today_str = datetime.now().strftime('%Y-%m-%d')
    selected_date = request.args.get('date', today_str)

    motivations = [
        "Believe in yourself and all that you are. 🌟",
        "Every small step takes you closer to your goals. 🚶‍♀",
        "Focus on progress, not perfection. 📈",
        "You’re doing better than you think. 💪",
        "Discipline is choosing what you want most. ⏳",
        "Your future is created by what you do today. ✨",
        "Hard work beats talent when talent doesn’t work hard. 🔥",
        "Stay consistent. Success loves discipline. 🧠",
        "You’ve made it this far — keep going! 🚀",
        "You got this. One task at a time! ✅"
    ]
    daily_motivation = random.choice(motivations)

    # Görevleri tarihe göre filtrele
    filtered_tasks = [t for t in tasks if t.get('due_date') == selected_date]

    recent_feedbacks = daily_feedbacks[-5:]
    completion_stats = get_weekly_completion_stats(tasks)

    return render_template('index.html',
                           tasks=filtered_tasks,
                           date=date,
                           motivation=daily_motivation,
                           feedbacks=recent_feedbacks,
                           completed_tasks_per_day=completion_stats,
                           selected_date=selected_date)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    due_date = request.form.get('due_date')
    if not due_date:
        due_date = datetime.now().strftime('%Y-%m-%d')
    if task_text:
        tasks.append({
            'text': task_text,
            'done': False,
            'created_at': datetime.now(),
            'due_date': due_date
        })
    return redirect(url_for('index') + f'?date={due_date}#tasks')

@app.route('/check/<int:task_id>')
def check_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        if tasks[task_id]['done']:
            tasks[task_id]['completed_at'] = datetime.now()
        else:
            tasks[task_id].pop('completed_at', None)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/feedback', methods=['POST'])
def feedback():
    emoji = request.form.get('emoji')
    if emoji in ['😄', '😐', '😞']:
        daily_feedbacks.append({
            'emoji': emoji,
            'timestamp': datetime.now()
        })
    return redirect(url_for('index'))

# Uygulama başlatıldığında veritabanı oluşturulmalı
if __name__ == '__main__':
    app.run(debug=True)

