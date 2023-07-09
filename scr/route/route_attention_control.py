from flask import Blueprint, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import redirect

from scr.models.model_Attention_Control import model_Attention_Control
from scr.models.entities.Attention_Control import Attention_Control

main = Blueprint('attention_ctrl_bp', __name__)


# Select
@main.route('/')
def Index():
    # Obtener los parametros de paginación de la URL actual
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # Obtener datos  para la tabla
    attentions = model_Attention_Control.get_attention_control_list_ver2()

    data = []
    # convertir los obj. a una lista de diccionario
    for attention in attentions:
        attention_dict = {
            'id': attention.id,
            'fecha': attention.fecha,
            'nombres': attention.nombres,
            'hora_ingreso': attention.hora_ingreso,
            'hora_salida': attention.hora_salida,
            'polo_gift': attention.polo_gift,
            'keychain_gift': attention.keychain_gift,
            'catalog_book': attention.catalog_book,
        }
        data.append(attention_dict)
        # calcular el numero total de elementos y la lista de elementos para la pag. actual.
        total = len(data)
        paginated_data = attentions[offset: offset + per_page]
        # Crear objeto Pagination
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
        # data = model_Attention_Control.get_attention_control_list()

    return render_template('index.html', attentions=paginated_data, pagination=pagination)


# insert
@main.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":

        fecha = request.form['fecha']
        nombres = request.form['nombres']
        hora_ingreso = request.form['hora_ingreso']
        hora_salida = request.form['hora_salida']
        estado_polo = request.form.get('polo_gift', False)

        if estado_polo == 'on':
            estado_polo = True
        else:
            estado_polo = False

        estado_keychain = request.form.get('keychain_gift', False)

        if estado_keychain == 'on':
            estado_keychain = True
        else:
            estado_keychain = False

        catalog_book = request.form['catalog_book']

        attention_control_model = Attention_Control(fecha, nombres, hora_ingreso, hora_salida, estado_polo,
                                                    estado_keychain, catalog_book)

        affected_rows =model_Attention_Control.add_attention_control(attention_control_model)

        if affected_rows ==1:
            print('Registrado')
        else:
            print('No registado')
            # redirect= funcion que redirige a una URL  especifica.
            #url_for =  funcion que genera la URL para una ruta especifica en función de su nombre.
            # attention_ctrl_bp nombre  de la ruta a la que se va a redirigir.
        return redirect(url_for('attention_ctrl_bp.Index'))

# update
@main.route('/update', methods=['POST'])
def update():
    return render_template('index.html')


# delete
@main.route('/delete/<string:id>')
def delete(id):
    return render_template('index.html')
