import requests
#res = requests.get('http://elasticsearch:9200/_search')
#print(res.status_code)

class Train:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    @classmethod
    def action(cls):
        return cls('Ivan','Petya')

obj = Train(name='name',age='age')
obj.action()
print(obj.name)



# curl -XGET "http://elasticsearch:9200/_search" -H 'Content-Type: application/json' -d'
# {
#   "query": {
#     "match_all": {}
#   }
# }'

engine.connect().execute(f"""create or replace view sources.spreadsheet_view as 
(
select "Модальности" as "Modality",
"Название ис-ния" as "Body_part",
extract('year' from "Дата исследования") as "Study_year",
"Дата исследования" as Study_date,
"Источник" as "Device_manufacture",
null as Device_model,
"Пол"as "Gender",
null as Age,
null as Race,
null as Etnicity,
null as Report,
null as Disease,
null as Region,
null as Additional_fields,
,dense_rank() over (order by "ID исследования")  as "StudyID_medframe"
,"ID исследования"::text as "StudyID_source"
,dense_rank() over (order by "DICOM идентификатор исследования") as "ScanID_medframe"
,"DICOM идентификатор исследования" as "ScanID_source"
,1 as "Source_id"
,dense_rank() over (order by "ID пациента")  as "PatientID_medframe"
"ID пациента"::text as "PatientID_source"
from sources."CT_Philips_Ingenuity"

union all

select null as "Modality",
"Body Part Examined" as "Body_part", 
null as "Study_year",
null as Study_date,
"Machine Model" as "Device_manufacture",
null as Device_model,
"Пол"as "Gender",
null as Age,
null as Race,
null as Etnicity,
null as Report,
null as Disease,
null as Region,
null as Additional_fields,
null as "StudyID_medframe"
,null as "StudyID_source"
,null as "ScanID_medframe"
,null as "ScanID_source"
,2 as "Source_id"
,null as "PatientID_medframe"
,null as "PatientID_source"
from sources.spreadsheet

union all

select "Modality" as "Modality", 
"BodyPartExamined" as "Body_part",
"Study Year" as "Study_year",
null as "Study_date",
"ManufacturerModelName" as "Device_manufacture",
null as Device_model,
"PatientSex"as "Gender"
null as Age,
null as Race,
null as Etnicity,
null as Report,
null as Disease,
null as Region,
"Constrast Enhanced (Y/N/NA)" as Additional_fields,
,dense_rank() over (order by "SeriesInstanceUID")  as "StudyID_medframe"
,"SeriesInstanceUID" "StudyID_source"
,null as "ScanID_source"
,null as "ScanID_source_our"
,3 as "Source_id"
,dense_rank() over (order by "PatientID")  as "PatientID_medframe"
,"PatientID" "PatientID_source"
from sources."demo_CT_any"

)

""")