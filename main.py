from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
import full_code
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)
##WTForm

#home
@app.route('/')
def get_all_posts():
    result = full_code.get_home()
    return render_template("index.html", result=result)


# Code from previous day
@app.route("/address_list", methods=['GET', 'POST'])
def address_list():
    if request.method == 'POST':
        list = request.form.get("list")
        data = request.form.get("data")
        ip_list = full_code.generate_ip_list(list=list,input_data=data)
        return render_template('address_list.html', answer=ip_list)
    else:
        return render_template('address_list.html', answer=None, destination=None)

@app.route("/dns_lookup", methods=['GET', 'POST'])
def dns_lookup():
    if request.method == 'POST':
        start_ip = request.form.get("domain_name")
        type= request.form.get("record")
        record = full_code.find_dns(start_ip, type)
        return render_template('dns_lookup.html', answer=record, record=type)
    else:
        return render_template('dns_lookup.html', answer=None, destination=None)

@app.route("/ping-trace", methods=['GET', 'POST'] )
def ping_trace():
    if request.method == 'POST':
        function = request.form.get('function')
        host1 = request.form.get("host")
        if function == "ping":
            answer = full_code.ping(host1)
            return render_template("ping_trace.html", answer=answer, function=function)
        else:
            answer = full_code.traceroute(host1).to_html(classes='table', border=0)
            return render_template("ping_trace.html", answer= answer, function=None)
    return render_template("ping_trace.html", answer= None, function=None)

@app.route('/ptr-generator', methods=['GET', 'POST'])
def ptr_generator():
    if request.method == 'POST':
        ip_address = request.form.get('ip_address')
        prefix = int((request.form.get("prefix").split("/"))[1])
        # Generate the DNS zone file
        dns_config = full_code.generate_dns_zone(ip_address, prefix)
        # Save the DNS zone file
        with open('dns_zone.txt', 'w') as file:
            file.write(dns_config)

        file_url = '/dns_zone.txt'  # Set the file URL for download

        return render_template('ptr_generator.html', file_url=file_url)
    return render_template('ptr_generator.html', file_url=None)

@app.route("/whoislookup", methods=['GET', 'POST'])
def get_domain_profile():
    if request.method == 'POST':
        domain_name = request.form.get("domain")
        domain_profile = full_code.get_domain_profile(domain_name)
        return render_template('whoislookup.html', domain_info=domain_profile)
    else:
        return render_template('whoislookup.html', domain_info=None)

@app.route('/dns_zone.txt')
def download_dns_zone():
    return send_file('dns_zone.txt', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=4984)
