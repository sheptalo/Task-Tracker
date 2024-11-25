import csv
import os
from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from celery import shared_task

from .models import Task, UserModel
from reportlab.pdfgen import canvas


@shared_task(serializer="pickle")
def generate_project_csv(project_id: int) -> HttpResponse:
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="export.csv"'
    writer = csv.writer(response)  # запись csv в response

    writer.writerow(["Title", "assignee", "tester", "status", "priority"])

    tasks = Task.objects.all().filter(project_id=project_id)
    for task in tasks:
        assignee, tester = None, None
        if task.assignee:
            assignee = UserModel.objects.get(id=task.assignee.id).username
        if task.tester:
            tester = UserModel.objects.get(id=task.tester.id).username

        writer.writerow(
            [
                task.title,
                assignee,
                tester,
                task.status,
                task.priority,
            ]
        )

    return response


@shared_task(serializer="pickle")
def generate_pdf_file(project_id: int, project_name: str) -> HttpResponse:
    pdfmetrics.registerFont(
        TTFont("font", os.path.join(os.getcwd(), "font.ttf"))
    )

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    tasks = Task.objects.all().filter(project_id=project_id)

    p.setFont("font", 12)
    p.drawString(100, 750, f"Tasks for project {project_name}")

    y = 700
    for task in tasks:
        assignee, tester = None, None
        if task.assignee:
            assignee = UserModel.objects.get(id=task.assignee.id).username
        if task.tester:
            tester = UserModel.objects.get(id=task.tester.id).username
        p.drawString(100, y, f"Title: {task.title}")
        p.drawString(100, y - 20, f"Assignee: {assignee}")
        p.drawString(100, y - 40, f"Tester: {tester}")
        p.drawString(100, y - 60, f"Status: {task.status}")
        p.drawString(100, y - 80, f"Priority: {task.priority}")
        y -= 150
        if y <= 50:
            p.showPage()
            p.setFont("font", 12)
            y = 800
    p.showPage()
    p.save()

    buffer.seek(0)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="export.pdf"'
    response.write(buffer.getvalue())

    return response
