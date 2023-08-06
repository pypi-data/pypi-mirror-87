IP_ADD = "39.52.82.88"
import requests
r = requests.get("http://ipchecker.statistics.api.vpngate.net/api/ipcheck/?key=MVpfd3Jz&ip=" + str(IP_ADD))
print(int(r.content.decode("utf-8")))

r = requests.get("http://ip-api.com/json/"+IP_ADD+"?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
print(r.content.decode("utf-8"))

import IP2Proxy

db = IP2Proxy.IP2Proxy()
### open IP2Proxy BIN database for proxy lookup
db.open("/Users/ali/Downloads/sample.bin.px10 (1)/IP2PROXY-IP-PROXYTYPE-COUNTRY-REGION-CITY-ISP-DOMAIN-USAGETYPE-ASN-LASTSEEN-THREAT-RESIDENTIAL.BIN")
### get versioning information
print ('Module Version: ' + db.get_module_version())
print ('Package Version: ' + db.get_package_version())
print ('Database Version: ' + db.get_database_version())
### single function to get all proxy data returned in array
record = db.get_all(IP_ADD)
### close IP2Proxy BIN database
db.close()

if record['is_proxy'] > 0 and (record['proxy_type']!='RES' and record['country_short']!='PK' and record['usage_type']!='MOB'):
    print(IP_ADD,'Going to ban ip')
else:
    print("Not gonna ban")

print ('Is Proxy: ' + str(record['is_proxy']))
print ('Proxy Type: ' + record['proxy_type'])
print ('Country Code: ' + record['country_short'])
print ('Country Name: ' + record['country_long'])
print ('Region Name: ' + record['region'])
print ('City Name: ' + record['city'])
print ('ISP: ' + record['isp'])
print ('Domain: ' + record['domain'])
print ('Usage Type: ' + record['usage_type'])
print ('ASN: ' + record['asn'])
print ('AS Name: ' + record['as_name'])
print ('Last Seen: ' + record['last_seen'])



# individual proxy data check
# print ('Is Proxy: ' + str(db.is_proxy("128.199.69.218")))
# print ('Proxy Type: ' + db.get_proxy_type("128.199.69.218"))
# print ('Country Code: ' + db.get_country_short("128.199.69.218"))
# print ('Country Name: ' + db.get_country_long("128.199.69.218"))
# print ('Region Name: ' + db.get_region("128.199.69.218"))
# print ('City Name: ' + db.get_city("128.199.69.218"))
# print ('ISP: ' + db.get_isp("128.199.69.218"))
# print ('Domain: ' + db.get_domain("128.199.69.218"))
# print ('Usage Type: ' + db.get_usage_type("128.199.69.218"))
# print ('ASN: ' + db.get_asn("128.199.69.218"))
# print ('AS Name: ' + db.get_as_name("128.199.69.218"))
# print ('Last Seen: ' + db.get_last_seen("128.199.69.218"))
#print ('Threat: ' + db.get_threat("128.199.69.218"))


#print ('Threat: ' + record['threat'])


