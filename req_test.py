import requests
_csrf_token='lDGJGyExnzM%2FvsxAWnxE2ds0%2F4ivT8r9SMp16ESbeGWlRdBBSlLGcFbb%2FSI0NHy%2F6X7Q3OMtubwGuwXDCMoUKQ%3D%3D'
URL = 'https://commons.ssu.ac.kr/CommonsCore2/v2/services/download/3274ab3cbc214fca92a1d0179c8d2ced'
cookie= {"sToken":"Vy3zFySFx5FASzTyGIDx5FDEMO1zCy1669867970zPy86400zAy34zEyWc7SlPNf5tNndSrSMEHeuSx2FoBP5XEUdDOYw4WVwOElWBSM4AnNZptucsJV0uPT5ezKyJJjKx2BXnQCRx2Fa8w7mpvlMx2F1x782Qx79aFMh9XO4k0VtCb90Ax3DzSSy00003314063zUURy658c938b3a8cad81zMyfDD4Kx79Dx79LMUx3Dz","PHPSESSID":"6hh85ekssarfrh35t3ea2gq86h"}

response = requests.get(URL,cookies=cookie)
print(response)
with open('metadata.pdf', 'wb') as f:
    f.write(response.content)
# print(response.raw)


# https://commons.ssu.ac.kr/contents15/ssu1000001/631821c66bdbb/contents/web_files/original.pdf