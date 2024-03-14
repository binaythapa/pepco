from django.shortcuts import get_object_or_404,render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import * 
from .serializers import *
from django.http import JsonResponse
from django.views.generic import View
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from account.serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


import pandas as pd
from pandasql import sqldf
import csv
import io


def index(request):
    return render(request, 'index.html')


#User Authentication
@ensure_csrf_cookie
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@ensure_csrf_cookie
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
        
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
        
class FileUploadViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        print("this is list")
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        print("this is retrive")
        return super().retrieve(request, *args, **kwargs)
    
class ProjectUploadViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer  


class MappingUploadViewSet(ModelViewSet):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    

class Validator(APIView):
    def __init__(self):
        self.project_id = None     
    permission_classes = []    
    
    def get_project(self):
        try:
            self.project = Project.objects.get(id=self.project_id)            
            return self.project
        except Project.DoesNotExist:
            print("Project not found!")
            return None

    def get_files(self):
        if hasattr(self, 'project'):
            self.files = self.project.excel_files.all()
            return self.files
        else:
            print("Project is not fetched yet!")
            return None
        
    
    def get_mapping(self):
        if hasattr(self, 'project'):
            try:
                self.mapping = Mapping.objects.get(project=self.project)
                return self.mapping
            except Mapping.DoesNotExist:
                print("Mapping not found for this project!")
                return None
        else:
            print("Project is not fetched yet!")
            return None
 

    def get_sql(self):
        if hasattr(self, 'mapping'):
            try:
                sql_instance = Sql.objects.get(mapping=self.mapping)
                return sql_instance.sql_query
            except SQL.DoesNotExist:
                print("SQL query not found for this mapping!")
                return None
        else:
            print("Mapping is not fetched yet!")
            return None
    
    
       
    def get(self, request, *args, **kwargs):
        self.project_id = kwargs.get('project_id')

        project = self.get_project()
        files = self.get_files()
        mapping = self.get_mapping()     
        sql_query = self.get_sql()          
        
        if project and files and mapping and sql_query:  
            excel_data_dict = {}

            for file in files:
                file_path = file.file.path
                file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]    
                # Fetch the aliases from the header column of the File model
                header_aliases = file.header
                # Read the Excel file
                excel_data = pd.read_excel(file_path)
                # Rename columns using aliases
                if header_aliases:
                    excel_data.rename(columns=header_aliases, inplace=True)
                excel_data_dict[file_name_without_extension] = excel_data

            # Dynamically assign variables based on file names
            for file_name, excel_data in excel_data_dict.items():
                globals()[file_name] = pd.DataFrame(excel_data)

            print(sql_query)
            index_df = sqldf(sql_query, globals())  
            index_info = index_df.info()
            #print(test) 
            #print(test1)     
            print(index_df)  
            #print(test.info())  
            print(index_df.info())           
            
            # Convert index_df to JSON
            index_df_json = index_df.to_json(orient='records')
            #index_info_json = index_info.to_json(orient='records')
            response_data = {
                                "index_df": index_df_json
                                #,"index_info": index_info_json
                            }
            # Return index_df_json as a JSON response
            return Response(response_data,status=status.HTTP_200_OK)
        if project:            
            return None

        if files:            
            return None

        if mapping:            
            return None
        
        else:
            validation_status = {"status": "Validation failed!"}
            return Response(validation_status, status=status.HTTP_400_BAD_REQUEST)

class SqlViewSet(ModelViewSet):
    queryset = Sql.objects.all()
    serializer_class = SqlSerializer

class IndexViewSet(ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

class TerminalViewSet(ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer

    def get(self, request, *args, **kwargs):
        print("hello world")
        return super().get(request, *args, **kwargs)

class Terminal(APIView):
    def __init__(self):
        self.project_id = None     
    permission_classes = []    
    
    def get_project(self):
        try:
            self.project = Project.objects.get(id=self.project_id)            
            return self.project
        except Project.DoesNotExist:
            print("Project not found!")
            return None

    def get_files(self):
        if hasattr(self, 'project'):
            self.files = self.project.excel_files.all()
            return self.files
        else:
            print("Project is not fetched yet!")
            return None      
    

    def post(self, request, *args, **kwargs):
        # Retrieve data from request body
        sql_query = request.data.get('sql_query')        
        project_id = kwargs.get('project_id')
        print(sql_query)
        print(project_id)
            
        if project_id:            
            self.project_id = project_id            
            project = self.get_project()
            files = self.get_files()
            if project and files:
                excel_data_dict = {}
                for file in files:
                    file_path = file.file.path
                    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
                    header_aliases = file.header
                    excel_data = pd.read_excel(file_path)
                    if header_aliases:
                        excel_data.rename(columns=header_aliases, inplace=True)
                    excel_data_dict[file_name_without_extension] = excel_data

                for file_name, excel_data in excel_data_dict.items():
                    globals()[file_name] = pd.DataFrame(excel_data)

                index_df = sqldf(sql_query, globals())
                index_df_json = index_df.to_json(orient='records')
                print(index_df)
                print(index_df_json)
                return Response(index_df_json, status=status.HTTP_200_OK)

            if project:
                return None

            if files:
                return None

            else:
                validation_status = {"status": "Validation failed!"}
                return Response(validation_status, status=status.HTTP_400_BAD_REQUEST)

        else:
            error_message = {"error": "Missing 'project_id' in request body"}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
