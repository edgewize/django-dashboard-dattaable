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
import app.lib.RiverWave as RiverWave
import app.components


def index(request):
    waves_in_db = Wave.objects.all()
    waves = [RiverWave.View(i.site_id, 'dv', period='P10D') for i in waves_in_db]
    infos = [i.info() for i in waves]
    context = {}
    context['segment'] = 'index'
    context['waves'] = infos
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def wave(request):
    site_id = request.GET.get('site_id')
    if site_id is None:
        site_id = "13206000"
    wave = RiverWave.View(site_id, 'dv', period="P30D")
    context = {}
    context['segment'] = 'wave'
    context['site_id'] = site_id
    context['wave'] = wave.build()
    html_template = loader.get_template('wave.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def build(request):
    wave_info = [{'name': 'Boise Whitewater Park', 'site_id': '13206000', 'in_level': 250, 'awesome_level': 550},
                 {'name': 'Lochsa Pipeline', 'site_id': '13337000', 'in_level': 8000, 'awesome_level': 10000}]
    [i.delete() for i in Wave.objects.all()]
    [Wave.objects.create(name=i['name'], site_id=i['site_id'], in_level=i['in_level'],
                         awesome_level=i['awesome_level']) for i in wave_info]
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
