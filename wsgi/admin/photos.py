# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, abort, url_for, session, current_app, flash, request
from flask import send_from_directory
from models import Photo
import os
from decorators import login_required
from pagination import Pagination
from uploads import get_saved_filename
from exiv2 import reset_orientation, get_image_exif, get_image_date

bp = Blueprint('photos', __name__)


@bp.route("/", defaults={'page': 1})
@bp.route("/page/<int:page>")
@login_required
def index(page):
    file_per_page = current_app.config.get('FILE_PER_PAGE', 10)
    photos_count = Photo.query.count()
    photos = Photo.query.offset((page - 1) * file_per_page).limit(file_per_page)
    for photo in photos:
        photo.url = url_for(".show_photo", filename=photo.filename)

    pagination = Pagination(page, file_per_page, photos_count)
    return render_template("admin/photos.html", photos=photos, page=page, pagination=pagination)


@bp.route('/file/<filename>')
def show_photo(filename):
    saved_filename = get_saved_filename(filename)
    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename)):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], saved_filename, as_attachment=False)


@bp.route('/file/<filename>/exif')
def reset_exif_photo(filename):
    saved_filename = get_saved_filename(filename)
    exif_info = get_image_exif(saved_filename=saved_filename, filepath=current_app.config['UPLOAD_FOLDER'])
    # reset_orientation(saved_filename=saved_filename, filepath=current_app.config['UPLOAD_FOLDER'])
    return exif_info


@bp.route('/file/<filename>/date')
def show_photo_date(filename):
    saved_filename = get_saved_filename(filename)
    image_date = get_image_date(saved_filename=saved_filename, filepath=current_app.config['UPLOAD_FOLDER'])
    return image_date
