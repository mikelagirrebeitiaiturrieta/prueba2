from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from main import main
import sqlite3 as sql
import os
import time
import json
app = Flask(__name__)
# config = json.load(open('config.json','rb'))
# app.config['UPLOAD_FOLDER'] = config['upload_folder']

access=False
mueble=''
electrodomestico = ''
user_message=''
msg_upload_send = False
msg_run = False
msg_download = False

@app.route('/', methods=['POST','GET'])
def login():
   global access, user_message
   print(app.root_path)
   if request.method=='POST':
       try:
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from usuarios")
            rows_reservas = cur.fetchall();
            contador = [row for row in rows_reservas]
            username_password = {}
            for row in rows_reservas:
                username_password[row['username']] = row['password']
            con.close()
            if len(contador)==0:
                msg='No hay usuarios registrados'
                return render_template("login.html",msg=msg)
            # elif len(contador)==1:
            #     msg='Hay 1 usuario registrado. Inicie sesión con esa cuenta, o puede crear otro usuario.'
            #     return render_template("login.html",msg=msg)
            else:
                try:
                    if username_password[request.form['user']] == request.form['key']:
                        access=True
                        return redirect(url_for('principal'))
                    else:
                        msg = 'El usuario introducido es correcto pero la contraseña no. Por favor, inténtelo de nuevo!'
                        return render_template('login.html', msg=msg)  
                except:
                    msg = 'El usuario introducido no existe. Por favor, inténtelo de nuevo!'
                    return render_template('login.html', msg=msg)  
       except:
            try:
                 if (request.form['boton'] == 'Enviar'):
                    return render_template('login.html')
            except:
                return render_template('login.html')
   else:
        try:
           if user_message=='user_created':
                msg = 'Los dos usuarios que se pueden crear ya han sido creados. Por favor, inicie sesión.'
                return render_template('login.html', msg=msg)
           else:
                return render_template('login.html')
        except:
            return render_template('login.html')
         
       

@app.route('/principal', methods=['POST','GET'])
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
        


# @app.route('/uploads/<name>', methods=['GET', 'POST'])
# def download_file(name):
#     print(os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], name)))
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)

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

    
# @app.route('/muebles', methods=['POST','GET'])
# def muebles():
#     global access, mueble, msg_run, msg_upload_send, msg_download
#     if request.method=='POST':
#         try:
#             mueble = request.form['muebles']
#             if mueble in ["Acceder", "Optimización Muebles"]:
#                 mueble=''
#                 return render_template('muebles.html',msg_upload=msg_upload_send, msg_run=msg_run, msg_download=msg_download)
#         except:
#             try:
#                 try:
#                     if request.form['filename']=='error':
#                         return redirect(url_for('muebles'))
#                 except:
#                     if request.files.get("filename"):
#                         file = request.files.get("filename")
#                         file.filename = 'muebles_routes.xls'
#                         if os.path.exists(app.config['UPLOAD_FOLDER']):
#                             files = os.listdir(app.config['UPLOAD_FOLDER'])
#                             [os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file)) for file in files if 'muebles_routes.xls' in file]
#                             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#                         else:
#                             os.makedirs(app.config['UPLOAD_FOLDER'])
#                             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#                         access=True
#                         return redirect(url_for('muebles'))
#             except:
#                 pass
#             try:
#                 if (request.form['run']=='error'):
#                     return redirect(url_for('muebles'))
#                 elif (request.form['run']==''):
#                     list_dir = os.listdir(app.config["UPLOAD_FOLDER"])
#                     last_file = [file for file in list_dir if 'muebles_routes.xls' in file][-1]
#                     # file = os.listdir(app.config['UPLOAD_FOLDER'])
#                     # [os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file)) for file in files if 'm' in file]
#                     # main(path=os.path.join(app.config['UPLOAD_FOLDER'], file), num_vehicles=1)
#                     config = json.load(open('config.json','rb'))
#                     # print(config)
#                     # main(config=config, file=last_file, type='muebles')
#                     access=True
#                     time.sleep(1)
#                     return render_template('muebles.html')
#             except:
#                 pass
#             try:
#                 if (request.form['download'] == 'error'):
#                     return redirect(url_for('muebles'))
#                 elif (request.form['download'] == 'download'):
#                     list_dir = os.listdir(app.config["UPLOAD_FOLDER"])
#                     files = [file for file in list_dir if ('muebles' in file)&('ordenado' in file)]
#                     for f in files:
#                         access=True
#                         return redirect(url_for("download_file", name=f))
#                     # return render_template('muebles.html')
#             except:
#                 pass
#             try:
#                 if (request.form['optimized'] == ''):
#                     access=True
#                     return render_template('muebles.html')
#             except:
#                 msg_upload_send = False
#                 msg_run = False
#                 msg_download = False
#                 return render_template('muebles.html', msg_upload=msg_upload_send, msg_run=msg_run)
#     else:
#         if access==True:
#             access=False
#             msg_upload_send = False
#             msg_run = False
#             msg_download = False
#             return render_template('muebles.html',msg_upload=msg_upload_send, msg_run=msg_run)
#         else:
#             return redirect(url_for('principal'))

 
    

