from __future__ import unicode_literals
import youtube_dl
import logging
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, current_app
from flask_wtf import Form
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
from flask_login import current_user
from subprocess import call
from multitool.mp3converter.forms import Song_Url
# from multitool.mp3converter.utils import 

mp3converter = Blueprint('mp3converter', __name__)
logging.basicConfig(filename='multitool.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger('Multitool')

class Converter_Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    logger.info(status)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


@mp3converter.route("/convert", methods=['POST', 'GET'])
def convert():
    form = Song_Url()
    song_urls = []
    if form.validate():
        if current_user.is_authenticated:
            if form.validate():
                if not form.download_file_path.data:
                    form.download_file_path.data = current_app.config['DOWNLOAD_FILE_LOCATION'] + '/%(title)s.%(ext)s'

                if form.url_string.data:
                    song_urls.append(form.url_string.data)

                ydl_opts = {
                    'outtmpl': form.download_file_path.data,
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'logger': Converter_Logger(),
                    'progress_hooks': [my_hook],
                }

                if song_urls:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(song_urls)
                    flash('Song Converted!', 'success')
        else:
            flash('User not authenticated', 'danger')
        form = Song_Url()
        return render_template('mp3converter.html', form=form, title='MP3 Converter')
    return render_template('mp3converter.html', form=form, title='MP3 Converter')
    