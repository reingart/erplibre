# describes common tasks for users in ERP Libre

# Introducción #

En esta sección se explican las tareas básicas de uso de ERP Libre. Estas instrucciones se basan en una instalación configurada en idioma español que incluye la base de datos de ejemplo. Las instrucciones para la carga de registros de base de datos inicial se pueden ver en la página [LibreGUI Primeros pasos](http://code.google.com/p/erplibre/wiki/FirstStepsWithERP).


### Personalización de la empresa por defecto del sistema ###

Para poder realizar cualquier operación en la base de datos de ERP Libre, se recomienda configurar previamente los _datos locales_ de su firma, estos datos son utilizados por ERP Libre para rótulos de documentos, gestión de cuentas corrientes, control de existencias u otras operaciones que impliquen movimientos asociados a distintas entidades. La base de datos de ejemplo contiene una empresa preconfigurada que se puede utilizar como plantilla para sobreescribir con los datos de su firma.

  * Ingrese como usuario administrativo (opción "iniciar sesión")

![https://lh5.googleusercontent.com/-FCVe0SwmnPg/Tusoh35ibBI/AAAAAAAAAac/wi3VffnJnps/s640/mdu_01_login_hand.png](https://lh5.googleusercontent.com/-FCVe0SwmnPg/Tusoh35ibBI/AAAAAAAAAac/wi3VffnJnps/s640/mdu_01_login_hand.png)

  * Seleccionar el link _ABM_

![https://lh6.googleusercontent.com/-X_2rTrFpsEY/Tusoh7i76BI/AAAAAAAAAaY/DtDuBVIQTOA/s640/mdu_02_crud.png](https://lh6.googleusercontent.com/-X_2rTrFpsEY/Tusoh7i76BI/AAAAAAAAAaY/DtDuBVIQTOA/s640/mdu_02_crud.png)

  * Seleccionar el link _Proveedor_ en la sección _SCM_

![https://lh6.googleusercontent.com/-6cF0oD9sW-g/Tusoi1mTbcI/AAAAAAAAAas/KUXM9dSjjqY/s640/mdu_03_crud_scm_hand.png](https://lh6.googleusercontent.com/-6cF0oD9sW-g/Tusoi1mTbcI/AAAAAAAAAas/KUXM9dSjjqY/s640/mdu_03_crud_scm_hand.png)

  * Seleccione el proveedor por defecto (clic en el link ubicado en la primer columna)

![https://lh4.googleusercontent.com/-tX2TOlyOoIE/TusolJ18JkI/AAAAAAAAAbE/M_p1hWgHH0I/s640/mdu_05_crud_scm_supplier_default_hand.png](https://lh4.googleusercontent.com/-tX2TOlyOoIE/TusolJ18JkI/AAAAAAAAAbE/M_p1hWgHH0I/s640/mdu_05_crud_scm_supplier_default_hand.png)

  * Modifique el registro con la información de su empresa (mantenga el valor de código -1, que por defecto es la empresa local del sistema. Esta opción es personalizable, pero si se modifica se debe actualizar la opción código de proveedor por defecto, en la tabla de opciones)
  * Al finalizar el formulario aplique los cambios presionando el botón Enviar/Submit.

![https://lh4.googleusercontent.com/-ToLgZYBzbw8/TusokwldSYI/AAAAAAAAAbA/BJvj6hkcpHE/s640/mdu_06_crud_scm_supplier_default_edit.png](https://lh4.googleusercontent.com/-ToLgZYBzbw8/TusokwldSYI/AAAAAAAAAbA/BJvj6hkcpHE/s640/mdu_06_crud_scm_supplier_default_edit.png)

![https://lh5.googleusercontent.com/-D1qrQPvPjn4/TusolcFMT7I/AAAAAAAAAbM/FwKJvKy0Uqw/s640/mdu_07_crud_scm_supplier_default_edit_submit_hand.png](https://lh5.googleusercontent.com/-D1qrQPvPjn4/TusolcFMT7I/AAAAAAAAAbM/FwKJvKy0Uqw/s640/mdu_07_crud_scm_supplier_default_edit_submit_hand.png)

### Otras opciones generales de la base de datos ###

ERP Libre almacena las opciones locales de la base de datos en la tabla especial _option_. La base de datos de ejemplo contiene opciones por defecto para poder realizar operaciones básicas como registro de documentos y actualización de existencias.

Cada registro de la tabla _option_ contiene un campo _name_ que identifica la opción en la tabla para ser recuperada por la interfaz de negocio. El valor asociado a la opción se especifica en el campo _value_. Si el valor almacenado es una secuencia, se debe utilizar el signo "|" como separador.Además la tabla _option_ admite argumentos de entrada en el campo _args_, para almacenar conjuntos de opciones con distintos parámetros.


Opciones por defecto de la base de datos de ejemplo (Lista parcial)

| **nombre** | **valor** | **detalle** |
|:-----------|:----------|:------------|
| default\_supplier\_code | -1 | Proveedor por defecto (para la firma local del sistema) |
| customer\_allowed\_orders | | 3 | | Los documentos de pedidos que se muestran para clientes (interfaz web) |
| customer\_default\_order | 3 | El documento de pedidos seleccionado por defecto (interfaz web) |
| customer\_default\_order | 3 | El documento de pedidos por defecto para clientes (interfaz web) |
| current\_account\_payment | 1 | El código utilizado para el concepto cuentas corrientes en métodos de pago |
| sales\_check\_input\_concept | 110101 | Concepto a aplicar en pagos con cheques para comprobantes de ventas |
| quota\_frequence | 30 | Cantidad de días para plazos de pago de cuentas corrientes |
| default\_customer\_code | -1 | Deudor por defecto (para la firma local del sistema) |
| purchases\_check\_input\_concept |111305 | Código de concepto para cheques en operaciones de compras |
| purchases\_payment\_point\_of\_sale\_code | 5 | Punto de venta de comprobantes de compras para pagos |
| sales\_payment\_point\_of\_sale\_code | 4 | Punto de venta de comprobantes de ventas para pagos |

Las opciones del sistema se pueden visualizar y editar seleccionando el link opciones, en la página de configuración.

![https://lh5.googleusercontent.com/-71iUxTJUous/TusonLZFMSI/AAAAAAAAAbc/2x0T8K4KAkE/s640/mdu_08_setup_options_hand.png](https://lh5.googleusercontent.com/-71iUxTJUous/TusonLZFMSI/AAAAAAAAAbc/2x0T8K4KAkE/s640/mdu_08_setup_options_hand.png)

![https://lh3.googleusercontent.com/-uMJ4KlJmBG0/TusonDpbqKI/AAAAAAAAAbo/Rg6DLeS0PdA/s640/mdu_09_setup_options_list.png](https://lh3.googleusercontent.com/-uMJ4KlJmBG0/TusonDpbqKI/AAAAAAAAAbo/Rg6DLeS0PdA/s640/mdu_09_setup_options_list.png)

### Ingreso básico de productos ###

Para ingresar un nuevo producto al sistema, utilice la sección ABM:

  * Ingrese como usuario administrativo (opción "iniciar sesión")
  * Seleccionar el link _ABM_
  * Seleccionar el link _Concepto_ en la sección _Operaciones_

![https://lh5.googleusercontent.com/-RMyI1i4Weu4/Tusooo6bPRI/AAAAAAAAAbs/NqcLOAjbiOM/s640/mdu_11_new_concept_crud_operations_hand.png](https://lh5.googleusercontent.com/-RMyI1i4Weu4/Tusooo6bPRI/AAAAAAAAAbs/NqcLOAjbiOM/s640/mdu_11_new_concept_crud_operations_hand.png)

  * Seleccionar el link _Crear concepto_ sobre la lista de registros de la tabla producto.
  * Ingrese un código único para identificar el producto en el sistema
  * Ingrese los valores según los campos del registro incluyendo las referencias a tablas externas (requisito para la validación del formulario)
  * Al finalizar, presione el botón Submit/Enviar.

![https://lh4.googleusercontent.com/-gDMNWwRuUYk/TusonBZIrvI/AAAAAAAAAbY/OJi9GKLoito/s640/mdu_10_new_concept.png](https://lh4.googleusercontent.com/-gDMNWwRuUYk/TusonBZIrvI/AAAAAAAAAbY/OJi9GKLoito/s640/mdu_10_new_concept.png)

### Ingreso básico de clientes ###

El método para ingreso de clientes u otros elementos del sistema es similar al descripto para el caso de los registros de productos. El controlador para ABM de la base de datos da acceso a los registros de toda tabla definida para ERP Libre.

  * Ingrese como usuario administrativo (opción "iniciar sesión")
  * Seleccionar el link _ABM_
  * Seleccionar el link _Cliente_ en la sección _CRM_.
  * Seleccionar el link _Crear cliente_ sobre la lista de registros de la tabla cliente. Además de insertar un nuevo registro, puede optar por utilizar un cliente de la base de datos como plantilla. Si desea utilizar un cliente existente en la base de datos, selecciónelo desde la lista de clientes con clic en el link de la columna _Editar_
  * Ingrese un código único para identificar el cliente en el sistema
  * Ingrese los valores según los campos del registro incluyendo las referencias a tablas externas (requisito para la validación del formulario)
  * Es requisito asociar el cliente a un registro en la tabla deudor.
  * Al finalizar, presione el botón Submit/Enviar.

### Ingresar Pedidos ###

Para ingresar pedidos de clientes se puede utilizar la sección _Panel de clientes_:

  * Seleccionar el link _Panel de contol de clientes_ en la sección de inicio

![https://lh3.googleusercontent.com/-iBwa-KuIJ7c/Tusoo6YQVbI/AAAAAAAAAb0/fSatAgbezHY/s640/mdu_12_customer_control_panel_hand.png](https://lh3.googleusercontent.com/-iBwa-KuIJ7c/Tusoo6YQVbI/AAAAAAAAAb0/fSatAgbezHY/s640/mdu_12_customer_control_panel_hand.png)

  * Seleccionar el link _Crear/Editar pedidos_.

![https://lh5.googleusercontent.com/-K-5zSVs2ywY/TusoqEKx4MI/AAAAAAAAAcA/R1QnOQdomdw/s640/mdu_13_customer_control_panel_page_hand.png](https://lh5.googleusercontent.com/-K-5zSVs2ywY/TusoqEKx4MI/AAAAAAAAAcA/R1QnOQdomdw/s640/mdu_13_customer_control_panel_page_hand.png)

  * Completar el formulario en pantalla con los datos básicos de la operación. El formulario presenta el tipo de documento asignado por defecto para pedidos.

![https://lh5.googleusercontent.com/-i4e8OnDHno4/TusoqFttadI/AAAAAAAAAcE/ioRAdx2fd4c/s640/mdu_14_customer_control_panel_edit_order.png](https://lh5.googleusercontent.com/-i4e8OnDHno4/TusoqFttadI/AAAAAAAAAcE/ioRAdx2fd4c/s640/mdu_14_customer_control_panel_edit_order.png)

  * Para procesar los datos ingresados en el pedido, presione Submit/Enviar
  * Los ítem del pedido se ingresan con el comando en pantalla _ingresar ítem_, sobre la lista de conceptos ingresados al pedido. Especifique concepto, descripción (opcional) y cantidad.

![https://lh4.googleusercontent.com/-VJ4vILMjLFg/Tusoqk4CJXI/AAAAAAAAAcI/sar1sIdneWY/s640/mdu_15_create_order_new_item_hand.png](https://lh4.googleusercontent.com/-VJ4vILMjLFg/Tusoqk4CJXI/AAAAAAAAAcI/sar1sIdneWY/s640/mdu_15_create_order_new_item_hand.png)

![https://lh5.googleusercontent.com/-69hJELeGumQ/Tusor8-CkPI/AAAAAAAAAcg/pQAgVaQ6nUM/s640/mdu_16_create_order_new_item_form.png](https://lh5.googleusercontent.com/-69hJELeGumQ/Tusor8-CkPI/AAAAAAAAAcg/pQAgVaQ6nUM/s640/mdu_16_create_order_new_item_form.png)

Los pedidos no requieren confirmación para su registro en la base de datos. Cada pedido se almacena automáticamente al iniciar el formulario. (Es posible eliminar pedidos desde la lista de operaciones).

### Asignación de pedidos ###

Al asignar pedidos, las cantidades asignadas por ítem se transfieren a un nuevo documento por cliente:

  * Seleccionar el link _Asignación de pedidos_ en la sección de inicio. El sistema presentará un listado de cantidades por ítem y cliente pendientes de asigación.

![https://lh3.googleusercontent.com/-MKh_NvalSig/TusososFv5I/AAAAAAAAAcs/STPLndTqeCE/s640/mdu_18_order_allocation_hand.png](https://lh3.googleusercontent.com/-MKh_NvalSig/TusososFv5I/AAAAAAAAAcs/STPLndTqeCE/s640/mdu_18_order_allocation_hand.png)

  * Ingrese las cantidades a asignar por ítem en el campo _Asignar_ para cada ítem de la lista. El listado de pedidos pendientes de asignación presenta las cantidades solicitadas, asignaciones parciales y el total de existencia para cada ítem.

![https://lh3.googleusercontent.com/-hKypfSCCHkM/TusotJPPH5I/AAAAAAAAAcw/rkW_H9rQz5s/s640/mdu_19_order_allocation_items.png](https://lh3.googleusercontent.com/-hKypfSCCHkM/TusotJPPH5I/AAAAAAAAAcw/rkW_H9rQz5s/s640/mdu_19_order_allocation_items.png)

  * Presionar el botón _Asignar pedidos/Allocate orders_ al pie del formulario. Los nuevos comprobantes generados se listan en pantalla. Es posible examinar y editar los comprobantes haciendo clic en cada link de la nueva lista

![https://lh5.googleusercontent.com/-ZjeVFmsrAA8/Tusot1p2wiI/AAAAAAAAAc8/DrwtkhJlUVI/s640/mdu_20_order_allocation_created.png](https://lh5.googleusercontent.com/-ZjeVFmsrAA8/Tusot1p2wiI/AAAAAAAAAc8/DrwtkhJlUVI/s640/mdu_20_order_allocation_created.png)

  * Las asignaciones de pedidos almacenadas en la base de datos se pueden consultar en el listado general (seleccionando el link _Lista de operaciones.._)


### Remitos ###

Se pueden ingresar remitos desde el formulario general para comprobantes o utilizar una asignación de pedidos como punto de partida.

Instrucciones para generar un remito con datos de un comprobante de asignación de pedidos

  * Seleccionar el link _Asignación de pedidos_ en la sección de inicio

![https://lh5.googleusercontent.com/-MPE1K63vH08/TusovQScxsI/AAAAAAAAAdI/7yNLH8EyNeU/s640/mdu_22_order_allocation_link_hand.png](https://lh5.googleusercontent.com/-MPE1K63vH08/TusovQScxsI/AAAAAAAAAdI/7yNLH8EyNeU/s640/mdu_22_order_allocation_link_hand.png)

  * Seleccionar el link _Lista de operaciones..._

![https://lh3.googleusercontent.com/-s4-xYbtzDn8/Tusovju5RAI/AAAAAAAAAdM/1vDT8VU5X0o/s640/mdu_23_order_allocation_list_link_hand.png](https://lh3.googleusercontent.com/-s4-xYbtzDn8/Tusovju5RAI/AAAAAAAAAdM/1vDT8VU5X0o/s640/mdu_23_order_allocation_list_link_hand.png)

  * Abrir el detalle del comprobante (clic en el campo editar de la tabla) a utilizar.
  * Para generar el nuevo remito, seleccione el link _Nuevo remito desde esta asignación de pedidos_. Se generará un nuevo comprobante con los datos de la asignación de pedidos como base.

![https://lh5.googleusercontent.com/-gcSgFVuHD1Y/Tusowk6v7tI/AAAAAAAAAdY/-0q3aXaHueM/s640/mdu_24_order_allocation_update_form_hand.png](https://lh5.googleusercontent.com/-gcSgFVuHD1Y/Tusowk6v7tI/AAAAAAAAAdY/-0q3aXaHueM/s640/mdu_24_order_allocation_update_form_hand.png)

  * Complete el formulario de remito y presione el botón _Enviar_. Utilice un código alfanumérico único para identificar el documento.

![https://lh4.googleusercontent.com/-IOuLwwb0Wb4/Tusowvkqh1I/AAAAAAAAAdU/OqSQDFNxjIY/s640/mdu_25_order_allocation_new_packing_slip.png](https://lh4.googleusercontent.com/-IOuLwwb0Wb4/Tusowvkqh1I/AAAAAAAAAdU/OqSQDFNxjIY/s640/mdu_25_order_allocation_new_packing_slip.png)

### Facturación de remitos ###

El pasaje de datos de remitos para facturación se realiza a través del formulario _Facturación de productos_

  * Seleccionar el link _Modo RIA facturación de productos_ en la sección de inicio

![https://lh4.googleusercontent.com/-u8oDq7ZgBlE/Tusox4udQPI/AAAAAAAAAdo/uWx26KmQmoA/s640/mdu_27_product_billing_link_hand.png](https://lh4.googleusercontent.com/-u8oDq7ZgBlE/Tusox4udQPI/AAAAAAAAAdo/uWx26KmQmoA/s640/mdu_27_product_billing_link_hand.png)

  * Completar los datos iniciales del formulario (deudor, cliente y lista de precios)

![https://lh4.googleusercontent.com/-_EvQ1cwNiAE/TusoyupOAMI/AAAAAAAAAd0/EhNXtCEZFQc/s640/mdu_28_product_billing_starting_form.png](https://lh4.googleusercontent.com/-_EvQ1cwNiAE/TusoyupOAMI/AAAAAAAAAd0/EhNXtCEZFQc/s640/mdu_28_product_billing_starting_form.png)

  * El sistema presenta un listado completo de remitos disponibles para facturación,  con fecha y número de orden del comprobante.

![https://lh6.googleusercontent.com/-UtIiGRNsb18/TusozkAY2mI/AAAAAAAAAeA/ahUl_6ugQ1k/s640/mdu_29_product_billing_packing_slips_list.png](https://lh6.googleusercontent.com/-UtIiGRNsb18/TusozkAY2mI/AAAAAAAAAeA/ahUl_6ugQ1k/s640/mdu_29_product_billing_packing_slips_list.png)

  * Seleccione el tipo de documento a crear en el combo box al pie de la lista.
  * Marque las cajas correspondientes a los comprobantes a incluír en la nueva factura y presione el botón "Facturar marcados". La nueva factura generada se visualizará en el formulario de operaciones con los elementos del remito cargados automáticamente.
  * Es posible personalizar el formulario cambiando el encabezado o modificando el detalle (ABM de ítems). Para instrucciones sobre el uso del formulario general de operaciones ver la sección _Formulario de movimientos_.
  * Para registrar la operación seleccione el link _Registrar_

![https://lh6.googleusercontent.com/-qiLekqGBiag/Tuso0e7xyCI/AAAAAAAAAeQ/dEr9mPJg1z8/s640/mdu_30_product_billing_invoice_detail.png](https://lh6.googleusercontent.com/-qiLekqGBiag/Tuso0e7xyCI/AAAAAAAAAeQ/dEr9mPJg1z8/s640/mdu_30_product_billing_invoice_detail.png)

### Pagos de cuentas corrientes ###

Para aplicar cobros, órdenes de pago y cancelaciones de deudas de documentos registrados en cuentas corrientes se pueden generar recibos tomando como referencia una lista de comprobantes a cancelar.

Instrucciones para cancelación de comprobantes de ventas:

  * Seleccionar el link _Pagos de cuentas corrientes_ en la sección de inicio.

![https://lh3.googleusercontent.com/-jEoqvnfdKFY/Tuso29aYGII/AAAAAAAAAe0/Ju1-Cc1y0eY/s640/mdu_32_current_accounts_payments_link_hand.png](https://lh3.googleusercontent.com/-jEoqvnfdKFY/Tuso29aYGII/AAAAAAAAAe0/Ju1-Cc1y0eY/s640/mdu_32_current_accounts_payments_link_hand.png)

  * Marcar la opción _Deudor_ en el combo box de tipo de cuenta corriente y presionar _Enviar_ para continuar.

![https://lh3.googleusercontent.com/-V0-jKJinxU4/Tuso2u8hoUI/AAAAAAAAAes/SI7kGOQJ4R0/s640/mdu_33_current_accounts_payments_starting_form.png](https://lh3.googleusercontent.com/-V0-jKJinxU4/Tuso2u8hoUI/AAAAAAAAAes/SI7kGOQJ4R0/s640/mdu_33_current_accounts_payments_starting_form.png)

  * Elija un rango de fechas y un deudor en el formulario de datos de la cuenta corriente y luego presione _Enviar_. El sistema presenta un listado de comprobantes registrados. Los comprobantes pendientes de cancelación tienen importes mayores a cero.

![https://lh5.googleusercontent.com/-Zeo-WbjV7FQ/Tuso3aI82mI/AAAAAAAAAe8/H-FKt7ZiFzc/s640/mdu_34_current_accounts_payments_second_form.png](https://lh5.googleusercontent.com/-Zeo-WbjV7FQ/Tuso3aI82mI/AAAAAAAAAe8/H-FKt7ZiFzc/s640/mdu_34_current_accounts_payments_second_form.png)

  * Seleccione la opción _Cobrar_ en el combo box de tipo de operación.
  * Si desea registrar la cancelación de la deuda total del deudor para los límites de fecha establecidos, presione el botón _Enviar_ al final del formulario.
  * Si la cancelación de la deuda es parcial, deberá seleccionar previamente cada comprobante a cancelar marcándolo en cada campo _Seleccionar_ del listado.

![https://lh5.googleusercontent.com/-OYcE4E29L30/Tuso3_qy30I/AAAAAAAAAfM/XB-Hy_0s49s/s640/mdu_35_current_accounts_payments_operations_list.png](https://lh5.googleusercontent.com/-OYcE4E29L30/Tuso3_qy30I/AAAAAAAAAfM/XB-Hy_0s49s/s640/mdu_35_current_accounts_payments_operations_list.png)

  * En el nuevo formulario de opciones para pagos de cuentas corrientes, especifique el tipo de documento (Recibo), el concepto a registrar y la forma de pago. Al finalizar, presione _Enviar_.

![https://lh6.googleusercontent.com/-PWbt99SQAao/Tuso48HHfHI/AAAAAAAAAfQ/NVfejGpzzB8/s640/mdu_36_current_accounts_payments_create_receipt.png](https://lh6.googleusercontent.com/-PWbt99SQAao/Tuso48HHfHI/AAAAAAAAAfQ/NVfejGpzzB8/s640/mdu_36_current_accounts_payments_create_receipt.png)

  * El sistema presenta el detalle del nuevo comprobante creado automáticamente.
  * Para la cancelación del comprobante, se debe seleccionar al menos un método de pago. Si no se ingresan métodos de pago, al registrar el comprobante se aplicará el método de pago por defecto. Seleccione el link _Ingresar método de pago_.
  * Puede comprobar los datos del encabezado del recibo o modificarlos seleccionando _Modificar encabezado_. Para regresar a la vista de detalle del comprobante seleccione _Detalle de la operación_.
  * Registre el comprobante seleccionando el link _Registrar_

![https://lh4.googleusercontent.com/-ebew0yq4Yhw/Tuso5Bm8FPI/AAAAAAAAAfc/hGLeXlv6Oew/s640/mdu_37_current_accounts_payments_created_receipt.png](https://lh4.googleusercontent.com/-ebew0yq4Yhw/Tuso5Bm8FPI/AAAAAAAAAfc/hGLeXlv6Oew/s640/mdu_37_current_accounts_payments_created_receipt.png)

![https://lh3.googleusercontent.com/-C4ctxUI37eA/Tuso5bJGYCI/AAAAAAAAAfY/uodK2tSX_4A/s640/mdu_38_current_accounts_payments_receipt_accepted.png](https://lh3.googleusercontent.com/-C4ctxUI37eA/Tuso5bJGYCI/AAAAAAAAAfY/uodK2tSX_4A/s640/mdu_38_current_accounts_payments_receipt_accepted.png)

### Impresión de comprobantes ###

> El formulario general de movimientos permite la conversión de la operación al formato _Portable file document_ de Adobe (R) utilizando la interfaz [PyFPDF](http://code.google.com/p/pyfpdf) para facilitar la impresión con equipos estándar.

  * Desde el detalle del comprobante seleccione el link _Imprimir este documento_. Si no se producen errores en la conversión el sistema presenta una vista especificando el nombre del archivo almacenado para impresión. La ruta por defecto para los archivos .pdf es la subcarpeta _output_ en el directorio raíz de la aplicación de escritorio.

![https://lh3.googleusercontent.com/-ufKnIhvyIp4/Tuso6n6JzaI/AAAAAAAAAfk/eyN_JN4BWm8/s640/mdu_39_print_document_link_hand.png](https://lh3.googleusercontent.com/-ufKnIhvyIp4/Tuso6n6JzaI/AAAAAAAAAfk/eyN_JN4BWm8/s640/mdu_39_print_document_link_hand.png)

![https://lh3.googleusercontent.com/-xhzRfdHEVsg/Tuso7RzaU4I/AAAAAAAAAfw/-TcH-fMe7LA/s640/mdu_40_print_document_pdf_created.png](https://lh3.googleusercontent.com/-xhzRfdHEVsg/Tuso7RzaU4I/AAAAAAAAAfw/-TcH-fMe7LA/s640/mdu_40_print_document_pdf_created.png)

![https://lh3.googleusercontent.com/-2RLM8zKjE1A/Tuso7W06UsI/AAAAAAAAAf0/gc_4Xny2tLM/s640/mdu_41_print_document_pdf_header.png](https://lh3.googleusercontent.com/-2RLM8zKjE1A/Tuso7W06UsI/AAAAAAAAAf0/gc_4Xny2tLM/s640/mdu_41_print_document_pdf_header.png)

![https://lh6.googleusercontent.com/-PeRjBABWmIs/Tuso7gJk4SI/AAAAAAAAAf4/0VdNUxDPYu8/s640/mdu_42_print_document_pdf_footer.png](https://lh6.googleusercontent.com/-PeRjBABWmIs/Tuso7gJk4SI/AAAAAAAAAf4/0VdNUxDPYu8/s640/mdu_42_print_document_pdf_footer.png)

# Formulario de movimientos #

El formulario de movimientos de la operación permite realizar altas, bajas y modificaciones para elementos del detalle en una operación determinada, modificar opciones de selección de depósito para actualización de existencias, cuentas corrientes, descuentos y recargos, métodos de pago, encabezado del comprobante y cálculo de impuestos.

El acceso al formulario de movimientos desde la sección inicial es el link _Lista de movimientos_.

Nota: El término movimientos se utiliza tanto para operaciones como para ítems de operaciones, aunque en la definición de la base de datos se trata de tablas distintas. Los movimientos de la base de datos se asocian a el conjunto de elementos relacionados a un registro de operación. Un elemento operación puede contener uno o más elementos movimiento.

Para ingresar al detalle de una operación en la lista de movimientos, seleccione el link de la operación en la columna _Editar_. El sistema presenta la vista de detalle de la operación seleccionada.

### Acciones de la vista de detalle del formulario de movimientos ###

  * _Cuenta corriente de Deudor_
Presenta un listado con comprobantes no cancelados para el deudor activado por el formulario de operación.
  * _Cuenta corriente de Cliente_
Presenta un listado con comprobantes no cancelados para el cliente activado por el formulario de operación.
  * _Modificar encabezado_
Permite modificar datos básicos del comprobante como cliente/proveedor, tipo de documento, vendedor o forma de pago.
  * _Ingresar ítem_
Inserta un elemento de la operación por medio de un formulario de edición
  * _Ingresar método de pago_
Utilizado para ingresar diferentes pagos y detalles de pagos asociados a la operación seleccionada.
  * _Ingresar artículo_
Similiar a la opción de ingresar ítem, pero permite seleccionar conceptos por categoría/rubro
  * _Ingresar cheque_
Asocia cheques al comprobante
  * _Ingresar impuesto_
Ingreso de impuestos manual (para montos de impuestos no calculados automáticamente)
  * _Cuenta corriente_
Presenta una secuencia de formularios para establecer las opciones de cuenta corriente de la operación para ventas y compras.
  * _Descuentos recargos_
Formulario para ingreso de conceptos de recargo/descuento. Permite ingresar porcentuales o valores fijos.
  * _Registrar operación_
Procesa el documento para registro en el libro diario, y validación de datos.
  * _Seleccionar una lista de precios_
Establece la lista de referencia para cálculo automático de montos por movimiento.
  * _Operación: actualizar/no actualizar existencias_
Es posible registrar operaciones sin afectar los valores de existencia en depósito deshabilitando esta opción.
  * _Acción para impuestos_
Opción para habilitar o deshabilitar el cálculo automático de impuesto por movimiento
  * Links de columna _Editar_
Los link de la columna _Editar_ en la lista de elementos dan acceso a los formularios de edición para cada categoría (pagos, ítem, impuestos)