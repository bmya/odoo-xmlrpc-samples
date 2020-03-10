from xmlrpc import client

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
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# busqueda de compañías
models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]])

# busqueda por RUT. Devuelve una lista de los ID de los partners que cumplen la condición
records = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['vat', '=', '76201224-3']]])
# devuelve [46, 47]

# busqueda por RUT combinado con compañías. Devuelve una lista de los ID de los partners que cumplen la condición
records = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['vat', '=', '76201224-3'], ['is_company', '=', True]]])
# devuelve [46]

objects = models.execute_kw(
    db, uid, password, 'res.partner', 'read', [records], {'fields': ['vat', 'name']})
# devuelve [{'id': 46, 'vat': '76201224-3', 'name': 'Blanco Martin & Asociados EIRL'}]

new_record = models.execute_kw(
    db, uid, password, 'res.partner', 'create', {
        'name': 'La Empresa S.A.',
        'vat': '71292734-1'
    }
)

records = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_company', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

for r in records:
    print(r)
# devuelve...
# {'id': 14, 'name': 'Azure Interior', 'country_id': [233, 'United States'], 'comment': False}
# {'id': 46, 'name': 'Blanco Martin & Asociados EIRL', 'country_id': [46, 'Chile'], 'comment': False}
# {'id': 10, 'name': 'Deco Addict', 'country_id': [233, 'United States'], 'comment': False}
# {'id': 11, 'name': 'Gemini Furniture', 'country_id': [233, 'United States'], 'comment': False}
# {'id': 15, 'name': 'Lumber Inc', 'country_id': [233, 'United States'], 'comment': False}

id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': "Partner", 'vat': '76201517-k'
}])
# devuelve el ID del partner (actualmente no controla si existe o no)

id = models.execute_kw(
    db, uid, password, 'res.partner', 'create',
    [
        {
            'name': "Partner3", 'vat': "76201517-1", 'country_id': country_id
        },
    ])
# esto devuelve un error, porque al detectar el país "Chile", valida el RUT y al ser incorrecto muestra el traceback:
# xmlrpc.client.Fault: <Fault 1: 'Traceback (most recent call last):\n  File
# "/mnt/odoo/odoo/addons/base/controllers/rpc.py", line 63, in xmlrpc_2\n
# response = self._xmlrpc(service)\n  File "/mnt/odoo/odoo/addons/base/controllers/rpc.py", line 43, in _xmlrpc\n
# result = dispatch_rpc(service, method, params)\n  File "/mnt/odoo/odoo/http.py", line 138, in dispatch_rpc\n
# result = dispatch(method, params)\n  File "/mnt/odoo/odoo/service/model.py", line 40, in dispatch\n
# res = fn(db, uid, *params)\n  File "/mnt/odoo/odoo/service/model.py", line 168, in execute_kw\n
# return execute(db, uid, obj, method, *args, **kw or {})\n  File "/mnt/odoo/odoo/service/model.py",
# line 93, in wrapper\n    return f(dbname, *args, **kwargs)\n  File "/mnt/odoo/odoo/service/model.py",
# line 175, in execute\n    res = execute_cr(cr, uid, obj, method, *args, **kw)\n  File
# "/mnt/odoo/odoo/service/model.py", line 164, in execute_cr\n
# return odoo.api.call_kw(recs, method, args, kw)\n  File "/mnt/odoo/odoo/api.py", line 385, in call_kw\n
# result = _call_kw_model_create(method, model, args, kwargs)\n  File "/mnt/odoo/odoo/api.py", line 365, in _
# call_kw_model_create\n    result = method(recs, *args, **kwargs)\n  File "<decorator-gen-238>",
# line 2, in create\n  File "/mnt/odoo/odoo/api.py", line 314, in _model_create_single\n
# return create(self, arg)\n  File "/mnt/odoo/addons/l10n_cl/models/res_partner.py", line 44, in create\n
# return super().create(values)\n  File "<decorator-gen-219>", line 2, in create\n  File "/mnt/odoo/odoo/api.py",
# line 314, in _model_create_single\n    return create(self, arg)\n
# File "/mnt/odoo/addons/base_vat/models/res_partner.py", line 477, in create\n
# return super(ResPartner, self).create(values)\n  File "<decorator-gen-198>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 335, in _model_create_multi\n    return create(self, [arg])\n
# File "/mnt/odoo/addons/account/models/partner.py", line 508, in create\n
# return super().create(vals_list)\n  File "<decorator-gen-132>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 336, in _model_create_multi\n    return create(self, arg)\n
# File "/mnt/odoo/addons/partner_autocomplete/models/res_partner.py", line 183, in create\n
# partners = super(ResPartner, self).create(vals_list)\n  File "<decorator-gen-79>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 336, in _model_create_multi\n    return create(self, arg)\n
# File "/mnt/odoo/odoo/addons/base/models/res_partner.py", line 544, in create\n
# partners = super(Partner, self).create(vals_list)\n  File "<decorator-gen-109>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 336, in _model_create_multi\n    return create(self, arg)\n
# File "/mnt/odoo/addons/mail/models/mail_thread.py", line 268, in create\n
# threads = super(MailThread, self).create(vals_list)\n  File "<decorator-gen-190>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 336, in _model_create_multi\n    return create(self, arg)\n
# File "/mnt/odoo/addons/website/models/mixins.py", line 151, in create\n
# records = super(WebsitePublishedMixin, self).create(vals_list)\n  File "<decorator-gen-3>", line 2, in create\n
# File "/mnt/odoo/odoo/api.py", line 336, in _model_create_multi\n    return create(self, arg)\n
# File "/mnt/odoo/odoo/models.py", line 3729, in create\n    records = self._create(data_list)\n
# File "/mnt/odoo/odoo/models.py", line 3882, in _create\n
# records._validate_fields(name for data in data_list for name in data[\'stored\'])\n
# File "/mnt/odoo/odoo/models.py", line 1167, in _validate_fields\n    check(self)\n
# File "/mnt/odoo/addons/l10n_latam_base/models/res_partner.py", line 22, in check_vat\n
# return super(ResPartner, with_vat).check_vat()\n  File "/mnt/odoo/addons/base_vat/models/res_partner.py",
# line 193, in check_vat\n    raise ValidationError(msg)\nodoo.exceptions.ValidationError: (\'\\n
# The VAT number [76201517-1] for partner [Partner3] does not seem to be valid. \\n
# Note: the expected format is CL76086428-5\', None)\n'>

