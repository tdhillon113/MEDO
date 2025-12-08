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
    'paul-yang': {
        'name': 'Dr. Paul Yang',
        'role': 'Principal Investigator',
        'department': 'Department of Physics',
        'image': '/static/assets/img/theme/paul.jpg',
        'bio': 'Dr. Yang is a distinguished researcher in materials science and quantum computing. His work focuses on developing new computational methods for studying quantum systems and their applications in materials discovery.',
        'publications': 3,
        'citations': 8,
        'projects': 5,
        'email': 'paul.yang@university.edu',
        'phone': '+1 (555) 123-4567',
        'office': 'Physics Building, Room 301',
        'interests': ['Quantum Computing', 'Materials Science', 'Computational Physics', 'Quantum Simulation'],
        'recent_publications': [
            {
                'title': 'Quantum Computing Applications in Materials Science',
                'journal': 'Nature Physics',
                'year': '2025'
            },
            {
                'title': 'Novel Approaches to Quantum Simulation',
                'journal': 'Physical Review Letters',
                'year': '2024'
            },
            {
                'title': 'Machine Learning for Quantum State Preparation',
                'journal': 'Quantum',
                'year': '2024'
            }
        ],
        'current_work': [
            'Developing quantum algorithms for materials discovery',
            'Building open-source quantum simulation frameworks',
            'Collaborating on quantum machine learning applications'
        ]
    },
    'emilia-szynwald': {
        'name': 'Emilia Szynwald',
        'role': 'Graduate Research Student',
        'department': 'Department of Computer Science',
        'image': '/static/assets/img/theme/emilia.png',
        'bio': 'Emilia specializes in molecular modeling and machine learning. Her research combines cutting-edge ML techniques with traditional computational chemistry methods to predict molecular properties and accelerate drug discovery.',
        'publications': 12,
        'citations': 350,
        'projects': 8,
        'email': 'emilia.szynwald@university.edu',
        'phone': '+1 (555) 234-5678',
        'office': 'Computer Science Building, Room 215',
        'interests': ['Computational Chemistry', 'Machine Learning', 'Molecular Dynamics', 'Drug Discovery'],
        'recent_publications': [
            {
                'title': 'Machine Learning for Molecular Property Prediction',
                'journal': 'Journal of Chemical Information and Modeling',
                'year': '2025'
            },
            {
                'title': 'Neural Networks in Chemical Space Exploration',
                'journal': 'Chemical Science',
                'year': '2024'
            },
            {
                'title': 'Deep Learning for Protein-Ligand Interactions',
                'journal': 'ACS Central Science',
                'year': '2024'
            }
        ],
        'current_work': [
            'Developing ML models for predicting drug-target interactions',
            'Creating interactive visualizations for molecular simulations',
            'Building datasets for computational chemistry research'
        ]
    },
    'cameron getner': {
        'name': 'Cameron Getner',
        'role': 'Undergraduate Research Student',
        'department': 'Department of Physics',
        'image': '/static/assets/img/theme/cameron.png',
        'bio': 'Cameron is a talented undergraduate researcher specializing in computational physics and scientific visualization. Her work focuses on creating interactive tools and simulations that make complex physics concepts more accessible to students and researchers.',
        # 'publications': 0,
        # 'citations': 0,
        'projects': 1,
        'email': 'cameron.getner@hofstra.edu',
        'phone': 'placeholder',
        # 'office': 'Physics Building, Room 412',
        'interests': ['Computational Physics', 'Scientific Visualization'],
        'recent_publications': [
            {
                'title': 'Interactive Visualization Tools for Quantum Mechanics Education',
                'journal': 'Journal of Physics Education',
                'year': '2025'
            },
            {
                'title': 'Web-Based Simulation Framework for Physics Demonstrations',
                'journal': 'Computer Physics Communications',
                'year': '2024'
            },
            {
                'title': 'Real-Time Lattice Structure Visualization in Browser',
                'journal': 'Journal of Computational Physics',
                'year': '2024'
            }
        ],
        'current_work': [
            'Building interactive cell visualization tools for materials science',
            'Developing web-based physics simulation platform',
            'Creating educational resources for quantum computing concepts'
        ]
    }
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
