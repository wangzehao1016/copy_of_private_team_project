from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random,datetime

class Instructor(User):
	autobiagraphy=models.TextField()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Learner(User):
	staff_ID = models.CharField(max_length=8)
	cummulative_CECU = models.IntegerField()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Category(models.Model):
	name=models.CharField(max_length=200)
	description=models.TextField()

	def __str__(self):
		return f'Category: {self.name}'


class Course(models.Model):
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)

	title = models.CharField(max_length=200)
	description = models.TextField()
	CECU_value = models.IntegerField()
	STATUS = (
		(0,'Open'),
		(1,'Pending'),
		(2,'Closed'),
	)
	status = models.IntegerField(choices=STATUS)

	def __str__(self):
		return f'Title: {self.title} | Instructor: {self.instructor.first_name} {self.instructor.last_name}'

	def setModuleAccess(self,progress):
		"""
			Each course will keep a list of accessibility of the modules
			Prams:
				- progress: the index of modules undertaking. start from 0
					(e.g. progress=3 means module3 and then on are not available)
		"""
		self.modules=Module.objects.filter(course__id=self.pk)
		self.module_access=[True if i<=progress else False for i in range(len(self.modules))]

	def updateProgress(self,progress,learnerID):
		"""
			Update the learning progress of a course for a learner
		"""
		enroll=Enroll.objects.get(course__id=self.pk,learner__id=learnerID)
		enroll.progress=progress
		enroll.save()


class Module(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	order = models.IntegerField()
	title=models.CharField(max_length=200)

	def __str__(self):
		return f'Course: {self.course.title} | Title: {self.title}'

	def takeQuiz(self):
		raise NotImplementedError

	def setOrder(self,index):
		"""
			set the position of ranking of this module inside a course
		"""
		"need to add auto manage order"
		self.order=index
		self.save()


class Component(models.Model):
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	module=models.ForeignKey(Module, default=None, null=True, blank=True, on_delete=models.SET_NULL)

	order=models.IntegerField(default=-1)
	title=models.CharField(max_length=200, blank=True)			# title of component?
	date_of_creation=models.DateField()
	date_of_lastUpdate=models.DateField()

	def __str__(self):
		return f'Course: {self.course.title} | Title: {self.title}'

	def setOrder(self,index):
		self.order=index
		self.save()


class ComponentImage(Component):
	path=models.CharField(max_length=200)


class ComponentText(Component):
	content=models.TextField()


class Quiz(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	module=models.ForeignKey(Module,null=True,blank=True,on_delete=models.SET_NULL)

	title=models.CharField(max_length=200)
	pass_score = models.IntegerField()
	num_draw=models.IntegerField()

	def __str__(self):
		return f'Course: {self.course.title} | Title: {self.title}'

	def drawQuestions(self):
		self.allQuestions=Question.objects.filter(quiz__id=self.pk)
		self.questions_drew=random.sample(self.allQuestions,self.num_draw)
		return self.questions_drew

	def getResult(self,answers):
		"""
			the answers should be in the same sequence as the questions are given
		"""
		score=0
		for i,q in enumerate(self.questions_drew):
			if q.checkAnswer(answers[i]):
				score+=1
		return score>=self.pass_score


class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

	description = models.TextField()
	option_1 = models.TextField()
	option_2 = models.TextField()
	option_3 = models.TextField()
	option_4 = models.TextField()
	answer = models.CharField(max_length=1)

	def __str__(self):
		return f'Quiz: {self.quiz.title} |Description: {self.description}'

	def checkAnswer(self,ans):
		return ans==self.answer

class Enroll(models.Model):
	learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	status = models.BooleanField()
	progress = models.IntegerField()								# modules that visible to the learner
	finish_time = models.DateField(default=None)

	def __str__(self):
		return f'{self.learner} | {self.course.title}'

	def awardCECU(self):
		"""
			award CECU to a user, should be executed only once
		"""
		if self.finish_time==None:
			learner.cummulative_CECU+=course.CECU_value
			learner.save()
			self.finish_time=datetime.date.today
			self.save()

	def setProgress(self,progress):
		self.progress=progress
		self.save()
