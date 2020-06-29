from django.db import models

class Person(models.Model):
	""" Model representing the Person table"""
	height = models.DecimalField(max_digits=5, decimal_places=2)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	uploaded = models.DateTimeField()
	from_file = models.CharField(max_length=100)

	def __str__(self):
		return str(self.weight)

OPERATION_STATUS = (
	(1, 'progress'),
	(2, 'stop'),
	(3, 'resume'),
	(4, 'terminate')
	)

class OperationStatus(models.Model):
	""" Model representing the OperationStatus table"""
	user = models.CharField(max_length=50)
	operation = models.CharField(max_length=10)
	objectName = models.CharField(max_length=50)
	status = models.IntegerField(choices=OPERATION_STATUS, default=1)

	def __str__(self):
		return self.user + " is " + self.operation + " " + self.objectName