# ejemplos de búsqueda de datos relacionales: esto permite obtener ID de datos que se requieren para ingresar
# correctamente un cliente o proveedor
country_id = models.execute_kw(
    db, uid, password, 'res.country', 'search', [[['name', '=', 'Chile']]])[0]
# devuelve 46
comuna_id = models.execute_kw(db, uid, password, 'res.city', 'search', [[['name', '=', 'Vitacura']]])[0]
# devuelve 342
latam_identification_type_id = models.execute_kw(db, uid, password, 'l10n_latam.identification.type', 'search', [[['name', '=', 'RUT']]])[0]
# es el id de nombre que se usa para el VAT en Chile (RUT) devuelve 4
l10n_cl_partner_activities_ids = models.execute_kw(db, uid, password, 'l10n_cl.partner.activities', 'search',
                                                   [[['code', 'in', ['662100', '662900']]]])
# devuelve los id interno de la base para esas actividades [768, 770]


# para la correcta alta de un cliente, se recomiendan como mínimo los siguientes campos:
partner_data = {
    'name': 'Empresa S.A.',
    'company_type': 'company',  # si es persona: 'person'
    'country_id': country_id,  # el valor de ID que se obtuvo de la consulta. Siempre será el mismo para la misma BDD
    'street': 'La Calle 1234',  # el dato de calle y número
    'street2': 'Piso 11 Oficina 1103',  # el dato adicional de la dirección
    'city_id': comuna_id,
    'vat': '76201517-K',  # RUT (debe ser válido como ya se vió)
    'l10n_latam_identification_type_id': latam_identification_type_id,  # RUT
    'l10n_cl_sii_taxpayer_type': '1',  # 1: iva afecto 1ra categoría (99,9%)
    'l10n_cl_dte_email': 'dte@ejemplo.com',  # email de intercambio
    'l10n_cl_activity_description': 'Compañía de Seguros',  # Giro
    'l10n_cl_partner_activities_ids': [[6, 0, l10n_cl_partner_activities_ids]],
}

id = models.execute_kw(db, uid, password, 'res.partner', 'create', [partner_data])
# crea el partner y devuelve el ID asignado

