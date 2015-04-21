# borrador en español para manual de desarrollo

# ERP Libre #
## Sistema de gestión desarrollado en Python y WEB2PY ##

## Información para desarrolladores ##

### Observaciones sobre el proceso de desarrollo. ###

La fase inicial del proyecto consiste en la migración a Python y web2py de las aplicaciones de escritorio para gestión de empresas de Mariano Reingart - Sistemas Ágiles (Gestión Pyme y otras)
La interfase gráfica para las aplicaciones de escritorio se desarrollará en base a las librerías gráficas wx para Python y la herramienta para python y wx gui2py
El proyecto sigue el patrón MVC como esquema de programación de las interfaces. Esto permitirá una integración más ágil de las sub-aplicaciones web (por medio de web2py) y las herramientas de escritorio (gui2py)

Una versión inicial del sistema incluirá las siguientes funcionalidades:
  * facturación
  * stock
  * cuentas corrientes

El procesamiento de datos de la organización se basa en las técnicas tradicionales de
contabilidad por partida doble.

La unidad de operación mínima es llamada movimiento (movement). Los movimientos se agrupan en instancias superiores, denominadas operación (operation). La operación es un conjunto coherente de movimientos realizados en una fecha determinada, referida a un proveedor y a un cliente determinados. Una operación no implica un documento fiscal, y abarca toda transacción de la organización, como liquidaciones de sueldos o traslados de mercaderías

Ejemplo de clasificación de objetos para una operación:

operación 1
| fecha       | hoy   |   |
|:------------|:------|:--|
| cliente     | Gumby |   |
| proveedor   | Sr. Conejo |  |
| documento   | factura A |  |
| movimientos |  |  |
|             | ítem código 0001 x 3 unidades | 700 |
|             | ítem código 0002 x 2 unidades | 300 |
|             | IVA 21 % | 210 |
|             | pago contado | 1210 |

La carga de eventos por partida doble permite la validación de cada operación (movimiento) reflejándose los movimientos en elementos de registro contables.

Asientos para operación 1:

| Cuenta  | debe | haber |
|:--------|:-----|:------|
| Sin afectación contable | 700 |  |
| Sin afectación contable | 300 |  |
| IVA ventas | 210 |  |
| Caja |  | 1210 |

El criterio elemental de validación consiste en la suma a cero de la totalidad de los asientos en la lista.

Para el pasaje de movimientos a asientos se utilizan los objetos concepto y cuenta. Todo movimiento refiere a un concepto, que indica parámetros como la cuenta afectada (account) y el tipo de asiento (débito/crédito). Los conceptos (al igual que el resto de los objetos manejados) son registros de base de datos relacional y permiten la personalización para casos particulares (esquemas contables especiales/modificaciones a medida/adaptación a requerimientos locales), aunque se pretende proveer un caso estándar para una implementación por defecto del sistema, en base a ejemplos de bases de datos pre configuradas. El objeto concepto es de suma importancia en el diseño de datos del sistema, ya que agrupa todo criterio de transacción (incluyendo impuestos, mercaderías, y cualquier otro motivo de imputación contable)

Los movimientos pueden o no actualizar stock, según especificación por parámetro en el tipo de documento.
El control y proceso de existencia (stock) consiste en la utilización de tablas inter-referidas indicando concepto, valor y depósito (warehouse). La modificación de stock se realiza en el controlador (en base a la opción de afectar stock) al procesarse cada operación.

Una operación debe contener al menos un movimiento. Un movimiento puede ser cualquier actividad de la organización que implique la modificación de los parámetros de existencia o actividad comercial. Además las operaciones refieren especialmente a un conjunto de elementos que definen el orden de esta operación (la categoría documento). Esta clasificación de operaciones por documento permiten identificar los movimientos según el tipo de operación, y realizar el proceso de los datos en función de la clase especificada.
Además los elementos documento (y también los conceptos) poseen parámetros para ordenar el flujo de proceso de los movimientos de cada operación.

La interfaz de negocio consiste en una serie de funciones distribuidas en el controlador de la aplicación que se alimenta de parámetros establecidos por el usuario en los formularios y de opciones de procesamiento de movimientos almacenadas en una tabla especial en la base de datos relacional.

La interfaz de usuario se divide en módulos/secciones operativas, siguiendo la estructura de la aplicación de origen en Visual Basic

Actualmente el desarrollo está enfocado en el módulo movimientos (formulario de movimientos de Gestión Pyme), que es fundamental en
la actualización de stock, facturación y cuentas corrientes

### Exploración de (algunas) tablas para la base de datos relacional. ###

Deudor (customer)
  * Una de las partes afectadas de la operación.
Acreedor (supplier)
  * La contraparte de la operación. Suele ser el emisor del documento
Concepto (concept)
  * Criterio para transacción (impuesto, pago, cobro, venta, ingreso, egreso).
  * Refiere a cuenta y especifica débito/crédito (entry/exit).
Cuenta (account)
  * Clase contable (caja, ventas por cuenta corriente, deudores,...)
