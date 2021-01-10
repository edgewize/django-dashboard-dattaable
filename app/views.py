# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app.models import Wave


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'
    waves = Wave.objects.all()
    context['waves'] = waves
    flow = hydrofunctions.NWIS("13206000",  'dv', period="P10D")
    context['flow'] = format_site_data(flow)
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def wave(request):
    site_id = request.GET.get('site_id')
    if site_id is None:
        site_id = "13206000"
    flow = hydrofunctions.NWIS(site_id,  'dv', period="P10D")
    context = {}
    context['segment'] = 'wave'
    context['site_id'] = site_id
    context['wave'] = format_site_data(flow)
    html_template = loader.get_template('wave.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def build(request):
    wave_info = [{'name': 'Boise', 'site_id': 13206000},
                 {'name': 'Lochsa', 'site_id': 13337000}]
    [i.delete() for i in Wave.objects.all()]
    [Wave.objects.create(name=i['name']) for i in wave_info]
    context = {}
    context['segment'] = 'build'
    html_template = loader.get_template('build.html')
    waves = Wave.objects.all()
    context['waves'] = waves
    return HttpResponse(html_template.render(context, request))


@ login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
