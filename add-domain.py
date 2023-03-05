#!/usr/local/bin/python3.8

# from domain import domains
import time
#from reza import domains
import requests
import json
from db import domain_insert, sub_domain_insert , dns_record


domain_url = "https://napi.arvancloud.ir/cdn/4.0/domains/dns-service"
header = {"Content-Type": "application/json",
          "Authorization": "Apikey 667645-676545gh-gfhhghh-hg454",
          "Accept": "application/json, text/plain, */*"}


def domain_maker(a):
    body = {"domain": a}
    # print(body)
    return json.loads(requests.post(domain_url, headers=header, data=json.dumps(body)).text)


def record_maker(a, subdomain):
    record_url = "https://napi.arvancloud.ir/cdn/4.0/domains/{}/dns-records".format(
        a)
    body = {

        "type": "a",
        "name": subdomain,
        "value": [{"ip": "37.156.144.251"}],
        "ttl": 120,
        "cloud": True,
        "upstream_https": "default",
        "ip_filter_mode":

        {
            "count": "single",
            "order": "none",
            "geo_filter": "none"
        }

    }
    return json.loads(requests.post(record_url, headers=header, data=json.dumps(body)).text)


def update_dns (a):
    dns_url = "https://napi.arvancloud.ir/cdn/4.0/domains/{}/dns-service/ns-keys".format(a)
    body = {
        "ns_keys": ["ns1.ippanel.com","ns2.ippanel.com"]
    }
    return json.loads(requests.put(dns_url,headers=header , data=json.dumps(body)).text)




with open("/home/admin/web/ippanel.com/dns_domain/add-list","r") as domain_file:
    new_domain = domain_file.read().split()

    for j in new_domain:
        new_response = domain_maker(j)
        if 'data' in new_response:
            print("domain {} succesasfully inserted by id : ".format(j) ,  domain_insert(j, new_response["message"], new_response["data"]["id"]))
        for k in ["sms", "panel", "www", "@"]:

            record = record_maker(j, k)
            if 'data' in record:
                print("subdomain {} of domain {} succesasfully inserted by id : ".format(k,j) ,sub_domain_insert(j, k, record["data"]["id"]))
            else:
                print("subdomain {} of domain {} unsuccesasfull".format(k,j) , sub_domain_insert(j, k, record["message"]))
        else:
            print("domain {} unsuccesasfull".format(j) , domain_insert(j, new_response["message"], "failed"))
    
    
        # result = update_dns(j)

        # if 'data' in result:
	    #     print("dns record domain {} succesasfully updated ".format(j) , dns_record (j ,result["message"]))
        # else:
	    #     print("dns record domain {} unsuccesasfully updated ".format(j) , dns_record (j ,result["message"]))    
print("Done")
