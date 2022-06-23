#引用必要套件
import requests , json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

with open('GOVERNMENT_KEY.txt','r') as f:
 urlapi = f.read()
 
cred = credentials.Certificate("private_key.json") # 引用私密金鑰
firebase_admin.initialize_app(cred)                                     # 初始化firebase，注意不能重複初始化
db = firestore.client()                                                 # 初始化firestore
 
def get_weather_into_firebase():                                        #從url中拿取資料，並寫入到資料庫
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/{}?Authorization="+urlapi+"&format=JSON"  #擷取資料的url
    country_code = {"宜蘭縣":"F-D0047-001","桃園市":"F-D0047-005","新竹縣":"F-D0047-009","苗栗縣":"F-D0047-013","彰化縣":"F-D0047-017","南投縣":"F-D0047-021","雲林縣":"F-D0047-025","嘉義縣":"F-D0047-029","屏東縣":"F-D0047-033","臺東縣":"F-D0047-037","花蓮縣":"F-D0047-041","澎湖縣":"F-D0047-045","基隆市":"F-D0047-049","新竹市":"F-D0047-053","嘉義市":"F-D0047-057","臺北市":"F-D0047-061","高雄市":"F-D0047-065","新北市":"F-D0047-069","臺中市":"F-D0047-073","臺南市":"F-D0047-077","連江縣":"F-D0047-081","金門縣":"F-D0047-085"} #縣市的網頁代碼
    for code_number in country_code:
        get_data_url = url.format(country_code[code_number])            #把不同縣市的代碼輸入到url裡
        web_request = requests.get(get_data_url).json()                 #再用requests取出來，並轉換成json檔案的形式
        city_name = web_request["records"]["locations"][0]["locationsName"]
        doc_ref = db.collection("weather_data").document(city_name)     #在firebase中創建集合以及文件
        doc_ref.set({"縣市":city_name})                                 #以({"縣市":city_name})在文件裡新增欄位
        data = web_request["records"]["locations"][0]["location"]       #選取我們要抓取的data
        for obj in data:
            try:
                doc_ref.update({obj["locationName"]:obj["weatherElement"]}) #在裡面新增選取的資料
                print("新增",obj["locationName"],"成功")
            except:
                print("新增",obj["locationName"],"失敗")

get_weather_into_firebase()
 
 
 
 
 
 

