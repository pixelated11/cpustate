# Maintainer: Andrew <itspixelatd@proton.me>
pkgname=cpustate
pkgver=0.1.0
pkgrel=1
pkgdesc="Persist CPU power settings (governor, EPP, ryzenadj) across boot and sleep"
arch=('any')
url="https://github.com/pixelated11/cpustate"
license=('GPL-3.0')
depends=('python')
optdepends=('ryzenadj: TDP and power limit control for AMD Ryzen laptops')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    pip install --no-deps --no-build-isolation --prefix=/usr --root="$pkgdir" .
}

package() {
    cd "$pkgname-$pkgver"

    # systemd service
    install -Dm644 systemd/cpustate.service \
        "$pkgdir/usr/lib/systemd/system/cpustate.service"

    # sleep hook
    install -Dm755 systemd/cpustate-sleep.sh \
        "$pkgdir/usr/lib/systemd/system-sleep/cpustate"

    # example config
    install -Dm644 config/cpustate.conf \
        "$pkgdir/etc/cpustate.conf"

    # license
    install -Dm644 LICENSE \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
