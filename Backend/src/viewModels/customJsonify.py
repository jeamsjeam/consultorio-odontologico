from flask import jsonify

def CustomJsonify(data, single_schema=None, list_schema=None):
    # Si el dato es None, retorna null
    if data is None:
        return jsonify(None)
    # Si el dato es una lista vacía, retorna []
    elif isinstance(data, list) and not data:
        return jsonify([])
    # Si el dato es una lista con elementos, usa el esquema de lista si está disponible
    elif isinstance(data, list):
        if list_schema:
            return jsonify(list_schema.dump(data))
        return jsonify(data)
    # Si el dato es un objeto, usa el esquema individual si está disponible
    elif hasattr(data, '__dict__') or isinstance(data, dict):
        if single_schema:
            return jsonify(single_schema.dump(data))
        return jsonify(data)
    # Si es un valor base (booleano, string, número), retorna el valor directamente
    else:
        return jsonify(data)