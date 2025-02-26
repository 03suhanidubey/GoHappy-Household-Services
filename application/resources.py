from flask_restful import Api, reqparse, Resource
from .models import *

api = Api()
parser=reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('professional_email')
parser.add_argument('fullname')
parser.add_argument('pincode')
parser.add_argument('experience')
parser.add_argument('rating')

class getprofessionalsbyservicename(Resource):
    def get(self, service_name):
        profes=Professionals.query.filter(Professionals.service==service_name)
        profeslist=[]
        for p in profes:
            p1 = {}
            p1['id'] = p.id
            p1['professional_email'] = p.emailid
            p1['fullname'] = p.fullname
            p1['pincode'] = p.pincode
            p1['experience']=p.experience
            p1['rating'] = p.avg_rating
            profeslist.append(p1)
        return profeslist
    
api.add_resource(getprofessionalsbyservicename, '/api/professionals_byservice/<service_name>')