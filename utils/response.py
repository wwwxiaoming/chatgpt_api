from flask import jsonify;
def httpOk200(data = '', message = '成功'):
    return jsonify({
        "code":200,
        "message":message,
        "data":data
    })


def httpError400(message = '成功'):
    return jsonify({
        "code":400,
        "message":message,
        "data":''
    })

def httpError403(message = "拒绝访问"):
    return jsonify({
        "code": 403,
        "message": message,
        "data": ''
    })