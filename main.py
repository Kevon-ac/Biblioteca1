import mysql.connector

#comentario para probar git

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="bibliotecaparra"
)

mycursor = mydb.cursor()
 
#Inicia el lector de qr y obtiene el identificador del libro.
import custom_qr
idLibro = int(custom_qr.text)

#imprime el identificador del libro
print("El id es: " + str(idLibro))

#guarda le identificador con el libro
#sql = ("INSERT INTO libros (idLibro, Titulo, Autor, Coleccion, Estado) VALUES (%s, %s, %s, %s, %s)")
#val = (idLibro, 'El Chino', 'Chino', 'Cuentos', 'Disponible')

#Busca un libro por su id
sql = ("SELECT * FROM libros WHERE idLibro = %s")

mycursor.execute(sql, (idLibro,))

#Para guardar cambios en la base de datos
#mydb.commit()

myresult = mycursor.fetchone()

print(myresult)