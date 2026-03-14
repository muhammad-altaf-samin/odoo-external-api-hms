"""
Odoo External API Script
Hospital Management System Example
Covers all CRUD operations (Create, Read, Update, Delete)
"""

import xmlrpc.client

# Configuration
url = "http://localhost:8069"
db = "hospital_db"
username = "admin"
password = "admin"


# Step 1: Connect to Common (Authentication)
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
if uid:
    print(f"Authenticated successfully. UID: {uid}")
else:
    raise Exception("Authentication Failed!")


# Step 2: Connect to Object (Model Access)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")


# Step 3: CREATE Operation
patient_id = models.execute_kw(
    db, uid, password,
    'hospital.patient',       # model
    'create',                 # method
    [{
        'name': 'Ali Khan',
        'age': 30,
        'gender': 'male'
    }]
)
print(f"Patient Created. ID: {patient_id}")


# Step 4: READ Operation
patients = models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'search_read',
    [[('id','=',patient_id)]],  # domain filter
    {'fields':['name','age','gender']}  # return only required fields
)
print("Patient Data:", patients)


# Step 5: UPDATE Operation
models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'write',
    [[patient_id], {'age': 35}]
)
print("Patient Updated Successfully.")


# Step 6: DELETE Operation
models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'unlink',
    [[patient_id]]
)
print("Patient Deleted Successfully.")


# Step 7: SEARCH with Domain & Pagination
patients_list = models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'search_read',
    [[('age','>=',18)]],  # domain
    {'fields':['name','age'], 'limit': 5, 'offset':0}
)
print("Patients List (First 5 adults):", patients_list)


# Step 8: READ_GROUP (Reporting)
age_group_report = models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'read_group',
    [[('age','>=',18)]],
    {'fields':['age'], 'groupby':['gender']}
)
print("Age Group Report by Gender:", age_group_report)


# Step 9: Bulk Create
bulk_patients = models.execute_kw(
    db, uid, password,
    'hospital.patient',
    'create',
    [[
        {'name':'Ahmad', 'age':28, 'gender':'male'},
        {'name':'Sara', 'age':25, 'gender':'female'},
        {'name':'Hina', 'age':22, 'gender':'female'}
    ]]
)
print("Bulk Patients Created:", bulk_patients)