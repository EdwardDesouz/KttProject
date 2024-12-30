from typing import Any
from django.shortcuts import render,redirect
from KttApp.views import SqlDb
from django.views import View
from datetime import *
import pandas as pd
from KttApp.models import *
from django.http import JsonResponse 
from django.http import HttpResponse
import json
import re
from PyPDF2 import PdfReader
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
import pandas as pd
from django.db import connection
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny


def hscodelist(request):

    return render (request,'hscode/hscodefinder.html')

class PartyPage(View):
    def get(self, request):
        # Ensuring the session contains the Permit_Id key
        permit_id = request.session.get("Permit_Id")
        if not permit_id:
            return JsonResponse({"error": "Permit_Id not found in session."}, status=400)
        
        try:
            # Using raw SQL queries to fetch data
            importer = self._fetch_data("SELECT Code, Name, Name1, CRUEI FROM Importer WHERE status = 'Active' ORDER BY Code")
            inward = self._fetch_data("SELECT Code, Name, Name1, CRUEI FROM InwardCarrierAgent WHERE status = 'Active' ORDER BY Code")
            fright = self._fetch_data("SELECT Code, Name, Name1, CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Code")
            claimant = self._fetch_data("SELECT Name, Name1, CRUEI, ClaimantName, ClaimantName1, ClaimantCode, Name2 FROM ClaimantParty WHERE status = 'Active'")
            supply = self._fetch_data("SELECT Code, Name, Name1, CRUEI FROM SUPPLIERMANUFACTURERPARTY WHERE status = 'Active' ORDER BY Code")
            inhouse = self._fetch_data("SELECT InhouseCode, HSCode, Description, Brand, Model, DGIndicator, DeclType, ProductCode FROM InhouseItemCode")
            inFile = self._fetch_data(
                f"SELECT Id, Sno, Name, ContentType, Data, DocumentType, InPaymentId, FilePath, Size, PermitId, Type FROM InFile WHERE PermitId = %s", (permit_id,)
            )
            
            # Returning the data as JSON response
            return JsonResponse(
                {
                    "Infile": self._convert_to_dict(inFile, [
                        "Id", "Sno", "Name", "ContentType", "Data", "DocumentType", "InPaymentId", "FilePath", "Size", "PermitId", "Type"
                    ]),
                    "Importer": self._convert_to_dict(importer, ["Code", "Name", "Name1", "CRUEI"]),
                    "Inward": self._convert_to_dict(inward, ["Code", "Name", "Name1", "CRUEI"]),
                    "Frieght": self._convert_to_dict(fright, ["Code", "Name", "Name1", "CRUEI"]),
                    "Claimant": self._convert_to_dict(claimant, [
                        "Name", "Name1", "CRUEI", "ClaimantName", "ClaimantName1", "ClaimantCode", "Name2"
                    ]),
                    "Supply": self._convert_to_dict(supply, ["Code", "Name", "Name1", "CRUEI"]),
                    "Inhouse": self._convert_to_dict(inhouse, [
                        "InhouseCode", "HSCode", "Description", "Brand", "Model", "DGIndicator", "DeclType", "ProductCode"
                    ]),
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def _fetch_data(self, query, params=None):
        """ Executes a query and returns the result as a list of tuples """
        with connection.cursor() as cursor:
            cursor.execute(query, params if params else ())
            return cursor.fetchall()

    def _convert_to_dict(self, data, columns):
        """ Converts raw database data into a list of dictionaries """
        return pd.DataFrame(list(data), columns=columns).to_dict("records")
    
class InwardGet(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Code, Name, Name1, CRUEI FROM InwardCarrierAgent WHERE status = 'Active' ORDER BY Code")
                data = cursor.fetchall()
            result = pd.DataFrame(data, columns=["Code", "Name", "Name1", "CRUEI"]).to_dict("records")
            return Response({"Importer": result})
        except Exception as e:
            raise APIException(str(e))

class ImporterGet(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Code, Name, Name1, CRUEI FROM Importer WHERE status = 'Active' ORDER BY Code")
                data = cursor.fetchall()
            result = pd.DataFrame(data, columns=["Code", "Name", "Name1", "CRUEI"]).to_dict("records")
            return Response({"Importer": result})
        except Exception as e:
            raise APIException(str(e))
    
class ImporterUpdate(APIView):
    permission_classes = [AllowAny]
    def put(self, request):
        try:
            name = request.data.get('Name')
            name1 = request.data.get('Name1')
            cruei = request.data.get('CRUEI')
            code = request.data.get('Code')
            if not all([name, name1, cruei, code]):
                raise APIException("All fields (Name, Name1, CRUEI, Code) are required for update")
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Importer SET Name = %s, Name1 = %s, CRUEI = %s WHERE Code = %s AND status = 'Active'",
                    [name, name1, cruei, code]
                )
            return Response({"message": "Importer updated successfully"})
        except Exception as e:
            raise APIException(f"Error updating importer: {str(e)}")


class FreightForwarderGet(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Code, Name, Name1, CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Code")
                data = cursor.fetchall()
            result = pd.DataFrame(data, columns=["Code", "Name", "Name1", "CRUEI"]).to_dict("records")
            return Response({"fright": result})
        except Exception as e:
            raise APIException(str(e))

class FreightForwarderUpdate(APIView):
    permission_classes = [AllowAny]
    def put(self, request):
        try:
            name = request.data.get('Name')
            name1 = request.data.get('Name1')
            cruei = request.data.get('CRUEI')
            code = request.data.get('Code')
            if not all([name, name1, cruei, code]):
                raise APIException("All fields (Name, Name1, CRUEI, Code) are required for update")
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE FreightForwarder SET Name = %s, Name1 = %s, CRUEI = %s WHERE Code = %s AND status = 'Active'",
                    [name, name1, cruei, code]
                )
            return Response({"message": "FreightForwarder updated successfully"})
        except Exception as e:
            raise APIException(f"Error updating importer: {str(e)}")



