import json
import httpx,random,string
from bs4 import BeautifulSoup
from urllib.parse import urlencode

header={"authority":"www.walmart.ca",
    "method":"GET",
    "path":"/en/search?q=lego&facet=f_SellerType_en%3AWalmart%7C%7Cf_Availability_en%3AOnline%7C%7Cbrand%3ALEGO&catId=10011_6000205043132",
    "scheme":"https",
    "accept":"application/json",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-US,en;q=0.9,fr;q=0.8,ar;q=0.7",
    "Cache-Control":"no-cache",
    "Cookies":"wm_route_based_language=en-CA; WM_SEC.AUTH_TOKENMTAyOTYyMDE4kG6P2f38XH9l2YjDuQGxAOqJevWBWr40r0F9h3yrkFkulcaar6duVTPeb3cYIpvi%2Bqy7kN4kp%2Frf%2F8Ox2th1nSK%2FlQ15nfhU6LbkuT6x7mh4rC%2FsszkbJ2Qyi13uShDDj8OFN4dileb20bpDLeCIlSFd%2FHsc7bnSe4%2BTLU2zbj21p2%2F23VnrWO%2F5chgOZ1dmagmvEqD4HEXwAMIjAnPVfW3MlX5XKTmMOZYRfh4ePBHb%2FSoGFgAYL9DGZ8K45WCXJ0tmvH1FCaN9tZDh4SCrHUlO9lhKq9lXbxrORWo3byqlfBMCBLxnYkJ5m7AHHVOX0QWkXPtlb7lCZPADlGwPdl%2FjL1b%2BloPcY%2Fzd3tDE8BEjuM1P2CuxAWGbSkBUt7L9HzO9Q5cPXZw9vUtGzaZb%2B0r1eX9YGQ0laieVMoEr348%3D; auth=MTAyOTYyMDE4kG6P2f38XH9l2YjDuQGxAOqJevWBWr40r0F9h3yrkFkulcaar6duVTPeb3cYIpvi%2Bqy7kN4kp%2Frf%2F8Ox2th1nSK%2FlQ15nfhU6LbkuT6x7mh4rC%2FsszkbJ2Qyi13uShDDj8OFN4dileb20bpDLeCIlSFd%2FHsc7bnSe4%2BTLU2zbj21p2%2F23VnrWO%2F5chgOZ1dmagmvEqD4HEXwAMIjAnPVfW3MlX5XKTmMOZYRfh4ePBHb%2FSoGFgAYL9DGZ8K45WCXJ0tmvH1FCaN9tZDh4SCrHUlO9lhKq9lXbxrORWo3byqlfBMCBLxnYkJ5m7AHHVOX0QWkXPtlb7lCZPADlGwPdl%2FjL1b%2BloPcY%2Fzd3tDE8BEjuM1P2CuxAWGbSkBUt7L9HzO9Q5cPXZw9vUtGzaZb%2B0r1eX9YGQ0laieVMoEr348%3D; DYN_USER_ID=78ebeed0-534a-4517-8d7b-fc41bec7de1b; LT=1711037411574; ACID=78ebeed0-534a-4517-8d7b-fc41bec7de1b; locDataV3=eyJwaWNrdXBTdG9yZSI6eyJhZGRyZXNzTGluZU9uZSI6IjY3OTcgQmx2ZCBOZXdtYW4iLCJjaXR5IjoiTGFzYWxsZSIsInN0YXRlT3JQcm92aW5jZUNvZGUiOiJRQyIsImNvdW50cnlDb2RlIjoiQ0EiLCJwb3N0YWxDb2RlIjoiSDhOIDNFNCIsInN0b3JlSWQiOiIzMDQ2IiwiZGlzcGxheU5hbWUiOiJMQVNBTExFLCBRVUVCRUMiLCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6NDUuNDUyMDM3LCJsb25naXR1ZGUiOi03My42MTEyMDF9LCJhY2Nlc3NQb2ludElkIjoiMjljMWE4NWQtZmVjMC00YzVjLWIyMmMtNTFmZjA1YmZjZDU0IiwiZnVsZmlsbG1lbnRTdG9yZUlkIjoiMzA0NiIsInByaWNpbmdTdG9yZUlkIjoiMzA0NiIsImZ1bGZpbGxtZW50T3B0aW9uIjoiUElDS1VQIiwiZnVsZmlsbG1lbnRUeXBlIjoiSU5TVE9SRV9QSUNLVVAifSwic2hpcHBpbmciOnsicG9zdGFsQ29kZSI6Ikg4TiAzRTQiLCJjaXR5IjoiTGFzYWxsZSIsInN0YXRlT3JQcm92aW5jZUNvZGUiOiJRQyIsImNvdW50cnlDb2RlIjoiQ0EiLCJsYXRpdHVkZSI6NDUuNDUyMDM3LCJsb25naXR1ZGUiOi03My42MTEyMDEsImlzR2lmdEFkZHJlc3MiOmZhbHNlfSwiaW50ZW50IjoiUElDS1VQIiwiaXNFeHBsaWNpdEludGVudCI6ZmFsc2UsInZhbGlkYXRlS2V5IjoicHJvZDp2Mjo3OGViZWVkMC01MzRhLTQ1MTctOGQ3Yi1mYzQxYmVjN2RlMWIifQ%3D%3D; hasLocData=1; userAppVersion=main-1.81.0-5a803ad-0315T0054; vtc=WOiwLC-alRjQUoQ4o3yZ9A; walmart.nearestLatLng=""/45.4738,-73.5875/""; userSegment=40-percent; _astc=6fabb23d8605a3a3fc2096c3c152826c; localStoreInfo=eyJwb3N0YWxDb2RlIjoiSDhOM0U0IiwibG9jYWxTdG9yZUlkIjoiMzA0NiIsInNlbGVjdGVkU3RvcmVJZCI6IjMwNDYiLCJzZWxlY3RlZFN0b3JlTmFtZSI6IkxBU0FMTEUsIFFVRUJFQyIsImZ1bGZpbGxtZW50U3RvcmVJZCI6IjMwNDYiLCJmdWxmaWxsbWVudFR5cGUiOiJJTlNUT1JFX1BJQ0tVUCJ9Cg==; deliveryCatchment=3046; walmart.nearestPostalCode=H8N3E4; walmart.shippingPostalCode=H8N3E4; defaultNearestStoreId=3046; wmt.c=0; cartId=f32d32e3-b576-4a65-9aa6-aa75473838dc; uxcon=enforce=true&p13n=true&ads=true&createdAt=1711037411467&modifiedAt=1711039198896; ak_bmsc=B320C07A2D2DA3CC35785D39847A6BBE~000000000000000000000000000000~YAAQjn86FwidN3qOAQAAwDbHgBcYJ5IwLMRTfY6CQjTXkxmGThXmhnLCTMMBAG7PgVOWSZcNVSUrI5nrYw9ve0EGqXGO1/Ztjmf++K1cHcwl4n2D/jjiAUNHr+AzPLw7h1ooXEH7+Hyqh7uCOmK+2OtJLKFWrIJxLzDSX/BeMwailuuB4F/eIyLk1Qu6yyxdl05YRbWgMEktoIC67wBGgotcwB03FZGaef0TtqBXguRbL8VBb7eBygB9VaAzD8J0Ly/jP0fPLlsGix9Y82gglh+qWzFSV6kPYl/On2/r89pAmBcmRS9gw1b9qmVwHIDKdrZxZFAQNYL4AjoPYeRfu8QN2Egwv8pVJNFMmASYNnH6BRfuSlanFj2ZVxfEZwBlcn3FrceHINBzFw==; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-1124106680%7CMCIDTS%7C19810%7CMCMID%7C83701568589346262569222163537476957774%7CMCAID%7CNONE%7CMCOPTOUT-1711564722s%7CNONE%7CvVersion%7C5.2.0; pxcts=79b3a544-ec58-11ee-b86c-da27a82bfdc6; _pxvid=79b39536-ec58-11ee-b86c-414036c138b2; sizeID=bpje4eoeffhbgt0usi550tilhv; WM.USER_STATE=GUEST%7CGuest; type=GUEST%7CGuest; bstc=cSbfkQFgeR2mVcQWfQA2xY; xpa=4_row|8n9VQ|8w5K3|AkCnh|H9y_G|JOpAL|KxvHx|M4aON|Ux1PN|Vd_wf|gsmfi|hhuQW|mDA7E|sNTRO|xDVf0; exp-ck=4_row18n9VQ18w5K31AkCnh2JOpAL1KxvHx1M4aON1gsmfi1mDA7E1sNTRO1; ENV=ak-eus-t1-prod; xpm=1%2B1711560868%2BWOiwLC-alRjQUoQ4o3yZ9A~%2B0; dimensionData=1279; adblocked=true; seqnum=26; TS010110a1=0197384216d068c91a922171854ada972c05ab5940bff50c2fe2ca3ada66f9a086847a9303e9a3780082a11f5767e60998ea8ae6fa; TS01ea8d4c=0197384216d068c91a922171854ada972c05ab5940bff50c2fe2ca3ada66f9a086847a9303e9a3780082a11f5767e60998ea8ae6fa; TS0180da25=0197384216d068c91a922171854ada972c05ab5940bff50c2fe2ca3ada66f9a086847a9303e9a3780082a11f5767e60998ea8ae6fa; TSe62c5f0d027=085549fa9dab2000ba75120ac412e3495a22bccfd35075db933982caf9eeb0a7f3dae5c45893e51808beb634ba1130004a5f8ca4d60576e661aa17a93addb2a94e22c61a18815a891d0f6f234a544e035120f327de53fb1bb95e399bf8a39adc; bm_sv=2141DA8CAAC5721A16454475440FCEDE~YAAQPOg3F/jZHzmOAQAAOmEBgRfQK1hJGmGaRr7NGC+pCpMrq/LmqL0Mq66b50jLo5bq+D0nwk6FyhOFQeI9ySKkMGN8ogjQEfXvf2RfU/DLj7m7wL0GV1cGNtb/QbG1z7iDof39JqJfKeJvP60BSmPQ/eNc2y/Wc1FmsqYbxGxwKVqKU8XKtx7z0KCnckDHqojyiKryKL62vzdYViku9cWCl/RZFZznrSykDkVkqlF4Yo9CVZf4UUCC3R1JnkW2HA==~1",
    "downlink":"10", 
    "dpr":"1",
    "pramage":"no-cache",
    "Referer":"https://www.walmart.ca/en/search?q=lego",
    "sec-ch-ua":"\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"\"Windows\"",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "Synthetic-Request-For-Logging":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
}

