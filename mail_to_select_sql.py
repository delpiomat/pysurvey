name_file = 'aziende_stageit.txt'

#id auto increment ma a noi serve per la seconda insert
id = 2
password=''
is_superuser='0'
username=''
first_name=''
last_name=''
email=''
is_staff='0'
is_active='1'
row=''

type = '1'
azienda_id = 'null'
survey_id = 'null'
questionario = '0'

query=''

#scrivo su file
out_file = open("test.txt","w")


# leggo file un file.
with open(name_file) as fp:
    for line in fp:
        row = (line.strip()).lower()
        email = str.split(row, ',')[1]
        questionario = str.split(row, ',')[0]
        azienda_id = questionario
        username = email
        first_name = email
        last_name = email
        id += 1
        #tolto: last_login,date_joined
        query = 'INSERT INTO auth_user(id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active)'+' VALUES ('+str(id)+','+password+','+is_superuser+','+username+','+first_name+','+last_name+','+email+','+is_staff+','+is_active+');'
        out_file.write(query)
        query = '\n'
        out_file.write(query)
        #tolto: activationCode, timeCode
        query = 'INSERT INTO createsurvey_account(user_ptr_id, type, azienda_id, survey_id) VALUES ('+str(id)+','+type+','+azienda_id+','+survey_id+');'
        out_file.write(query)
        query = '\n\n'
        out_file.write(query)

out_file.close()

