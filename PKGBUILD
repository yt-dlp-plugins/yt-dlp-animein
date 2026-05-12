# Maintainer: asepsukasusunirvatia <asepdev.git@gmail.com>
pkgname=yt-dlp-animein-git
pkgver=r44.de1b0c9
pkgrel=1
epoch=1
pkgdesc='yt-dlp extractor for animeinweb.com'
url='https://github.com/yt-dlp-plugins/yt-dlp-animein'
arch=('any')
license=('GPL-3.0-or-later')
depends=('python' 'yt-dlp')
makedepends=('python-build' 'python-hatchling' 'python-installer' 'python-wheel' 'git')
source=("${pkgname}::git+${url}.git")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}/${pkgname}"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build(){
    cd "${srcdir}/${pkgname}"
    python -m build --wheel --no-isolation
}

package(){
    cd "${srcdir}/${pkgname}"
    python -m installer --destdir="${pkgdir}" dist/*.whl
    install -Dvm 644 'LICENSE' "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
