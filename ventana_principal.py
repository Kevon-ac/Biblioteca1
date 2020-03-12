from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import custom_qr
from ttkthemes import ThemedTk



#probando github

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="bibliotecaparra"
)

mycursor = mydb.cursor()

#abrir ventana en el centro
def centrar_ventana(ventana):
    windowWidth = ventana.winfo_reqwidth()
    windowHeight = ventana.winfo_reqheight()
    positionRight = int(ventana.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(ventana.winfo_screenheight()/3 - windowHeight/3)
    ventana.geometry("+{}+{}".format(positionRight, positionDown))

root = ThemedTk(theme="breeze")
root.title("Biblioteca Parra")
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='book.png'))
root.geometry("305x200")
root.config(bg="white")
centrar_ventana(root)




#Ventana para registrar usuario
def open_registro():

    def popup_usuario_agregado():
        messagebox.showinfo("Listo", "Usuario agregado con exito!")

    def agregar_usuario():
        #conectandome a la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="bibliotecaparra"
        )

        mycursor = mydb.cursor()

        sql_command = "INSERT INTO usuarios (Nombre, Apellido, FechaNacimiento) VALUES (%s, %s, %s)"
        values = (tb_primer_nombre.get(), tb_apellido.get(), tb_fechaNacimiento.get())
        mycursor.execute(sql_command, values)

        mydb.commit()
        popup_usuario_agregado()
        registro.destroy()

    registro = Toplevel()
    registro.title("Registrar Alumno")
    registro.tk.call('wm', 'iconphoto', registro._w, PhotoImage(file='book.png'))
    registro.geometry("350x250+600+300")
    #centrar_ventana(registro)

    #Crear etiqueta titulo
    title_label = Label(registro, text = "Registrar Alumno", font=("Helvetica"))
    title_label.grid(row = 0, column = 0, columnspan = 2, pady = '10')

    #Crear formulario
    lbl_primer_nombre = Label(registro, text="Nombre").grid(row=1, column=0, sticky=W, padx=10)
    lbl_apellido = Label(registro, text="Apellido").grid(row=2, column=0, sticky=W, padx=10)
    lbl_fechaNacimiento = Label(registro, text="Fecha de Nacimiento").grid(row=3, column=0, sticky=W, padx=10)

    #Crear Cajas de entrada
    tb_primer_nombre = ttk.Entry(registro)
    tb_primer_nombre.grid(row=1, column=1, pady=5)

    tb_apellido = ttk.Entry(registro)
    tb_apellido.grid(row=2, column=1, pady=5)

    tb_fechaNacimiento = ttk.Entry(registro)
    tb_fechaNacimiento.grid(row=3,column=1, pady=5)

    #Crear Botones
    btn_agregar_usuario = ttk.Button(registro, text="Agregar Usuario", command=agregar_usuario)
    btn_agregar_usuario.grid(row=4, column=1, padx=10, pady=10)

#Ventana para hacer prestamo
def prestamo():
    def popup_prestamo(query):
        messagebox.showinfo("Listo", query)


    def buscar_usuario():
        #conectandome a la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="bibliotecaparra"
        )

        mycursor = mydb.cursor()

        #Buscar id del usuario
        sql_command = "select idUsuario from usuarios where Nombre = %s and Apellido = %s"
        values = (tb_primer_nombre.get(), tb_apellido.get())
        mycursor.execute(sql_command, values)
        result = mycursor.fetchall()
        for row in result:
            idUsuario = row[0]
        
        #abrir camara en custom_qr y obtener id del libro
        text = custom_qr.qr_id()
        idLibro = int(text)
        try: 
            print("el id del usuario es:", idUsuario, "\nel id del libro es:", idLibro)
        except UnboundLocalError:
            messagebox.showerror("Error", "Usuario no existe en la base de datos.")
            prestamo.destroy()

        #Crear recibo del prestamo
        sql_command = """Insert into prestamos(idLibro, idUsuario, FechaPedido, FechaEntrega, Estado) 
        values (%s, %s, curdate(), date_add(curdate(), interval 5 day), 'pendiente')"""
        values = (idLibro, idUsuario)
        mycursor.execute(sql_command, values)

        mydb.commit()

        sql_command = """SELECT Nombre, Apellido, Titulo, FechaPedido, FechaEntrega, prestamos.Estado FROM prestamos 
	                    JOIN usuarios ON prestamos.idUsuario = usuarios.idUsuario
                        JOIN libros ON prestamos.idLibro = libros.idLibro 
                        WHERE prestamos.idLibro = %s AND prestamos.idUsuario = %s"""
        mycursor.execute(sql_command, values)
        print(mycursor.fetchone())
        messagebox.showinfo("Listo", mycursor.fetchone())

        prestamo.destroy()

    prestamo = Toplevel()
    prestamo.title("Prestar libro")
    prestamo.tk.call('wm', 'iconphoto', prestamo._w, PhotoImage(file='book.png'))
    prestamo.geometry("300x200+600+300")

    #Crear etiqueta titulo
    title_label = ttk.Label(prestamo, text = "Favor de ingresar \nel nombre y apellido del alumno", font=("Helvetica"))
    title_label.grid(row = 0, column = 0, columnspan = 2, pady = 10 , padx = 30)

    #formulario
    lbl_primer_nombre = Label(prestamo, text="Nombre").grid(row=1, column=0, sticky=W, padx=10)
    lbl_apellido = Label(prestamo, text="Apellido").grid(row=2, column=0, sticky=W, padx=10)

    tb_primer_nombre = ttk.Entry(prestamo)
    tb_primer_nombre.grid(row=1, column=1, pady=5)

    tb_apellido = ttk.Entry(prestamo)
    tb_apellido.grid(row=2, column=1, pady=5)

    btn_agregar_usuario = ttk.Button(prestamo, text="Aceptar", command=buscar_usuario)
    btn_agregar_usuario.grid(row=4, column=1, padx=10, pady=10)

def devolver():
    #conectandome a la base de datos
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="bibliotecaparra"
    )

    mycursor = mydb.cursor()
    
    #abrir webcam y obtener id del libro con QR
    text = custom_qr.qr_id()
    idLibro = int(text)

    #Actualizar la tabla
    sql_command = """UPDATE prestamos 
    SET estado = 'finalizado'
    WHERE idLibro = %s"""
    mycursor.execute(sql_command % idLibro)

    mydb.commit()

    messagebox.showinfo("Listo", "Prestamo finalizado")
    


#Etiqueta "Bienvenido"
var = StringVar()
welcome = Label(root, textvariable=var, relief = FLAT, bg="white")
var.set("Bienvenido")
welcome.grid(row=0, column=0, padx=10, pady=10)

bottom_frame = Frame(root, width=650, height=400, bg="white")
bottom_frame.grid(row=1, column=0, padx=10, pady=5)

prestamo_btn = ttk.Button(bottom_frame, text = "Prestar", command=prestamo)
prestamo_btn.grid(row=1, column=0, padx=10, pady=10, ipadx=15)

devolucion_btn = ttk.Button(bottom_frame, text = "Devolver", command=devolver)
devolucion_btn.grid(row=1, column=1, padx=10, pady=10, ipadx=15)

registro_btn = ttk.Button(bottom_frame, text = "Registrar Alumno", command=open_registro)
registro_btn.grid(row=2, column=0, padx=10, pady=10, ipadx=1)

pendientes_btn = ttk.Button(bottom_frame, text = "Pendientes")
pendientes_btn.grid(row=2, column=1, padx=10, pady=10, ipadx=15)




root.mainloop()