from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status

from .models import Person, OperationStatus
from .serializers import PersonSerializer

import datetime
import csv
import time

class FileUploadView(APIView):
	"""Class based view to handle File Upload operation"""

	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, format=None):
		file_obj = request.data['file']

		# creating a new record in OperationStatus table to track the user actions on this particular operation.
		OperationStatus.objects.create(user=request.user, operation='upload', objectName=file_obj.name, status=1)

		upload_status = self.persist_data(request, file_obj)

		if upload_status == 'success':
			msg = "file uploaded successfully"
		else:
			msg = "file upload aborted"
		return Response({
			"message": msg,
			"db_object_count": Person.objects.count()
			})

	def persist_data(self, request, file_obj):
		""" 
		Saves the file object to the database.
		The persistence is done in a batch wise manner.
		On each batch execution the user actions(ie user whether user decides to stop or terminate) on this
		operation is checked and execution flow is done accordingly.
		"""
		bulk_objs = []
		upload = datetime.datetime.now()
		file_name = file_obj.name 
		batch_size = 100

		for line in file_obj:
			rec = line.decode('utf-8').split(',')
			if rec[0].lower() == 'index':
				continue # skipping the header in csv file

			# creating the bulk object to store the Person records
			bulk_objs.append(Person(height=rec[1], weight=rec[2], uploaded=upload, from_file=file_name))
			time.sleep(0.1) # to add time delay

			if len(bulk_objs) == batch_size:
				# checking the user actions of this operations
				op_status = OperationStatus.objects.filter(user=request.user, operation='upload', objectName=file_obj.name).get()
				wait_time = 0
				while(op_status.status == 2 and wait_time < 6):
					"""
						this block handles the case when the user has requested to stop the execution 
						but has not decided to terminate or resume the process.
						We allow the user a time period of 3 minutes to make the decision to terminate or resume
					"""
					print('operation set to stop, waiting for user to either resume or terminate')
					time.sleep(30)
					wait_time += 1
					op_status = OperationStatus.objects.filter(user=request.user, operation='upload', objectName=file_obj.name).get()

				if op_status.status == 4 or op_status.status == 2:
					"""
					   if the user decides to terminate the process(denoted by number 4)
					   or if the status is still in stop state(denoted by number 2) we default it to termination.
					   We also delete if any records are inserted to database by this operation.
					"""
					print('aborting operation')
					Person.objects.filter(from_file=file_name, uploaded__gte=upload).delete()
					OperationStatus.objects.filter(user=request.user, operation='upload', objectName=file_obj.name).delete()
					return 'aborted'

				# inserting to db if the user decides to resume the operation(denoted by number 3)
				print('inserting to database')
				Person.objects.bulk_create(bulk_objs, batch_size)
				bulk_objs = []

		if len(bulk_objs) > 0:
			Person.objects.bulk_create(bulk_objs, batch_size)
			bulk_objs = []
		OperationStatus.objects.filter(user=request.user, operation='upload', objectName=file_obj.name).delete()
		return 'success'


class PersonCSVExportView(APIView):
	"""Class based View to handle file download operation."""

	serializer_class = PersonSerializer

	def get(self, request, *args, **kwargs):
		"""
			method that server the request to download the database record as a csv file.
			This method also follows the same approach as file upload to track for any user action on this operation.
		"""
		
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachement; filename="persons.csv"'
		serializer = self.serializer_class(Person.objects.all(), many=True)
		header = self.serializer_class.Meta.fields
		batch_size = 50
		# print(header)
		OperationStatus.objects.create(user=request.user, operation='download', objectName='persons.csv', status=1)

		writer = csv.DictWriter(response, fieldnames=header)
		writer.writeheader()
		for index, row in enumerate(serializer.data):
			writer.writerow(row)
			time.sleep(0.1)
			print(index)
			if index % batch_size == 0:
				op_status = OperationStatus.objects.filter(user=request.user, operation='download', objectName='persons.csv').get()
				wait_time = 0
				while(op_status.status == 2 and wait_time < 6):
					print('operation set to stop, waiting for user to either resume or terminate')
					time.sleep(30)
					wait_time += 1
					op_status = OperationStatus.objects.filter(user=request.user, operation='download', objectName='persons.csv').get()

				if op_status.status == 4 or op_status.status == 2:
					print('aborting operation')
					OperationStatus.objects.filter(user=request.user, operation='download', objectName='persons.csv').delete()
					return HttpResponse('operation aborted')

		OperationStatus.objects.filter(user=request.user, operation='download', objectName='persons.csv').delete()
		return response

class ChangeExecutionStatus(APIView):
	"""Class based view to allow user to change the action on any operation started"""

	def post(self, request, *args, **kwargs):
		user = request.user
		objectName = request.data['objectName']
		operation = request.data['operation']
		status = request.data['action']

		op_status = OperationStatus.objects.filter(user=user, objectName=objectName, operation=operation).get()
		op_status.status = status
		op_status.save()

		return Response({
				"message": "operation status changed."
			})
