from flask import Flask, render_template, request, jsonify, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# 假设有一些桌子
tables = ["1", "2", "3", "4", "5"]


@app.route('/')
def index():
    # 为每个桌子生成二维码
    table_qr_codes = {}
    for table in tables:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # 这里把桌号作为参数传递给URL
        qr_data = url_for('order', table_id=table, _external=True)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        table_qr_codes[table] = img_str

    return render_template('scan.html', table_qr_codes=table_qr_codes)


@app.route('/order/<table_id>')
def order(table_id):
    # 这里你可以添加更多逻辑，比如显示菜单，处理订单等
    # 现在我们只是显示桌号
    return render_template('order.html', table_id=table_id)


if __name__ == '__main__':
    app.run(debug=True)


