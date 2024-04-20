from . import disks
from . import cpu

# from filesystem import requests
# # from filesystem.xmltodict import xmltodict
# from filesystem import xmltodict
# import subprocess
# import json

# ### Collect Serial Number
# def GET_MAC_SERIAL_NUMBER():
#     try:
#         systemprofile_reader = subprocess.Popen(['system_profiler', '-json', 'SPHardwareDataType'], stdout=subprocess.PIPE)
#         system_profile_data = json.loads(systemprofile_reader.stdout.read())
#         MAC_SERIAL = system_profile_data.get('SPHardwareDataType', {})[0].get('serial_number')
#         return MAC_SERIAL
#     except:
#         return "Information not available for this device"
# ### Collect Serial Number
    
# def GET_BRAND_NAME():
#     serial = GET_MAC_SERIAL_NUMBER()
#     serial_split = serial[-4:]
#     URL = f'https://support-sp.apple.com/sp/product?cc={serial_split}&lang=en_US'
#     response = requests.get(URL)
#     data = xmltodict.parse(response.content)
#     MyDict = {}

#     ### Collecting data from dictionary
#     MyDict['name'] = data['root']['name']
#     MyDict['configCode'] = data['root']['configCode']
#     MyDict['locale'] = data['root']['locale']
#     ### Collecting data from dictionary

#     return MyDict['configCode']