## BULK CERT GENERATOR

Generate Certificate From Excell data

How To Use :
    - use python3 (Recomended)
    - Install Package Using PIP `pip install Bulk-cert-generator`
    - import package `import Cert_gen` or `from Bulk_cert_generator import Cert_gen`

Simple Usage :
```python
import Cert_gen

Cert_gen.Cert_gen.generate('png','tem.jpg','Daftar.xlsx','sertif')
```
More Options :
```python
import Cert_gen

Cert_gen.Cert_gen.generate('png','tem.jpg','Daftar.xlsx','sertif','cert101',{'font_size':1.5,'font_color':(0,0,0),'x':15,'y':7})
```

# Parameter :

| Param       | Value           | type  |
| ------------- |:-------------:| -----:|
| format      | 'png' or 'pdf' (Extension Output) | String |
| template_path      | image certificate path      |   String |
| details_path | excell file path      |    String |
| output_path | output path      |    String |
|prefix_name | prefix name for file      |    String |
| style | styling     |  {'font_size':1.5,'font_color':(0,0,0),'x':15,'y':7}  |

# Excell File Example
!dont use column name
first column => Certificate Owner Name
Second Column => identity (phone number, certificate id etc)
| Alfian       | 087384           |
| ------------- |:-------------:|
| Andi     | 2322 
| Joni      | 2314     

Contact : mail@alfiankan.com

# Buy me a Coffe

https://saweria.co/encoding

