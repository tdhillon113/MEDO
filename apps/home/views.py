# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# Sample data for contributors - in a real app, this would come from a database
CONTRIBUTORS = {
    'Paul-yang': {
        'name': 'Dr. Paul Yang',
        'role': 'Principal Investigator',
        'department': 'Department of Physics',
        'image': '/static/assets/img/theme/team-4.jpg',
        'bio': 'Dr. Yang is a distinguished researcher in materials science. His work focuses on developing new computational methods for studying such systems.',
        'publications': 10,
        'citations': 12,
        'projects': 10,
        'interests': ['Quantum Computing', 'Materials Science', 'Computational Physics'],
        'recent_publications': [
            {
                'title': 'Quantum Computing Applications in Materials Science',
                'journal': 'Nature Physics',
                'year': '2025'
            },
            {
                'title': 'Novel Approaches to Quantum Simulation',
                 
                'year': '2024'
            }
        ]
    },
    'Emilia-Szynwald': {
        'name': 'Emilia Szynwald',
        'role': 'Research student',
        'department': 'Computer Science Department',
        'image': '/static/assets/img/theme/team-1.jpg',
        'bio': 'Emilia specializes in molecular modeling. Her research combines machine learning with traditional elemental simulation methods.',
        'publications': 35,
        'citations': 850,
        'projects': 8,
        'interests': ['Computational physics', 'Machine Learning', 'Molecular Dynamics'],
        'recent_publications': [
            {
                'title': 'Machine Learning for Molecular Property Prediction',
                 
                'year': '2025'
            },
            {
                'title': 'Neural Networks in Chemical Space Exploration',
                
                'year': '2024'
            }
        ]
    },
    'james-smith': {
        'name': 'Dr. James Smith',
        'role': 'Assistant Professor',
        'department': 'Department of Physics',
        'image': '/static/assets/img/theme/team-2.jpg',
        'bio': '',
        'publications': 28,
        'citations': 650,
        'projects': 6,
        'interests': ['Physics', 'Quantum  Theory', ' '],
        'recent_publications': [
            {
                'title': ' ',
                
                'year': '2025'
            },
            {
                'title': ' ',
                
                'year': '2024'
            }
        ]
    },
       
    }

from .cell_visualization import get_cell_plots


def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def cells(request):
    """
    added: Added form handling for custom cell visualization
    - Accepts POST data: cell_type, lattice_constant, marker_size, line_width
    - Generates visualization only on form submission (POST)
    - Returns only selected cell type (square or honeycomb)
    """
    # Default values
    cell_type = 'square'
    lattice_constant = 1.0
    marker_size = 10
    line_width = 2
    cell_image = None
    
    # Handle form submission
    if request.method == 'POST':
        cell_type = request.POST.get('cell_type', 'square')
        try:
            lattice_constant = float(request.POST.get('lattice_constant', 1.0))
            marker_size = int(request.POST.get('marker_size', 10))
            line_width = float(request.POST.get('line_width', 2))
        except (ValueError, TypeError):
            # If conversion fails, use defaults
            pass
        
        # Generate only the selected cell type
        from .cell_visualization import generate_single_cell
        cell_image = generate_single_cell(cell_type, lattice_constant, marker_size, line_width)
    
    context = {
        'segment': 'cells',
        'cell_image': cell_image,
        'cell_type': cell_type,
        'lattice_constant': lattice_constant,
        'marker_size': marker_size,
        'line_width': line_width,
    }
    html_template = loader.get_template('home/cells.html')
    return HttpResponse(html_template.render(context, request))

def people(request):
    context = {
        'contributors': CONTRIBUTORS,
        'segment': 'people'
    }
    html_template = loader.get_template('home/people.html')
    return HttpResponse(html_template.render(context, request))

def profile(request, username):
    if username not in CONTRIBUTORS:
        return HttpResponseRedirect('/page-404.html')
    
    context = {
        'person': CONTRIBUTORS[username],
        'segment': 'people'
    }
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
