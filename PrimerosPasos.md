# cómo comenzar a utilizar la aplicación de escritorio

# Setup post-instalación #

Para poder utilizar la aplicación se debe crear un usuario administrador y generar la base de datos de ejemplo para la conexión a base de datos configurada (por defecto la base de datos incluída en la app web2py).

  * En la ventana HTML (work space) clic en setup.
  * Ingresar el usuario en el formulario (el login name es el mail)
  * Al terminar el formulario de registro inicial, clic en login y completar con email y password. La consola emite un mensaje de advertencia porque el usuario no tiene asociado un contacto. Ese dato puede completarse luego
  * Hacer clic nuevamente en setup
  * Clic en el link _load example db from csv_ y pulsar el botón de carga de datos.
  * Para evitar la advertencia de consola sobre asignación de contacto hacer clic en _specify firm's tin_. Ingresar un cuit de la lista y aceptar el formulario. Si el cuit es aceptado se ve un mensaje de validación del formulario en la salida de la terminal.

# Cambiar el idioma de la interfaz #

  * En la ventana HTML (work space) clic en configuración.
  * Seleccionar el link _Configurar el idioma de la aplicación_
  * Ingrese el idioma utilizando la notación _aa-bb_ para navegadores. Para idioma español utilice _es-es_ o _es_ o bien _es-[país]_. La página de configuración de idioma presenta una lista de idiomas disponibles en la notación requerida.
  * para cambiar la configuración de idioma presione el botón Enviar.
  * Los cambios de idioma se aplican al reiniciar la aplicación