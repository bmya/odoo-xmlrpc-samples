from xmlrpc import client
from datetime import datetime

url = 'https://demo.bmya.cl'
db = 'odoo13e_demo'
username = 'admin'
password = 'admin'

common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()
# {
#   'server_version': '13.0+e',
#   'server_version_info': [13, 0, 0, 'final', 0, 'e'],
#   'server_serie': '13.0',
#   'protocol_version': 1
# }

uid = common.authenticate(db, username, password, {})
# devuelve el uid del usuario autenticado.

# instancia los modelos
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

# busqueda de cuentas contables por el código de cuenta (ejemplo: 210210 cuenta proveedores
proveedores = models.execute_kw(db, uid, password,
    'account.account', 'search',
    [[['code', '=', '210210']]])[0]
# devuelve el id de la cuenta proveedores (80 en mi ejemplo)

banco = models.execute_kw(db, uid, password,
    'account.account', 'search',
    [[['code', '=', '110102']]])[0]
# devuelve el id de la cuenta banco (191 en mi ejemplo)

partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['vat', '=', '76201224-3']]])[0]
# devuelve el id del partner al que quiero asociar el asiento contable (en mi caso 46)

journal_id = models.execute_kw(
    db, uid, password, 'account.journal', 'search', [[['name', '=', 'Banco Santander CC']]])[0]
# devuelve el id del diario donde voy a registrar mi asiento contable

lineas_asiento = [[5, 0]]
lineas_asiento.append(
    [0, 0,
        {
            'account_id': proveedores,
            'partner_id': partner_id,
            'name': 'Glosa de la linea 1 (pago de factura xxx)',
            'debit': 1000.0,
            'credit': 0.0
}])
lineas_asiento.append(
    [0, 0,
        {
           'account_id': banco,
           'partner_id': partner_id,
           'name': 'Pago de factura xxx',
           'debit': 0.0,
           'credit': 1000.0,
}])


# Values: (0, 0, { fields }) create
# (1, ID, { fields }) update (write fields to ID)
# (2, ID) remove (calls unlink on ID, that will also delete the relationship because of the ondelete)
# (3, ID) unlink (delete the relationship between the two objects but does not delete ID)
# (4, ID) link (add a relationship)
# (5, ID) unlink all
# (6, ?, ids) set a list of links

asiento_contable = {
    'ref': 'Pago a proveedor',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'journal_id': journal_id,
    'company_id': 1,  # en un entorno de una sola compañía está OK, caso contrario debería obtenerse el id de la compañía
    'line_ids': lineas_asiento,
}

new_record = models.execute_kw(
    db, uid, password, 'account.move', 'create',
    [asiento_contable],
)
# devuelve el id interno del nuevo asiento (5 en mi caso).
# el asiento queda en estado borrador.
# ver imagen en img/ref2.png

# este proximo, publica el asiento
models.execute_kw(db, uid, password, 'account.move', 'post', [new_record], res=True)
# este xmlrpc call, devuelve un None, y no está permitido por el servicio xmlrpc en Odoo. Hay un issue no resuelto
# de parte de odoo. Nosotros hemos hecho un commit que salva esta posibilidad cuando la localización para chile
# está instalada.
# el issue que se menciona es el siguiente: https://github.com/odoo/odoo/issues/29768
# ver imagen en img/ref3.png



