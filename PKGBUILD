# Maintainer: Maxim Podlesnyj <cryptspirit at gmail.com>
pkgname=edna
pkgver=0.0.1
pkgrel=1
pkgdesc="Two panel file manager."

arch=('i686' 'x86_64')
url="https://github.com/cryptspirit/edna"
license=('GPL')
depends=('python2' 'findutils' 'gnome-icon-theme' 'pygtk')
makedepends=('python-distutils-extra' 'gettext' 'git')
md5sums=()

_gitroot="git://github.com/cryptspirit/edna.git"
_gitname="edna"

build() {
    cd ${srcdir}
    rm -rf edna 
    msg "Connecting to GIT server...."

    if [ -d edna ] ; then
        cd edna && git pull origin
        msg "The local files are updated."
    else
        git clone ${_gitroot}
    fi

    msg "GIT checkout done or server timeout"
    msg "Starting make..."
    
    cd ${srcdir}/edna
    cp edna edna~
    echo '#!'$(which python2) > edna
    grep -v '#!/' edna~ >> edna
    python2 setup.py install --prefix=${pkgdir}/usr clean --all
    mv edna~ edna
}
