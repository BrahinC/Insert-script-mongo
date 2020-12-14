import json
from pymongo import MongoClient

import pymongo



def cargar_datos(ruta):
  
    client=MongoClient('localhost',27017)
    db= client.leaflet_map_2
    collection=db.layercollection
    
         

    with open(ruta) as contenido:
        resultado=json.load(contenido)

        for host in  resultado:
      
    
            devicesInser=collection.find_one_and_update({"features.properties.Ne_IP":host["ip-vieja"]}, {"$set":{"features.$.properties.Ne_IP":host["ip-nueva"]}} )
         
            
            if(devicesInser!=None):
                collection.update_one({"features.properties.NE_IP_Address_Source":host["ip-vieja"]}, {"$set":{"features.$[env].properties.NE_IP_Address_Source":host["ip-nueva"]}}, array_filters= [{ "env.properties.NE_IP_Address_Source": host["ip-vieja"] }])

                collection.update_one({"features.properties.NE_IP_Address_Sink":host["ip-vieja"]}, {"$set":{"features.$[env].properties.NE_IP_Address_Sink":host["ip-nueva"]}},array_filters= [{ "env.properties.NE_IP_Address_Sink": host["ip-vieja"] }])
                print("--------------divices documnet insert---------")
                print ("la ip: " + host["ip-vieja"]+"cambio por la ip: " +host["ip-nueva"])
            
            else:
                print("--------------divices documnet insert---------")
                print( "no se puedo cambiar la ip: "+ host["ip-vieja"] +" por la ip: " +host["ip-nueva"] )
                print()
                print("verifique si ya esta en la base de datos")
        
        
       
    

    
    

if __name__=='__main__':
    ruta='json/ip.json'
    print("cargadatos host")
    cargar_datos(ruta)
  