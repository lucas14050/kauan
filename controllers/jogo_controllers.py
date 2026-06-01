from models.jogo_models import Jogo 
from db import db 
import json
from flask import make_response, request
from flask import jsonify


def get_jogos():
    jogos = Jogo.query.all()  
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de jogos.',
            'dados': [jogo.json() for jogo in jogos]  
        }, ensure_ascii=False, sort_keys=False) 
    )
    response.headers['Content-Type'] = 'application/json'  
    return response


def get_jogo_by_id(jogo_id):
    jogo = Jogo.query.get(jogo_id)  

    if jogo:  
        response = make_response(
            json.dumps({
                'mensagem': 'Jogo encontrado.',
                'dados': jogo.json()  
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'   
        return response
    else:
        
        response = make_response(
            json.dumps({'mensagem': 'Jogo não encontrado.', 'dados': {}}, ensure_ascii=False),
            404 
        )
        response.headers['Content-Type'] = 'application/json' 
        return response


def create_jogo(jogo_data):
    
    if not all(key in jogo_data for key in ['titulo', 'genero', 'desenvolvedor', 'plataforma']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Titulo, genero, desenvlvedor e plataforma são obrigatórios.'}, ensure_ascii=False),
            400  
        )
        response.headers['Content-Type'] = 'application/json' 
        return response
    
    
    novo_jogo = Jogo(
        titulo=jogo_data['titulo'],
        genero=jogo_data['genero'],
        desenvolvedor=jogo_data['desenvolvedor'],
        plataforma=jogo_data['plataforma']
    )
    
    db.session.add(novo_jogo)  
    db.session.commit() 

    
    response = make_response(
        json.dumps({
            'mensagem': 'Jogo cadastrado com sucesso.',
            'jogo': novo_jogo.json() 
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  
    return response

def update_jogo(jogo_id, jogo_data):
    jogo = Jogo.query.get(jogo_id)  

    if not jogo: 
        response = make_response(
            json.dumps({'mensagem': 'Jogo não encontrado.'}, ensure_ascii=False),
            404  
        )
        response.headers['Content-Type'] = 'application/json'   
        return response

    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in jogo_data for key in ['titulo', 'genero', 'desenvolvedor', 'plataforma']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Titulo, genero, desenvolvedor e plataforma são obrigatórios.'}, ensure_ascii=False),
            400 
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    
    jogo.titulo = jogo_data['titulo']
    jogo.genero = jogo_data['genero']
    jogo.desenvolvedor = jogo_data['desenvolvedor']
    jogo.plataforma = jogo_data['plataforma']

    db.session.commit()

    
    response = make_response(
        json.dumps({
            'mensagem': 'Jogo atualizado com sucesso.',
            'jogo': jogo.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  
    return response

def delete_jogo(jogo_id):
    jogo = Jogo.query.get(jogo_id)

    if not jogo:
        return jsonify({'erro': 'Jogo não encontrado'}), 404

    db.session.delete(jogo)
    db.session.commit()

    return jsonify({'mensagem': 'Jogo deletado com sucesso'}), 200