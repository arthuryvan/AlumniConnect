from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User , MentorRequest , Notification , Message , Opportunity ,Recommendation
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager(app)
login_manager.login_view = 'login'


app.secret_key = 'alumniconnect-secret-key'


app.config['UPLOAD_FOLDER'] = os.path.join(
    app.static_folder,
    'uploads'
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alumniconnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)


# Page d'accueil
@app.route('/')
def home():
    return render_template('index.html')


# À propos
@app.route('/about')
def about():
    return render_template('about.html')


# Alumni
@app.route('/alumni')
def alumni():
    return render_template('alumni.html')


# Mentorat
@app.route('/mentorat')
def mentorat():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    mentors = User.query.filter_by(role='alumni').all()

    return render_template(
        'mentorat.html',
        mentors=mentors
    )


@app.route('/accepter-mentorat/<int:demande_id>')
def accepter_mentorat(demande_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    demande = MentorRequest.query.get_or_404(demande_id)

    if demande.mentor_id != session['user_id']:
        return "Accès interdit", 403

    demande.status = 'accepte'

    notification = Notification(
        user_id=demande.student_id,
        message=f"{demande.mentor.nom} a accepté votre demande de mentorat."
    )

    db.session.add(notification)
    db.session.commit()

    flash("Demande de mentorat acceptée.")

    return redirect(url_for('demandes_mentorat'))



@app.route('/refuser-mentorat/<int:demande_id>')
def refuser_mentorat(demande_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    demande = MentorRequest.query.get_or_404(demande_id)

    if demande.mentor_id != session['user_id']:
        return "Accès interdit", 403

    demande.status = 'refuse'

    notification = Notification(
        user_id=demande.student_id,
        message=f"{demande.mentor.nom} a refusé votre demande de mentorat."
    )

    db.session.add(notification)
    db.session.commit()

    flash("Demande de mentorat refusée.")

    return redirect(url_for('demandes_mentorat'))




@app.route('/demande-mentorat/<int:mentor_id>')
def demande_mentorat(mentor_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Empêcher de se demander soi-même comme mentor
    if mentor_id == session['user_id']:
        flash("Vous ne pouvez pas vous demander vous-même comme mentor.")
        return redirect(url_for('mentorat'))

    mentor = User.query.get_or_404(mentor_id)

    # Vérifier que la personne est bien un Alumni
    if mentor.role != 'alumni':
        flash("Cette personne n'est pas disponible comme mentor.")
        return redirect(url_for('mentorat'))

    demande = MentorRequest(
        student_id=session['user_id'],
        mentor_id=mentor_id
    )

    db.session.add(demande)
    db.session.commit()

    flash("Demande de mentorat envoyée avec succès.")

    return redirect(url_for('mentorat'))


@app.route('/demandes-mentorat')
def demandes_mentorat():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    demandes = MentorRequest.query.filter_by(
        mentor_id=session['user_id']
    ).all()

    return render_template(
        'demandes_mentorat.html',
        demandes=demandes
    )


# Événements
@app.route('/evenements')
def evenements():
    return render_template('evenements.html')


# Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        

        # Rechercher l'utilisateur dans la base
        user = User.query.filter_by(email=email).first()

        # Vérifier l'utilisateur et le mot de passe
        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['user_nom'] = user.nom

            return redirect(url_for('dashboard'))

        else:
            return "Email ou mot de passe incorrect."

    return render_template('login.html')




# Dashboard
@app.route('/dashboard')
def dashboard():

    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return render_template('dashboard.html', user=user)


# Mon profil
@app.route('/profil', methods=['GET', 'POST'])
def profil():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':

        photo = request.files.get('photo')

        if photo and photo.filename:

            filename = secure_filename(photo.filename)

            photo_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            photo.save(photo_path)

            user.photo = filename

            db.session.commit()

            return redirect(url_for('profil'))

    return render_template('profil.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




# Inscription
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nom = request.form['nom']
        email = request.form['email']
        
        password = generate_password_hash(
            request.form['password']
        )

        role = request.form['role']
        filiere = request.form.get('filiere')
        promotion = request.form.get('promotion')
        entreprise = request.form.get('entreprise')
        bio = request.form.get('bio')

        # Vérifier si l'email existe déjà
        utilisateur_existant = User.query.filter_by(email=email).first()

        if utilisateur_existant:
            return "Cette adresse email est déjà utilisée."

        # Création de l'utilisateur
        nouvel_utilisateur = User(
            nom=nom,
            email=email,
            password=password,
            role=role,
            filiere=filiere,
            promotion=promotion,
            entreprise=entreprise,
            bio=bio
        )

        db.session.add(nouvel_utilisateur)
        db.session.commit()

        return "Inscription réussie !"

    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/historique-mentorat')
def historique_mentorat():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    historique = MentorRequest.query.filter_by(
        student_id=session['user_id']
    ).order_by(
        MentorRequest.date_creation.desc()
    ).all()

    return render_template(
        'historique_mentorat.html',
        historique=historique
    )



@app.route('/notifications')
def notifications():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    notifications = Notification.query.filter_by(
        user_id=session['user_id']
    ).order_by(
        Notification.date_creation.desc()
    ).all()

    return render_template(
        'notifications.html',
        notifications=notifications
    )



@app.route('/messagerie')
def messagerie_liste():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Récupérer les utilisateurs avec lesquels
    # l'utilisateur connecté a déjà échangé
    messages = Message.query.filter(
        (Message.sender_id == user_id) |
        (Message.receiver_id == user_id)
    ).order_by(
        Message.date_envoi.desc()
    ).all()

    utilisateurs = []

    for message in messages:

        if message.sender_id == user_id:
            autre_utilisateur = message.receiver
        else:
            autre_utilisateur = message.sender

        if autre_utilisateur not in utilisateurs:
            utilisateurs.append(autre_utilisateur)

    return render_template(
        'messagerie_liste.html',
        utilisateurs=utilisateurs
    )




@app.route('/messagerie/<int:user_id>')
def messagerie(user_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    utilisateur = User.query.get_or_404(user_id)

    messages = Message.query.filter(
        (
            (Message.sender_id == session['user_id']) &
            (Message.receiver_id == user_id)
        ) |
        (
            (Message.sender_id == user_id) &
            (Message.receiver_id == session['user_id'])
        )
    ).order_by(
        Message.date_envoi.asc()
    ).all()

    return render_template(
        'messagerie.html',
        utilisateur=utilisateur,
        messages=messages
    )


@socketio.on('send_message')
def handle_message(data):

    if 'user_id' not in session:
        return

    sender_id = session['user_id']
    receiver_id = int(data['receiver_id'])

    contenu = data['contenu'].strip()

    if not contenu:
        return

    # Vérifier que le destinataire existe
    receiver = User.query.get(receiver_id)

    if not receiver:
        return

    # Créer le message
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        contenu=contenu
    )

    db.session.add(message)
    db.session.commit()

    # Room privée
    room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"

    message_data = {
        'id': message.id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'contenu': message.contenu,
        'date': message.date_envoi.strftime('%H:%M')
    }

    # Envoyer uniquement aux deux personnes
    emit(
        'new_message',
        message_data,
        to=room
    )


@socketio.on('join_chat')
def join_chat(data):

    if 'user_id' not in session:
        return

    user_id = session['user_id']
    other_user_id = int(data['other_user_id'])

    # Créer une room unique pour les deux utilisateurs
    room = f"chat_{min(user_id, other_user_id)}_{max(user_id, other_user_id)}"

    join_room(room)



# Opportunités
@app.route('/opportunites')
def opportunites():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    offres = Opportunity.query.order_by(
        Opportunity.date_publication.desc()
    ).all()

    return render_template(
        'opportunites.html',
        offres=offres
    )


@app.route(
    '/recommander/<int:student_id>',
    methods=['GET', 'POST']
)
def recommander(student_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    alumni = User.query.get(session['user_id'])

    if alumni.role != 'alumni':
        return "Accès interdit", 403

    etudiant = User.query.get_or_404(student_id)

    if request.method == 'POST':

        message = request.form['message']

        recommendation = Recommendation(
            alumni_id=alumni.id,
            student_id=etudiant.id,
            message=message
        )

        db.session.add(recommendation)

        notification = Notification(
            user_id=etudiant.id,
            message=f"{alumni.nom} vous a recommandé."
        )

        db.session.add(notification)

        db.session.commit()

        flash("Recommandation envoyée.")

        return redirect(url_for('etudiants'))

    return render_template(
        'recommander.html',
        etudiant=etudiant
    )


@app.route('/etudiants')
def etudiants():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    liste = User.query.filter_by(
        role='student'
    ).all()

    return render_template(
        'etudiants.html',
        etudiants=liste
    )




with app.app_context():
    db.create_all()


if __name__ == '__main__':
    socketio.run(app, debug=True)