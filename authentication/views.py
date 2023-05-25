# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from .utils.enums.vulnerability import Vulnerability
from django.http import HttpResponse
from django.http import FileResponse
from django.template.loader import get_template
from django.db import IntegrityError
from .models import Companie
from .models import ReportVulnerability
from .forms import CompanieForm
from .forms import ResportVulnForm
from .utils.enums.level import Level
import os
import tempfile
import pygal
import json
from weasyprint import HTML
from pygal.style import Style


def home(request):
    companie = Companie.objects.filter(created_by=request.user)
    data = []
    labels = []
    for i in list(Vulnerability):
        d = {}
        d['name'] = i.value
        for com in companie:
            c = ReportVulnerability.objects.filter(
                companie=com.id,
                vulnerability=i.value).count()
            d[com.name] = c
            labels.append(com.name)
        data.append(d)
    return render(request, 'dashboard.html', {
        'companie': companie,
        'data': json.dumps(data),
        'labels': json.dumps(list(set(labels)))})


def signup(request):
    context = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        return render(
            request,
            'signup.html',
            context
        )
    else:
        if context['password1'] == context['password2']:
            try:
                user = User.objects.create_user(
                    username=context['username'],
                    password=context['password1'],
                )
                user.save()
                return redirect('login')
            except IntegrityError:
                context['feedback'] = 'User already exist'
                return render(
                    request,
                    'signup.html',
                    context
                )
        context['feedback'] = 'Password do not match'
        return render(
            request,
            'signup.html',
            context
        )


def login(request):
    context = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        return render(
            request,
            'login.html',
            context
        )
    else:
        user = authenticate(
            request,
            username=context['username'],
            password=context['password1']
        )
        if not user:
            context['feedback'] = 'Username or password is incorrect'
            return render(request, 'login.html', context)
        else:
            auth_login(request, user)
            return redirect('home')


def signout(request):
    logout(request)
    return redirect('signup')


def create_companie(request):
    context = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        companies = Companie.objects.filter(created_by=request.user)
        context['companies'] = companies
        return render(
            request,
            'create_companie.html',
            context
        )
    else:
        try:
            companie = CompanieForm(request.POST)
            new_companie = companie.save(commit=False)
            new_companie.created_by = request.user
            new_companie.save()
            return redirect('create_companie')
        except IntegrityError:
            context['feedback'] = 'Companie already exist'
            return render(
                request,
                'create_companie.html',
                context
            )


def delete_companie(request, companie_id):
    companie = get_object_or_404(
        Companie, pk=companie_id, created_by=request.user)
    if request.method == "GET":
        companie.delete()
        return redirect('create_companie')


def detail_companie(request, companie_id):
    context = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        companie = Companie.objects.get(id=companie_id)
        vulns = ReportVulnerability.objects.filter(companie=companie_id)
        context['vulnerabilities'] = vulns
        context['companie'] = companie
        context['levels'] = [e.value for e in Level]
        context['vulns'] = [e.value for e in Vulnerability]
        return render(
            request,
            'detail_companie.html',
            context
        )


def create_vul(request):
    context = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'POST':
        try:
            report_vul = ResportVulnForm(request.POST)
            if report_vul.is_valid():
                new_report = report_vul.save(commit=False)
                new_report.created_by = request.user
                companie = Companie.objects.get(id=context['companie_id'])
                new_report.companie = companie
                new_report.save()
                return HttpResponseRedirect('/companie'+'/'+context['companie_id']+'/')
            else:
                return HttpResponseRedirect('/companie'+'/'+context['companie_id']+'/')
        except IntegrityError:
            return HttpResponseRedirect('/companie'+'/'+context['companie_id']+'/')
    else:
        return redirect('detail_companie')


def delete_vul(request, vuln_id):
    vuln = get_object_or_404(
        ReportVulnerability, pk=vuln_id, created_by=request.user)
    if request.method == "GET":
        vuln.delete()
        return HttpResponseRedirect('/companie'+'/'+str(vuln.companie.id)+'/')


def general_report_by_companie(request, companie_id):
    try:
        vulns = ReportVulnerability.objects.filter(companie=companie_id)
        companie = Companie.objects.get(id=companie_id)
        template = get_template('pdf_report.html')

        custom_style = Style(
            colors=('#0343df', '#e50000', '#ffff14', '#929591'),
            font_family='DejaVu Sans',
            background='transparent',
            label_font_size=14,
        )

        # Set up the bar plot, ready for data
        chart = pygal.Bar(
            title=f"{companie.name} Results",
            style=custom_style,
            y_title='Number of vulnerabilities',
            width=900,
            x_label_rotation=270,
        )

        # Agrega datos al gráfico
        for i in list(Vulnerability):
            c = ReportVulnerability.objects.filter(
                companie=companie_id,
                vulnerability=i.value).count()
            chart.add(i.value, c)

        # Renderiza el gráfico como SVG
        svg = chart.render().decode('utf-8')

        html = template.render(
            {'vulns': vulns, 'username': request.user.username, 'chart_svg': svg})

        # Create a temporary file to store the PDF
        pdf_file = tempfile.NamedTemporaryFile(delete=False)

        # Generate the PDF using weasyprint
        HTML(string=html).write_pdf(pdf_file)

        # Close the temporary file
        pdf_file.close()

        # Create a response with the PDF file
        response = FileResponse(open(pdf_file.name, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # Delete the temporary file
        os.unlink(pdf_file.name)

        return response
    except Exception as e:
        print(str(e))
