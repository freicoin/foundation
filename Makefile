#
# Copyright © 2013 by its contributors. See AUTHORS for details.
#

ROOT=$(shell pwd)
CACHE_ROOT=${ROOT}/.cache
PYENV=${ROOT}/.pyenv
RBENV=${ROOT}/.rbenv
CONF=${ROOT}/conf
APP_NAME=foundation
PACKAGE=foundation

-include Makefile.local

.PHONY: all
all: python ruby secret-keys dbvm

.PHONY: python
python: ${PYENV}/.stamp-h

.PHONY: ruby
ruby: ${RBENV}/.stamp-h

.PHONY: secret-keys
secret-keys: ${ROOT}/${PACKAGE}/settings/secret_keys.py

.PHONY: check
check: all
	mkdir -p "${ROOT}"/build/report
	"${PYENV}"/bin/python -Wall "${ROOT}"/manage.py test \
	    --settings=${PACKAGE}.settings.testing \
	    --with-xunit \
	    --xunit-file="${ROOT}"/build/report/xunit.xml \
	    --with-xcoverage \
	    --xcoverage-file="${ROOT}"/build/report/coverage.xml \
	    --cover-package=${PACKAGE} \
	    --cover-package=apps \
	    --cover-package=xunit \
	    --cover-erase \
	    --cover-tests \
	    --cover-inclusive \
	    --all-modules -v2 \
	    ${PACKAGE} apps xunit

.PHONY: shell
shell: all db
	"${PYENV}"/bin/python "${ROOT}"/manage.py shell_plusplus \
	    --settings=${PACKAGE}.settings.development \
	    --print-sql \
	    --ipython

.PHONY: run
run: all db
	bash -c "source '${PYENV}'/bin/activate && \
	    RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv exec bundle exec \
	        foreman start --port=8000 --root="${ROOT}" \
	                      --procfile "${CONF}"/Procfile.development"

.PHONY: run
run_production: all db
	bash -c "source '${PYENV}'/bin/activate && \
	    RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv exec bundle exec \
	        foreman start --port=8000 --root="${ROOT}" \
	                      --procfile "${ROOT}"/Procfile"

.PHONY: mostlyclean
mostlyclean:
	-rm -rf dist
	-rm -rf build
	-rm -rf .coverage

.PHONY: clean
clean: mostlyclean
	-rm -f .rbenv-version
	-rm -rf "${RBENV}"
	-rm -rf "${PYENV}"

.PHONY: distclean
distclean: clean
	-rm -rf "${CONF}"/cookbooks "${CONF}"/tmp
	-rm -rf "${CACHE_ROOT}"
	-rm -rf Makefile.local

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

# ===----------------------------------------------------------------------===

${ROOT}/${PACKAGE}/settings/secret_keys.py:
	@echo  >"${ROOT}/${PACKAGE}"/settings/secret_keys.py '# -*- coding: utf-8 -*-'
	@echo >>"${ROOT}/${PACKAGE}"/settings/secret_keys.py \
	    "SECRET_KEY='`LC_CTYPE=C < /dev/urandom tr -dc A-Za-z0-9_ | head -c24`'"

# ===--------------------------------------------------------------------===

.PHONY: db
db: all
	"${PYENV}"/bin/python "${ROOT}"/manage.py syncdb \
	    --settings=${PACKAGE}.settings.development
	"${PYENV}"/bin/python "${ROOT}"/manage.py migrate \
	    --settings=${PACKAGE}.settings.development
	
	# The static directory is where Django accumulates
	# staticfiles. It needs to be present (even if empty), or else
	# errors will be thrown when we try to collect the static files
	# to it.
	mkdir -p "${ROOT}"/staticfiles
	bash -c "source '${PYENV}'/bin/activate && \
	    python '${ROOT}'/manage.py collectstatic --noinput"

.PHONY: dbdestroy
dbdestroy:
	"${PYENV}"/bin/python "${ROOT}"/manage.py reset_db --router=default \
	    --settings=${PACKAGE}.settings.development

.PHONY: dbshell
dbshell: db
	"${PYENV}"/bin/python "${ROOT}"/manage.py dbshell \
	    --settings=${PACKAGE}.settings.development

# ===--------------------------------------------------------------------===

.PHONY: dbvm
dbvm:
	bash -c "cd '${ROOT}'/conf && vagrant up"
	PGPASSWORD=password psql -h localhost -p 14389 -U django_login django_db -c "SELECT 1;" || \
	    bash -c "cd '${ROOT}'/conf && vagrant reload"

.PHONY: dbssh
dbssh: db
	bash -c "cd '${ROOT}'/conf && vagrant ssh postgres"

# ===--------------------------------------------------------------------===

${CACHE_ROOT}/virtualenv/virtualenv-1.10.tar.gz:
	mkdir -p "${CACHE_ROOT}"/virtualenv
	curl -L 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.tar.gz' >'$@'