try:
    #keyword = 'ipad'
    #payload = {'q': keyword, 'sort': 'best_seller', 'page': 1, 'affinityOverride': 'default'}
    #walmart_search_url = 'https://www.walmart.com/search?' + urlencode(payload)
    
    #walmart_search_url = 'https://www.walmart.ca/en/browse/toys/lego/10011_6000205043132?icid=landing%2Fcp_page_toys_shop_all_lego_18944_EU28ISZ2DN&facet=f_SellerType_en%3AWalmart%7C%7Cbrand%3ALEGO%7C%7Cf_Availability_en%3AOnline'
    #response = requests.get(walmart_search_url, headers=headers)
    walmart_search_url ='https://www.walmart.ca/en/search?q=lego&facet=f_SellerType_en%3AWalmart%7C%7Cf_Availability_en%3AOnline%7C%7Cbrand%3ALEGO&catId=10011_6000205043132'


    response = httpx.get(walmart_search_url, headers=header)
    if response.status_code == 200:
        html_response = response.text
        soup = BeautifulSoup(html_response, "html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag is not None:
            json_blob = json.loads(script_tag.get_text())
            product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
            with open('./data/WalmartCurrent.json', 'w') as outfile:
                json.dump(product_list, outfile)
                print('We found some! :)')

        else    : 
            print("Script tag not found")
            print(html_response)
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup.get_text())
            
except Exception as e:
    print('Error', e)





