
import json

d="""
{
    "app":"PDV LITE",
    "key_code":"electro_code_097*$FDEAGRERSATHBNJGFFFRKCXDTGVCXDHJFDC<VTYDGHGHVjghgldxv.fTkvHLGdM",
    "data":{
        "nome":"Mutxutxu",
        "localizacao":"Av. filipe Samuel Magaia N 1104",
        "cidade":"Lichinga",
        "nuit":1667287375365,
        "valor":30000,
        "validade":"17-05-2020",
        "pago":true,
        "tipo":"Restaurante",
        "contacto":877136613,
        "codigo_fatura":"0786",
        "logo":"/assets/logo.png",
        "email":"admin@gmail.com"
    },
    "admin":{
        "nome":"Diqui Joaquim",
        "apelido":"Namueto",
        "email":"admin@gmail.com",
        "contacto":877136613,
        "username":"admin",
        "password":"1234"
    }

}
"""
info= json.loads(d)