Operación (operation)
  * Instancia de compra/venta/contrato/transferencia/pago
Movimiento (movement)
  * Elemento de operación. Define concepto, cantidad, valor, monto

Ejercicio (accounting year)
  * período contable que agrupa los libros diarios
Libro diario (journal entry)
  * consiste de una serie de asientos contables agrupados por una fecha única
Asiento (entry)
  * la unidad mínima de registro contable del sistema.
  * Refiere a una cuenta, posee monto y especifica debe/haber

La direccionalidad de los asientos contables (es decir, el signo de las imputaciones) se resuelve en el controlador en base a un parámetro de inversión especificado en el objeto documento

### Esquema actual de la aplicación ###

(Es probable que la ubicación y distribución del código fuente para las interfaces se modifique apreciablemente para adaptarlo a los requerimientos de gui2py)

El modelo, el controlador y la vista se dividen cada uno según las subáreas:
  * COMÚN (COMMON)
  * CONTABILIDAD (ACCOUNTING)
  * MANEJO DE CLIENTES (CRM)
  * ARANCELES (FEES)
  * FINANZAS (FINANCIALS)
  * PERSONAL (HR)
  * OPERACIONES (OPERATIONS)
  * PRODUCTOS (SCM)

Para controladores que requieren procesos extensos se utilizaron módulos auxiliares (en la carpeta modules) siguiendo el mismo criterio de clasificación por subáreas.

### Sintaxis ###

