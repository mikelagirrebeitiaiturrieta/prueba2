from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import json
app = Flask(__name__)
config = json.load(open('config.json','rb'))
app.config['UPLOAD_FOLDER'] = config['upload_folder']

access=True
mueble=''
electrodomestico = ''
user_message=''
msg_upload_send = False
msg_run = False
msg_download = False

# @app.route('/', methods=['POST','GET'])
# def login():
#    global access, user_message
#    if request.method=='POST':
#        try:
#             con = sql.connect("database.db")
#             con.row_factory = sql.Row
#             cur = con.cursor()
#             cur.execute("select * from usuarios")
#             rows_reservas = cur.fetchall();
#             contador = [row for row in rows_reservas]
#             username_password = {}
#             for row in rows_reservas:
#                 username_password[row['username']] = row['password']
#             con.close()
#             if len(contador)==0:
#                 msg='No hay usuarios registrados'
#                 return render_template("login.html",msg=msg)
#             # elif len(contador)==1:
#             #     msg='Hay 1 usuario registrado. Inicie sesión con esa cuenta, o puede crear otro usuario.'
#             #     return render_template("login.html",msg=msg)
#             else:
#                 try:
#                     if username_password[request.form['user']] == request.form['key']:
#                         access=True
#                         return redirect(url_for('principal'))
#                     else:
#                         msg = 'El usuario introducido es correcto pero la contraseña no. Por favor, inténtelo de nuevo!'
#                         return render_template('login.html', msg=msg)  
#                 except:
#                     msg = 'El usuario introducido no existe. Por favor, inténtelo de nuevo!'
#                     return render_template('login.html', msg=msg)  
#        except:
#             try:
#                  if (request.form['boton'] == 'Enviar'):
#                     return render_template('login.html')
#             except:
#                 return render_template('login.html')
#    else:
#         try:
#            if user_message=='user_created':
#                 msg = 'Los dos usuarios que se pueden crear ya han sido creados. Por favor, inicie sesión.'
#                 return render_template('login.html', msg=msg)
#            else:
#                 return render_template('login.html')
#         except:
#             return render_template('login.html')
         
       

@app.route('/', methods=['POST','GET'])
def principal():
    global access
    if request.method=='POST':
        return render_template('principal.html')
    else:
        if access==True:
            access=False
            return render_template('principal.html')
        else:
            return redirect(url_for('login'))
        



@app.route('/register', methods=['POST','GET'])
def register():
    global user_message
    if request.method=='POST':
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from usuarios")
        rows_reservas = cur.fetchall();
        contador = [row for row in rows_reservas]
        con.close()
        if len(contador)<2:
            try:
                if request.form['login_action']=='Regístrate':
                    return render_template('register.html')
            except:
                try:
                    username=request.form['username']
                    password=request.form['password']
                    confirm_password=request.form['confirm_password']
                    email=request.form['email']
                    msg1='-Username: Tipo texto.'
                    msg2='-Password: Tipo texto.'
                    msg3='-Confirm password: Tipo texto. Tiene que coincidir con el campo password.'
                    msg4='-Email: Tipo texto. Ejemplo:servidor@gmail.com.'

                    con = sql.connect("database.db")
                    con.row_factory = sql.Row
                    cur = con.cursor()
                    cur.execute("select * from usuarios")
                    rows_reservas = cur.fetchall();
                    con.close()
                    if rows_reservas!=[]:
                        username_password = {}
                        for row in rows_reservas:
                            username_password[row['username']] = row['password']
                        
                        if username in list(username_password.keys()):
                            msg='El usuario introducido ya existe. Por favor, introduzca otro usuario.'
                            return render_template('register.html',msg=msg)
                        elif password in list(username_password.values()):
                            msg='La contraseña introducida ya ha sido utilizada por otra persona. Por favor, introduzca otra contraseña.'
                            return render_template('register.html',msg=msg)
                        else:
                            pass
                    if len(password)!=8:
                        msg='La contraseña debe tener 8 caracteres. Por favor, inténtelo de nuevo.'
                        return render_template('register.html',msg=msg)
                    if password!=confirm_password:
                        msg='Las contraseñas no coinciden. Por favor, inténtelo de nuevo.'
                        return render_template('register.html',msg=msg)
                    if ('@' in email):
                        con = sql.connect('database.db')
                        cur = con.cursor()
                        try:
                            print('here')
                            result=request.form
                            cur.execute("INSERT INTO usuarios (username, password, confirm_password, email) VALUES (?,?,?,?)",(username, password, confirm_password, email))
                            con.commit()
                            msg = 'Los datos se han introducido con éxito!'
                            return render_template('login.html', msg=msg)
                        except:
                            con.rollback()
                            msg = 'Los datos no se han introducido correctamente. Cada campo introducido debe tener las siguientes características:'
                            return render_template('register.html', msg=msg,msg1=msg1,msg2=msg2,msg3=msg3,msg4=msg4)
                        finally:
                            con.close()
                    else:
                        msg = 'Los datos no se han introducido correctamente. Cada campo introducido deb tener las siguientes características:'
                        return render_template('register.html', msg=msg,msg1=msg1,msg2=msg2,msg3=msg3,msg4=msg4)
                except:
                    try:
                        if request.form['login_action']=='Register':
                            return render_template('register.html')
                    except:
                        return render_template('login.html')

        else:
            try:
                if request.form['login_action']=='Regístrate':	
                    user_message = 'user_created'
                    return redirect(url_for('login')) 
            except:
                return render_template('login.html')

    


if __name__ == '__main__':
   app.run()
   