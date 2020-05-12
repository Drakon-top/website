# -*- coding: utf-8 -*-


import flask
from flask import jsonify
from data.clas import Reviews
from data import db_session

blueprint = flask.Blueprint('reviews_api', __name__, 
                            template_folder='templates')


@blueprint.route('/api/reviews_all')
def get_reviews_all():
    session = db_session.create_session()
    reviews = session.query(Reviews).all()
    return flask.jsonify(
        {'reviews': 
         [item.to_dict(only=('id', 'name', 'estimation', 'plus', 'minus', 'content', 
              'created_date', 'user_id'))
        for item in reviews]})


@blueprint.route('/api/good_reviews/<reviews_estimation>')
def get_good_reviews(reviews_estimation):
    session = db_session.create_session()
    reviews = session.query(Reviews).filter(Reviews.estimation >= reviews_estimation)
    if not reviews:
        return jsonify({'error': 'Not found'})    
    return flask.jsonify(
        {'reviews': 
         [item.to_dict(only=('id', 'name', 'estimation', 'plus', 'minus', 'content', 
              'created_date', 'user_id'))
        for item in reviews]})


@blueprint.route('/api/name_reviews/<name>')
def get_name_reviews(name):
    session = db_session.create_session()
    reviews = session.query(Reviews).filter(Reviews.name == name)
    if not reviews:
        return jsonify({'error': 'Not found'})    
    return flask.jsonify(
        {'reviews': 
         [item.to_dict(only=('id', 'name', 'estimation', 'plus', 'minus', 'content', 
              'created_date', 'user_id'))
        for item in reviews]})