Para las consultas a la base de datos el formato de los comandos y su sintaxis
corresponde a la implementada por el framework [web2py](http://www.web2pycom), sobre el cual está desarrollada la interfaz de datos de ERP Libre.

Para consultas de registros de tablas de bases de datos migradas con valores id 0, se recomienda utilizar la forma

```
obj = db(db.tabla.registro_id == n).select().first()
```

por incompatibilidad de la forma abreviada (recuperar valores de diccionarios de Python), por ej.:

```
obj = db.tabla[n]
```

La interfaz wx (desktop) de ERP Libre implementa el patrón MVC para las vistas html y soporta el sistema de plantillas incluído en web2py. La sintaxis para la construcción y edición de vistas es idéntica para la interfaz web y desktop. Las ubicaciones de los archivos de plantillas de cada sección son independientes (ver _Ubicaciones de archivos_)

### Ubicaciones de archivos ###

ERP Libre se divide actualmente en dos secciones: Interfaz de escritorio (wx) e interfaz web (App web2py)

Al instalar ERP Libre por medio del script de instalación (_setup.py_), se crea una carpeta para cada sección. La carpeta de la aplicación web se genera en un subdirectorio de _applications_ en el path de la instalación de web2py. La ruta de la interfaz de escritorio corresponde a la ubicación en la que se descomprimió el archivo de instalación (o la carpeta del proyecto en el caso de instalación con mercurial)

Presentamos como ejemplo una estructura típica de la instalación para un equipo con sistema operativo GNU/Linux


| **ubicación** | **interfaz web** | **interfaz de escritorio** |
|:---------------|:-----------------|:---------------------------|
| carpeta raíz | /home/usuario/web2py/applications/erplibre | /home/usuario/erplibre |
| vistas | /home/usuario/web2py/applications/erplibre/views | /home/usuario/erplibre/views |
| controladores | /home/usuario/web2py/applications/erplibre/controllers | /home/usuario/erplibre/controllers |
| modelos | /home/usuario/web2py/applications/erplibre/models | vacío |
| módulos | /home/usuario/web2py/applications/erplibre/modules | vacío |
| almacenamiento de comprobantes | vacío | /home/usuario/erplibre/output |
| imágenes | /home/usuario/web2py/applications/erplibre/static/images | /home/usuario/erplibre/images |


### Nomenclatura ###

El componente HTML de la interfaz de escritorio soporta direcciones URL absolutas para recursos web o relativas para las funciones de la aplicación. En el caso de las URL relativas locales se debe anteponer el nombre de la aplicación de escritorio a la especificación de controlador y función (erplibre por defecto)

Para los nombres de direcciones tipo URL se ha tomado la siguiente regla

_erplibre/sección/funcion_

Exceptuando el caso del formulario de operaciones, que originalmente en la aplicación en Visual Basic es "movimientos". Para ese caso se utiliza:

_erplibre/sección/movements\_función_

Ejemplos:

**URL para la acción inicial de bienvenida (o home)**

`erplibre/default/index`

**URL para iniciar el formulario de comprobantes**

`erplibre/operations/movements_start`


### Sistema de control por direcciones URL ###

Para la resolución de acciones y el manejo de comandos y eventos enviados a la interfaz de escritorio se emuló el manejo de direcciones para entorno web de web2py.

Cada sección de la interfaz envía una acción del usuario o evento para comparación en un diccionario donde se asocian comandos con la forma URL a funciones, o bien asocia directamente el evento con una función específica. Los valores almacenados en el diccionario pueden ser asociaciones a manejadores de eventos o a acciones (declaradas en la carpeta controllers).

Las acciones son órdenes de ejecución y salida por ventana en modo HTML del resultado y se componen de una cadena URL (por ej.: _erplibre/default/index_ ). La salida en formato HTML no es obligatoria y es posible ejecutar instrucciones utilizando otros elementos de la interfaz wx para devolver el resultado.

Un valor para resolución de acciones puede devolver una referencia a un manejador ubicado en otro módulo. En este caso se ejecuta la llamada a la función especificada con forma _dot syntax_, por ej.: _handlers.mi\_funcion_

Ejemplo de estructura de árbol del diccionario para el mapeo de direcciones URL:

```
direcciones = {"controlador":
                  {"funcion":
                      { "accion": "controlador.funcion"}
                  },
               "otro_controlador":
                  {"otra_funcion":
                      { "manejador": "manejadores.funcion"}
                  }
              }
```

### Diagrama para operación: ###

Tomamos como ejemplo un comprobante de venta ingresado desde la interfaz de escritorio:

**Carga de datos:**

Al iniciar un formulario de nuevo comprobante por comando en el menú o link en la ventana HTML, se llama a una función que genera los campos a recuperar de la ventana interactiva (datos ingresados por el usuario) y configura un evento personalizado por la interfaz [gui2py](http://code.google.com/p/gui2py), para manejo de formularios HTML.

```
# Método OnLinkClicked de clase gui.NewHTMLWindow
...
# application action address
xml = action(link.Href)
config.html_frame.window.SetPage(unicode(xml, "utf-8"))
...


# función gui.action: convertir objetos Python/web2py a HTML
# maneja errores y redirección http
...
# get the address/parameters tuple
url_data = get_function(url)
...
# look for function bound to imput address and call it
action_data = config.actions[ \
"controllers"][url_data[1]][url_data[2]](None, \
url_data[3], url_data[4])
...
```

La función (definida como controlador) se ejecuta inicialmente para devolver el formulario por pantalla y luego para la validación de los datos ingresados. Es posible redirigir el manejo de la validación y proceso de datos a una función externa (siguiendo el ejemplo de la demo para gui2py). El primer caso emula el modo _form self-submission_ utilizado en web2py. La función recibe un objeto EVENT de wx.

Las funciones de controlador en ERP Libre no son idénticas a las declaradas en web2py. Para poder manejar el evento de envío de formulario y recuperar parámetros url se utilizan los argumentos evt, args y vars.

```
# función en controllers/operations.py
# self-submitted form (stores post form query in config.py)
def movements_articles(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("category", \
    ...
    return dict(form = session.form, table = table)

```

La validación del formulario se procesa unicamente para llamados con parámetro EVENT no vacío (se asume un evento de envío de formulario).
Si el parámetro evt es vacío, la función devuelve un nuevo formulario web2py para salida por pantalla. Si se detecta el envío del formulario para validación, la función valida los datos y devuelve un mensaje o redirige a otra acción (por un parámetro "_redirect" para la función controladora o ejecutando el método OnLinkClicked de la ventana de origen._

```
# movements_articles()
...
    # form submitted
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, \
        keepvalues=False, dbio=False):
...
    # evento customizado gui2py
    # Si el evento se genera, llamar nuevamente a esta función
    # con el objeto EVENT como parámetro.
    config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_articles)
...
```

**Validación**

Los atributos requires de web2py permiten el control de datos ingresados y configuran las condiciones de validación de los campos para método del objeto form accepts(). Si los datos ingresados no son correctos, es posible devolver mensajes de error por consola o widget wx (Actualmente los mensajes de error son enviados a la terminal o salida por defecto) o a una nueva vista html para el caso de redirección por anulación del comprobante.

```
# función ria_movements en controllers/operations.py
...
    if session.form.accepts(evt.args, formname=None, keepvalues=False, \
    dbio=False):
        # modificar registro
        db.operation[session.operation_id].update_record( \
        **session.form.vars)

        # aplicar cambios en la base de datos
        db.commit()
        print "Form accepted"
        
        # redirección
        return config.html_frame.window.OnLinkClicked(URL( \
        a=config.APP_NAME, c="operations", f="ria_movements"))
...
```

**Registro**

El registro de operaciones y procesos posteriores a la validación son manejados por módulos auxiliares (con acceso a la base de datos). Las funciones de estos módulos reciben las referencias y variables definidas en memoria (instancias session, request ,auth), realizan los cálculos y el balanceo de los asientos (para el caso de movimientos de cuentas) y actualización de las existencias. Los módulos auxiliares (y las declaraciones de tablas para la capa de abstracción) se almacenan en el path de la aplicación de escritorio de ERP Libre, y pueden importarse desde la interfaz web (web2py app).

```
# módulo operations.py en controllers

# importar módulos auxiliares en
# app web2py
modules = __import__('applications.%s.modules' \
% config.WEB2PY_APP_NAME, globals(), locals(), \
['operations', 'crm'], -1)
crm = modules.crm
operations = modules.operations
...


# registrar operación
...
    if operations.process(db, session, session.operation_id):
        print "Operation processed"
    else:
        print "Could not process the operation"
...
```