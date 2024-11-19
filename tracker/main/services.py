import csv
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from celery import shared_task

from .models import Task, UserModel
from reportlab.pdfgen import canvas
from io import StringIO
import tempfile


@shared_task
def generate_project_csv(project_id: int):
    output = StringIO()
    writer = csv.writer(output)
    print('lol')
    writer.writerow(["Title", "assignee", "tester", "status", "priority"])

    tasks = Task.objects.all().filter(project_id=project_id)
    for task in tasks:
        assignee, tester = None, None
        if task.assignee:
            assignee = UserModel.objects.get(id=task.assignee.id).username
        if task.tester:
            tester = UserModel.objects.get(id=task.tester.id).username
        writer.writerow([
            task.title,
            assignee,
            tester,
            task.status,
            task.priority,
        ])
    return output.getvalue()


@shared_task
def generate_pdf_file(project_id: int, project_name: str):
    pdfmetrics.registerFont(TTFont("font", os.path.abspath("font.ttf")))

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as temp_file:
        temp_filepath = temp_file.name
        p = canvas.Canvas(temp_filepath)

        tasks = Task.objects.filter(project_id=project_id)
        p.setFont("font", 12)
        p.drawString(100, 750, f"Tasks for project {project_name}")

        y = 700
        for task in tasks:
            assignee = task.assignee.username if task.assignee else None
            tester = task.tester.username if task.tester else None
            p.drawString(100, y, f"Title: {task.title}")
            p.drawString(100, y - 20, f"Assignee: {assignee}")
            p.drawString(100, y - 40, f"Tester: {tester}")
            p.drawString(100, y - 60, f"Status: {task.status}")
            p.drawString(100, y - 80, f"Priority: {task.priority}")
            y -= 150
        p.showPage()
        p.save()

    return temp_filepath
