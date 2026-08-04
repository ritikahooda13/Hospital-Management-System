from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hms_secure_secret_key'

# In-memory storage lists for complete hospital management
patients = []
doctors = []
appointments = []
billing = []
prescriptions = []

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', 
                           patients=len(patients), 
                           doctors=len(doctors), 
                           appointments=len(appointments),
                           billing=len(billing))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').lower()
    filtered_patients = patients
    
    if search_query:
        filtered_patients = [p for p in patients if search_query in p['name'].lower() or search_query in p['phone']]

    if request.method == 'POST':
        patient = {
            'id': len(patients) + 1,
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'phone': request.form['phone'],
            'medical_history': request.form['medical_history'],
            'registration_date': datetime.now().strftime("%Y-%m-%d")
        }
        patients.append(patient)
        return redirect(url_for('manage_patients'))
        
    return render_template('patients.html', patients=filtered_patients, search=search_query)

@app.route('/doctors', methods=['GET', 'POST'])
def manage_doctors():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        doctor = {
            'id': len(doctors) + 1,
            'name': request.form['name'],
            'specialization': request.form['specialization'],
            'phone': request.form['phone']
        }
        doctors.append(doctor)
        return redirect(url_for('manage_doctors'))
    return render_template('doctors.html', doctors=doctors)

@app.route('/appointments', methods=['GET', 'POST'])
def manage_appointments():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        p_id = int(request.form['patient_id'])
        d_id = int(request.form['doctor_id'])
        
        patient_name = next((p['name'] for p in patients if p['id'] == p_id), "Unknown")
        doctor_name = next((d['name'] for d in doctors if d['id'] == d_id), "Unknown")

        appointment = {
            'id': len(appointments) + 1,
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'appointment_date': request.form['appointment_date'],
            'status': 'Confirmed'
        }
        appointments.append(appointment)
        return redirect(url_for('manage_appointments'))
    return render_template('appointments.html', appointments=appointments, patients=patients, doctors=doctors)

@app.route('/billing', methods=['GET', 'POST'])
def manage_billing():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        p_id = int(request.form['patient_id'])
        patient_name = next((p['name'] for p in patients if p['id'] == p_id), "Unknown")

        bill = {
            'id': len(billing) + 1,
            'patient_name': patient_name,
            'amount': request.form['amount'],
            'status': 'Paid',
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        billing.append(bill)
        return redirect(url_for('manage_billing'))
    return render_template('billing.html', billing=billing, patients=patients)

@app.route('/prescriptions', methods=['GET', 'POST'])
def manage_prescriptions():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        p_id = int(request.form['patient_id'])
        patient_name = next((p['name'] for p in patients if p['id'] == p_id), "Unknown")

        prescription = {
            'id': len(prescriptions) + 1,
            'patient_name': patient_name,
            'medicine': request.form['medicine'],
            'dosage': request.form['dosage'],
            'instructions': request.form['instructions'],
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        prescriptions.append(prescription)
        return redirect(url_for('manage_prescriptions'))
    return render_template('prescriptions.html', prescriptions=prescriptions, patients=patients)

if __name__ == '__main__':
    app.run(debug=True, port=5002)