# @app.route('/electrodomesticos', methods=['POST','GET'])
# def electrodomesticos():
#     global access, electrodomestico, msg_run, msg_upload_send, msg_download
#     if request.method=='POST':
#         try:
#             electrodomestico = request.form['electrodomesticos']
#             if electrodomestico in ["Acceder", "Optimización Electrodomésticos"]:
#                 electrodomestico=''
#                 return render_template('electrodomesticos.html', msg_upload=msg_upload_send, msg_run=msg_run, msg_download=msg_download)
#         except:
#             try:
#                 try:
#                     if request.form['filename']=='error':
#                         return redirect(url_for('electrodomesticos'))
#                 except:
#                     if request.files.get("filename"):
#                         file = request.files.get("filename")
#                         file.filename = 'electrodomesticos_routes.xls'
#                         if os.path.exists(app.config['UPLOAD_FOLDER']):
#                             files = os.listdir(app.config['UPLOAD_FOLDER'])
#                             [os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file)) for file in files if 'electrodomesticos_routes.xls' in file]
#                             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#                         else:
#                             os.makedirs(app.config['UPLOAD_FOLDER'])
#                             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#                         access=True
#                         return redirect(url_for('electrodomesticos'))
#             except:
#                 pass
#             try:
#                 if (request.form['run']=='error'):
#                     return redirect(url_for('electrodomesticos'))
#                 elif (request.form['run']==''):
#                     list_dir = os.listdir(app.config["UPLOAD_FOLDER"])
#                     last_file = [file for file in list_dir if 'electrodomesticos_routes.xls' in file][-1]
#                     # file = os.listdir(app.config['UPLOAD_FOLDER'])
#                     # [os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file)) for file in files if 'm' in file]
#                     # main(path=os.path.join(app.config['UPLOAD_FOLDER'], file), num_vehicles=1)
#                     config = json.load(open('config.json','rb'))
#                     # print(config)
#                     # main(config=config, file=last_file, type='electrodomesticos')
#                     access=True
#                     time.sleep(1)
#                     return render_template('electrodomesticos.html')
#             except:
#                 pass
#             try:
#                 if (request.form['download'] == 'error'):
#                     return redirect(url_for('electrodomesticos'))
#                 elif (request.form['download'] == 'download'):
#                     list_dir = os.listdir(app.config["UPLOAD_FOLDER"])
#                     files = [file for file in list_dir if ('electrodomesticos' in file)&('ordenado' in file)]
#                     for f in files:
#                         access=True
#                         return redirect(url_for("download_file", name=f))
#             except:
#                 pass
#             try:
#                 if (request.form['optimized'] == ''):
#                     access=True
#                     return render_template('electrodomesticos.html')
#             except:
#                 msg_upload_send = False
#                 msg_run = False
#                 msg_download = False
#                 return render_template('electrodomesticos.html', msg_upload=msg_upload_send, msg_run=msg_run, msg_download=msg_download)
#     else:
#         if access==True:
#             access=False
#             msg_upload_send = False
#             msg_run = False
#             msg_download = False
#             return render_template('electrodomesticos.html',msg_upload=msg_upload_send, msg_run=msg_run, msg_download=msg_download)
#         else:
#             return redirect(url_for('principal'))


# @app.route('/muebles_map', methods=['POST','GET'])
# def muebles_map():
#     global access
#     if request.method=='GET':
#         if access==True:
#             access=False
#             return render_template('muebles_map.html')
#         else:
#             return redirect(url_for('muebles'))

# @app.route('/electrodomesticos_map', methods=['POST','GET'])
# def electrodomesticos_map():
#     global access
#     if request.method=='GET':
#         if access==True:
#             access=False
#             return render_template('electrodomesticos_map.html')
#         else:
#             return redirect(url_for('electrodomesticos'))


if __name__ == '__main__':
   app.run()
   