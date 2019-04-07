import sys
sys.path.append("..")
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.core.exceptions import SuspiciousOperation
from ..forms import *
from ..models import *

def checkCourseBelongToInstructor(course,instructor):
	if course.instructor.pk!=instructor.pk:
		raise SuspiciousOperation("Course does not belong to current instructor!")

def selectComponent(request,**kwargs):
	course_id=kwargs['course_id']
	module_id=kwargs['module_id']
	instructor=Instructor.objects.get(id=kwargs['instructor_id'])
	course=Course.objects.get(id=course_id)
	checkCourseBelongToInstructor(course,instructor)
	module=Module.objects.get(id=module_id)
	all_components=Component.objects.filter(course__id=course_id, module__isnull=True)

	template=loader.get_template("showComponent.html")
	context={'components':all_components,
			 'len_component':all_components.count(),
			 'module':module,
			 'course':course,
			 'instructor':instructor}
	return HttpResponse(template.render(context,request))


def addComponent(request,**kwargs):
	course=Course.objects.get(id=kwargs['course_id'])
	instructor=Instructor.objects.get(id=kwargs['instructor_id'])
	checkCourseBelongToInstructor(course,instructor)
	module_id=kwargs['module_id']
	component_id=kwargs['component_id']
	component=Component.objects.get(id=component_id)
	module=Module.objects.get(id=module_id)
	index=len(Component.objects.filter(module__id=module_id))
	# raise error is the component has already been assigned to a module
	if component.module:
		raise SuspiciousOperation("Invalid request; the component has been assigned to a module already")
	
	component.module=module
	component.setOrder(index)
	component.save()

	return redirect('/system/manage/{}/{}/{}/displayModuleContent/'.format(kwargs['instructor_id'],
																		   kwargs['course_id'],
																		   kwargs['module_id']))

	
def displayModuleContent(request, **kwargs):
	module_id=kwargs['module_id']
	module=Module.objects.get(id=module_id)
	course=Course.objects.get(id=kwargs['course_id'])
	instructor=Instructor.objects.get(id=kwargs['instructor_id'])
	checkCourseBelongToInstructor(course,instructor)
	all_text_components=ComponentText.objects.filter(module__id=module_id)
	all_image_components=ComponentImage.objects.filter(module__id=module_id)
	quiz=Quiz.objects.filter(module__id=module_id)
	all_components=[None for i in range(len(all_text_components)+len(all_image_components))]
	for t in all_text_components:
		t.istext=True
		all_components[t.order]=t
	for i in all_image_components:
		i.isimage=True
		all_components[i.order]=i
	len_quiz=quiz.count()
	if len_quiz>0:
		quiz=quiz[0]

	template=loader.get_template("moduleContent.html")
	context={'components':all_components,
			 'len_component':len(all_components),
			 'quiz':quiz,
			 'len_quiz':len_quiz,
			 'instructor':instructor,
			 'course':course,
			 'module':module
			 }
	return HttpResponse(template.render(context,request))

def saveOrder(request,**kwargs):
	course=Course.objects.get(id=kwargs['course_id'])
	instructor=Instructor.objects.get(id=kwargs['instructor_id'])
	checkCourseBelongToInstructor(course,instructor)
	neworder=kwargs['neworder']
	new_orders=neworder.split('-')
	new_orders=[int(x) for x in new_orders]
	components=Component.objects.filter(module__id=kwargs['module_id'])
	all_components=[None for i in range(len(components))]
	for c in components:
		all_components[c.order]=c
	for i in range(len(all_components)):
		component=all_components[i]
		indexToSet=new_orders.index(component.pk)
		# print(component)
		# print("new index:",indexToSet)
		component.setOrder(indexToSet)

	return redirect('/system/manage/{}/{}/{}/displayModuleContent/'.format(kwargs['instructor_id'],
																		   kwargs['course_id'],
																		   kwargs['module_id']))

def removeComponent(request,**kwargs):
	course=Course.objects.get(id=kwargs['course_id'])
	instructor=Instructor.objects.get(id=kwargs['instructor_id'])
	checkCourseBelongToInstructor(course,instructor)

	component=Component.objects.get(id=kwargs['component_id'])
	component.module=None
	component.order=-1
	component.save()

	#correct the order of rest components
	components=Component.objects.filter(module__id=kwargs['module_id']).order_by('order')
	index=0
	for c in components:
		c.order=index
		c.save()
		index+=1

	return redirect('/system/manage/{}/{}/{}/displayModuleContent/'.format(kwargs['instructor_id'],
																		   kwargs['course_id'],
																		   kwargs['module_id']))