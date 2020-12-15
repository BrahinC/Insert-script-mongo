import json
from pymongo import MongoClient
import os 
import pymongo



def cargar_datos(ruta):
    updateString=""
    client=MongoClient('localhost',27017)
    db= client.leaflet_map_2
    collection=db.layercollection
    countDevices=0
    countError=0
    countupdate=0
    ListErrorIp=[]
         

    with open(ruta) as contenido:
        resultado=json.load(contenido)

        for host in  resultado:
      
            countDevices=countDevices+1
            devicesInser=collection.find_one_and_update({"features.properties.Ne_IP":host["ip-vieja"]}, {"$set":{"features.$.properties.Ne_IP":host["ip-nueva"]}} )
         
            
            if(devicesInser!=None):
                collection.update_one({"features.properties.NE_IP_Address_Source":host["ip-vieja"]}, {"$set":{"features.$[env].properties.NE_IP_Address_Source":host["ip-nueva"]}}, array_filters= [{ "env.properties.NE_IP_Address_Source": host["ip-vieja"] }])

                collection.update_one({"features.properties.NE_IP_Address_Sink":host["ip-vieja"]}, {"$set":{"features.$[env].properties.NE_IP_Address_Sink":host["ip-nueva"]}},array_filters= [{ "env.properties.NE_IP_Address_Sink": host["ip-vieja"] }])
                update=True
                updateString=updateString+" * "
                countupdate=countupdate+1

            else:
                updateString=updateString+" - "
                update=False
                countError=countError+1 
                ListErrorIp.append(host)

            os.system("cls")
            print (updateString)
            

    print("Total: "+str(countDevices)  +" errores: "+str(countError)+" update: "+str(countupdate))
    print ("ip erros :"+str(ListErrorIp))

    return update
               
        
       
    

    
    

if __name__=='__main__':
    ruta='json/ip.json'
    print("cargadatos host")
    print (cargar_datos(ruta))
 
  