from app import app, db 
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm, ProfileForm
from app.models import Comic, Com_Profile 
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    profiles = Com_Profile.query.all()
    return render_template('index.html', profiles=profiles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form validated!')
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        print(full_name, email, password)
        check_comic = db.session.execute(db.select(Comic).filter(Comic.email == email)).scalars().all()
        if check_comic:
            flash('A comic with that email already exists!', 'warning')
            return redirect(url_for('signup'))
        new_comic = Comic(full_name=full_name, email=email, password=password)
        flash(f'Thank you {new_comic.full_name} for signing up! Please Log In!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form validated!')
        email = form.email.data 
        password = form.password.data
        print(email, password)
        comic = Comic.query.filter_by(email=email).first()
        if comic is not None and comic.check_password(password):
            login_user(comic)
            flash(f'HAHA! You have succesfully logged in as {email}! Please create a profile!', 'success')
            return redirect(url_for('index'))
        else: 
            flash(f'Invlaid username and/or password. Please try again, stupid!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!', 'primary')
    return redirect(url_for('index'))


@app.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        print('Form validated!')
        username = form.username.data 
        location = form.location.data 
        about_me = form.about_me.data
        image_url = form.image_url.data or None
        twitter_url = form.twitter_url.data or None 
        instagram_url = form.instagram_url.data or None 
        facebook_url = form.facebook_url.data or None 
        tiktok_url = form.tiktok_url.data or None 
        youtube_url = form.youtube_url.data or None 
        print(username, location, about_me, image_url, twitter_url, instagram_url, facebook_url, tiktok_url, youtube_url)
        check_profile = db.session.execute(db.select(Com_Profile).filter(Com_Profile.username == username)).scalars().all()
        if check_profile:
            flash('A profile for that username already exists!', 'warning')
            return redirect(url_for('create_profile'))
        new_profile = Com_Profile(username=username, location=location, about_me=about_me, image_url=image_url, twitter_url=twitter_url, instagram_url=instagram_url, facebook_url=facebook_url, tiktok_url=tiktok_url, youtube_url=youtube_url, comic_id=current_user.id)
        flash(f'Thank you {new_profile.username} for creating a profile!', 'success')
        return redirect(url_for('index'))
    return render_template('create_profile.html', form=form)

@app.route('/edit_profile/<profile_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(profile_id):
    form = ProfileForm()
    profile_to_edit = Com_Profile.query.get_or_404(profile_id)
    if profile_to_edit.comic != current_user:
        flash('You do not have permission to edit this profile', 'danger')
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        profile_to_edit.location = form.location.data
        profile_to_edit.about_me = form.about_me.data
        profile_to_edit.image_url = form.image_url.data
        profile_to_edit.twitter_url = form.twitter_url.data
        profile_to_edit.instagram_url= form.instagram_url.data
        profile_to_edit.facebook_url = form.facebook_url.data
        profile_to_edit.tiktok_url = form.tiktok_url.data
        profile_to_edit.youtube_url = form.youtube_url.data
        db.session.commit()
        flash('This profile has been updated!', 'success')
        return redirect(url_for('index'))
    
    form.location.data = profile_to_edit.location
    form.about_me.data = profile_to_edit.about_me
    form.image_url.data = profile_to_edit.image_url
    form.twitter_url = profile_to_edit.twitter_url
    form.instagram_url = profile_to_edit.instagram_url
    form.facebook_url = profile_to_edit.facebook_url 
    form.tiktok_url = profile_to_edit.tiktok_url 
    form.youtube_url = profile_to_edit.youtube_url 
    return render_template('edit_profile.html', form=form, profile=profile_to_edit)