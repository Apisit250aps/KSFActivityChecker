from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.staticfiles import finders
import pandas as pd
import json
# Create your views here.


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def check(request):
    id = request.data['id']
    status = 200
    file = finders.find(
        'data/A__07KSFCEDATA2566-ผลกิจกรรมสมาชิก-ชมรมฅนสร้างฝัน-ประจำปีการศึกษา-2566.xlsx')
    ExcelFile = pd.ExcelFile(file)
    data = pd.read_excel(
        ExcelFile, sheet_name=ExcelFile.sheet_names[1]).fillna(0)
    data = data.loc[(data['รหัสนักศึกษา'] == int(id))]
    serialize = data.to_json(force_ascii=False, orient='records')
    information = json.loads(serialize)
    
    if len(information) != 0:
        status = 200
        information= information[0]
    else :
        status = 204
        information
    return Response(
        information,
        status=status
    )
