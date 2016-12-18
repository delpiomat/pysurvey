name_file = 'mail_azz'

#id auto increment ma a noi serve per la seconda insert
id = 2
password='"pbkdf2_sha256$30000$ZxxNnT1er1h2$k7CsvSl2/AGyIibyQ9bgYqyuUAqPj7i/xwvV9XHwXS8="' #stageit
is_superuser='0'
username=''
first_name=''
last_name=''
email=''
is_staff='0'
is_active='1'
row=''
date_joined='"2016-08-17 12:31:31.757389"'

type = '1'
azienda_id = 'null'
survey_id = 'null'
questionario = '0'
activationCode = '"12345"'
timeCode = '"2016-10-22 18:21:29.519471"'


query=''

#scrivo su file
out_file = open("test.txt","w")


# leggo file un file.
with open(name_file) as fp:
    for line in fp:
        row = (line.strip()).lower()
        email = '"'+str.split(row, ',')[1]+'"'
        questionario = str.split(row, ',')[0]
        azienda_id = questionario
        username = email
        first_name = '"vuoto"'
        last_name = '"vuoto"'
        id += 1
        #tolto: last_login,date_joined
        query = 'INSERT INTO auth_user(id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)'+' VALUES ('+str(id)+','+password+','+is_superuser+','+username+','+first_name+','+last_name+','+email+','+is_staff+','+is_active+','+date_joined+');'
        out_file.write(query)
        query = '\n'
        out_file.write(query)
        #tolto: activationCode, timeCode
        query = 'INSERT INTO createSurvey_account(user_ptr_id, type, azienda_id, survey_id,activationCode,timeCode) VALUES ('+str(id)+','+type+','+azienda_id+','+survey_id+','+activationCode+','+timeCode+');'
        out_file.write(query)
        query = '\n\n'
        out_file.write(query)

out_file.close()

