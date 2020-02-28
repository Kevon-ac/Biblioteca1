from tkinter import *
import mysql.connector
from tkinter import messagebox
import custom_qr

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

root = Tk()
root.title("Biblioteca Parra")
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='book.png'))
root.geometry("250x300")
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
    registro.geometry("300x200+600+300")
    #centrar_ventana(registro)

    #Crear etiqueta titulo
    title_label = Label(registro, text = "Registrar Alumno", font=("Helvetica"))
    title_label.grid(row = 0, column = 0, columnspan = 2, pady = '10')

    #Crear formulario
    lbl_primer_nombre = Label(registro, text="Nombre").grid(row=1, column=0, sticky=W, padx=10)
    lbl_apellido = Label(registro, text="Apellido").grid(row=2, column=0, sticky=W, padx=10)
    lbl_fechaNacimiento = Label(registro, text="Fecha de Nacimiento").grid(row=3, column=0, sticky=W, padx=10)

    #Crear Cajas de entrada
    tb_primer_nombre = Entry(registro)
    tb_primer_nombre.grid(row=1, column=1, pady=5)

    tb_apellido = Entry(registro)
    tb_apellido.grid(row=2, column=1, pady=5)

    tb_fechaNacimiento = Entry(registro)
    tb_fechaNacimiento.grid(row=3,column=1, pady=5)

    #Crear Botones
    btn_agregar_usuario = Button(registro, text="Agregar Usuario", command=agregar_usuario)
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
    title_label = Label(prestamo, text = "Favor de ingresar \nel nombre y apellido del alumno", font=("Helvetica"))
    title_label.grid(row = 0, column = 0, columnspan = 2, pady = '10')

    #formulario
    lbl_primer_nombre = Label(prestamo, text="Nombre").grid(row=1, column=0, sticky=W, padx=10)
    lbl_apellido = Label(prestamo, text="Apellido").grid(row=2, column=0, sticky=W, padx=10)

    tb_primer_nombre = Entry(prestamo)
    tb_primer_nombre.grid(row=1, column=1, pady=5)

    tb_apellido = Entry(prestamo)
    tb_apellido.grid(row=2, column=1, pady=5)

    btn_agregar_usuario = Button(prestamo, text="Aceptar", command=buscar_usuario)
    btn_agregar_usuario.grid(row=4, column=1, padx=10, pady=10)
    


#Etiqueta "Bienvenido"
var = StringVar()
welcome = Label(root, textvariable=var, relief = FLAT, bd = 30, )
var.set("Bienvenido")
welcome.pack()

#Frame que contiene los botones
frame = Frame(root)
frame.pack()
frame.config(bg = "blue")
frame.config(width = "150", height = "150")

bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

prestamo_btn = Button(frame, text = "Prestar", command=prestamo)
prestamo_btn.pack(side = LEFT)

devolucion_btn = Button(frame, text = "Devolver")
devolucion_btn.pack(side = RIGHT)

registro_btn = Button(frame, text = "Registrar Alumno", command=open_registro)
registro_btn.pack(side = BOTTOM)



root.mainloop()