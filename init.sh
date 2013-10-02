export SECRET_KEY=$( cat secret.txt )
export DJANGO_SETTINGS_MODULE=bookmarks.settings.local
export PYTHONPATH=$PYTHONPATH:./bookmarks/bookmarks/
export ADMIN_USER=$( cat admin.txt )
source google.sh
source recaptcha.sh
