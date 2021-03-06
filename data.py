#database
from os import access
from pymongo import MongoClient
from face_recognition import load_image_file,face_encodings
import numpy as np
class datab(object):
    def __init__(self):
        self.client = MongoClient('localhost',27017,username="root",password="Adriano28")
        self.db=self.client['face_db']
        self.faces = self.db.face
    def __del__(self):
        self.client.close()

    def register(self,file_stream,_id,name,last,access):
        img = load_image_file(file_stream)
        encoding = face_encodings(img)[0]
        access = int(access)
        if len(encoding) > 0 and len(encoding) < 2:
            encoding = encoding.tolist()
            print(encoding)
            self.faces.insert_many([
                {"_id": _id, "name":name,"last":last,"access":access,"encoding":encoding}
                ])
    def delete(self,_id):
        _id = int(_id)
        self.faces.delete_one({'_id':_id})
    def getlist(self):
        all_docs=list(self.faces.find({}))
        _id,name,last,access_int=[doc["_id"] for doc in all_docs],[doc["name"] for doc in all_docs],[doc["last"] for doc in all_docs],[doc["access"] for doc in all_docs]
        access = []
        for i in access_int:
            t_access = "Invited"
            if i == 1:
                t_access = "Total"
            elif i == 2:
                t_access = "Welcome"
            else:
                t_access = "Not welcome"
            access.append(t_access)
        return (_id,name,last,access)
    def getnewid(self):
        all_docs = list(self.faces.find({}))
        ids = [doc["_id"] for doc in all_docs]
        ids.append(0)
        newid = max(ids)+1
        return newid
    def getencodings(self):
        all_docs = list(self.faces.find({}))
        names,lasts,encodings = [doc["name"] for doc in all_docs],[doc["last"] for doc in all_docs],[doc["encoding"] for doc in all_docs]
        Lnames = []
        for i in range(0,len(names)):
            Lname= names[0]+" "+lasts[0][0]
            Lnames.append(Lname)
        encodings = np.array(encodings)
        return(Lnames,encodings)