${PYENV}/.stamp-h: ${ROOT}/requirements.txt ${CONF}/requirements*.txt ${CACHE_ROOT}/virtualenv/virtualenv-1.10.tar.gz
	# Because build and run-time dependencies are not thoroughly
	# tracked, it is entirely possible that rebuilding the
	# development environment on top of an existing one could
	# result in a broken build. For the sake of consistency and
	# preventing unnecessary, difficult-to-debug problems, the
	# entire development environment is rebuilt from scratch
	# everytime this make target is selected.
	-rm -rf "${PYENV}"
	
	# The ${PYENV} directory, if it exists, was removed above. The
	# PyPI cache is nonexistant if this is a freshly checked-out
	# repository, or if the `distclean` target has been run.  This
	# might cause problems with build scripts executed later which
	# assume their existence, so they are created now if they don't
	# already exist.
	mkdir -p "${PYENV}"
	mkdir -p "${CACHE_ROOT}"/pypi
	
	# virtualenv is used to create a separate Python installation
	# for this project in ${PYENV}.
	tar \
	    -C "${CACHE_ROOT}"/virtualenv --gzip \
	    -xf "${CACHE_ROOT}"/virtualenv/virtualenv-1.10.tar.gz
	python "${CACHE_ROOT}"/virtualenv/virtualenv-1.10/virtualenv.py \
	    --clear \
	    --distribute \
	    --never-download \
	    --prompt="(${APP_NAME}) " \
	    "${PYENV}"
	-rm -rf "${CACHE_ROOT}"/virtualenv/virtualenv-1.10
	
	# readline is installed here to get around a bug on Mac OS X
	# which is causing readline to not build properly if installed
	# from pip, and the fact that a different package must be used
	# to support it on Windows/Cygwin.
	if [ "x`uname -o`" = "xCygwin" ]; then \
	    "${PYENV}"/bin/pip install pyreadline; \
	else \
	    "${PYENV}"/bin/easy_install readline; \
	fi
	
	# pip is used to install Python dependencies for this project.
	for reqfile in "${ROOT}"/requirements.txt \
	               "${CONF}"/requirements*.txt; do \
	    CFLAGS=-I/opt/local/include LDFLAGS=-L/opt/local/lib \
	    "${PYENV}"/bin/python "${PYENV}"/bin/pip install \
	        --download-cache="${CACHE_ROOT}"/pypi \
	        -r "$$reqfile"; \
	done
	
	# All done!
	touch "${PYENV}"/.stamp-h

# ===----------------------------------------------------------------------===

${CACHE_ROOT}/rbenv/rbenv-0.4.0.tar.gz:
	mkdir -p ${CACHE_ROOT}/rbenv
	curl -L 'https://codeload.github.com/sstephenson/rbenv/tar.gz/v0.4.0' >'$@'

${CACHE_ROOT}/rbenv/ruby-build-20130628.tar.gz:
	mkdir -p ${CACHE_ROOT}/rbenv
	curl -L 'https://codeload.github.com/sstephenson/ruby-build/tar.gz/v20130628' >'$@'

${RBENV}/.stamp-h: ${CACHE_ROOT}/rbenv/rbenv-0.4.0.tar.gz ${CACHE_ROOT}/rbenv/ruby-build-20130628.tar.gz
	# Because build and run-time dependencies are not thoroughly
	# tracked, it is entirely possible that rebuilding the
	# development environment on top of an existing one could
	# result in a broken build. For the sake of consistency and
	# preventing unnecessary, difficult-to-debug problems, the
	# entire development environment is rebuilt from scratch
	# everytime this make target is selected.
	-rm -rf "${RBENV}"
	mkdir -p "${RBENV}"
	
	# rbenv (and its plugins, ruby-build and rbenv-gemset) is used to build,
	# install, and manage ruby environments:
	tar \
	    -C "${RBENV}" --strip-components 1 --gzip \
	    -xf "${CACHE_ROOT}"/rbenv/rbenv-0.4.0.tar.gz
	mkdir -p "${RBENV}"/plugins/ruby-build
	tar \
	    -C "${RBENV}"/plugins/ruby-build --strip-components 1 --gzip \
	    -xf "${CACHE_ROOT}"/rbenv/ruby-build-20130628.tar.gz
	
	# Trigger a build and install of our required ruby version:
	- CONFIGURE_OPTS=--with-openssl-dir=$(shell which openssl | sed -e s:/bin/openssl::) \
	  RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv install 1.9.3-p448
	- RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv rehash
	echo 1.9.3-p448 >.rbenv-version
	
	# Install bundler & gemset dependencies:
	RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv exec gem install bundler
	- RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv rehash
	RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv exec bundle install
	- RBENV_ROOT="${RBENV}" "${RBENV}"/bin/rbenv rehash
	
	# Fetch Chef cookbooks
	bash -c "cd '${ROOT}'/conf && \
	    RBENV_ROOT='${RBENV}' '${RBENV}'/bin/rbenv exec bundle exec \
	        librarian-chef install"
	
	# All done!
	touch "${RBENV}"/.stamp-h

#
# End of File
#
