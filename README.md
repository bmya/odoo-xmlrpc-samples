[![License: LGPL-3](https://img.shields.io/badge/licence-LGPL--3-blue.png)](http://www.gnu.org/licenses/lgpl-3.0-standalone.html)
# Ejemplos de Uso de XMLRPC en Odoo

Este repositorio contiene ejemplos de uso de estos servicios.
Se proveen los siguientes:

[Consulta y Agregado de Clientes / Proveedores](add_partner.py)

[Consulta de Cuentas Contables, diarios y otros parametros, Agregado de Asientos Contables y Publicación](add_account_entry.py)

Estos han sido probados en Odoo 13.0 Enterprise, con la localización para Chile instalada.

#### Nota:
Durante los test se encuentra que el [Issue #29768](https://github.com/odoo/odoo/issues/29768) de Odoo aún no ha sido resuelto y está impactando esta versión 13.0.
El mismo provoca un error cuando se invocan con xmlrpc, métodos que devuelven "None".
Hemos hecho una actualización en el código de la localización para que el issue mencionado no afecte el uso del método `post`.

Autor: Daniel Blanco, Blanco Martín & Asociados
![Logo BMyA](https://blancomartin.cl/logo.png)


