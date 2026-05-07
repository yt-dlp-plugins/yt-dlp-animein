# Maintainer: asepsukasusunirvatia <asepdev.git@gmail.com>
pkgname=yt-dlp-animein
pkgver=2.2.9
pkgrel=1
pkgdesc='yt-dlp extractor for animeinweb.com'
url='https://github.com/asepsukasusunirvatia/yt-dlp-animein'
arch=('any')
license=('GPL-3.0-or-later')
depends=('python' 'yt-dlp')
makedepends=('python-build' 'python-hatchling' 'python-installer')
# source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/refs/tags/v${pkgver}.tar.gz")
source=()
sha256sums=()

build(){
    cd "${startdir}"
    python -m build --wheel --no-isolation
}

package(){
    cd "${startdir}"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
