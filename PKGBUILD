# Maintainer: Your Name <your.email@example.com>
pkgname=magicpods
pkgver=2.0.4
pkgrel=1
pkgdesc="A command-line utility for managing AirPods, Beats, and Galaxy Buds on Linux"
arch=('x86_64')
url="https://github.com/steam3d/MagicPodsCore"
license=('unknown')
depends=('bluez' 'python')
makedepends=('cmake' 'gcc' 'git')
backup=('etc/magicpods/magicpods.conf')
source=()
sha256sums=()

build() {
    cd "${srcdir}/.."
    
    # Build MagicPodsCore
    if [ -d "build" ]; then
        rm -rf build
    fi
    
    mkdir -p build
    cd build
    
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr
    
    make
}

package() {
    cd "${srcdir}/.."
    
    # Install MagicPodsCore binary
    install -Dm755 "build/MagicPodsCore" "${pkgdir}/usr/bin/magicpods-core"
    
    # Create virtual environment for UI dependencies
    install -dm755 "${pkgdir}/opt/magicpods"
    python -m venv "${pkgdir}/opt/magicpods/venv"
    
    # Install Python dependencies in the venv
    "${pkgdir}/opt/magicpods/venv/bin/pip" install --upgrade pip
    "${pkgdir}/opt/magicpods/venv/bin/pip" install textual websocket-client
    
    # Install UI files
    install -dm755 "${pkgdir}/opt/magicpods/ui"
    cp -r ui/* "${pkgdir}/opt/magicpods/ui/"
    
    # Install launcher script
    install -Dm755 "arch/magicpods-ui" "${pkgdir}/usr/bin/magicpods-ui"
    
    # Install systemd service
    install -Dm644 "arch/magicpods.service" "${pkgdir}/usr/lib/systemd/system/magicpods.service"
    
    # Install README
    install -Dm644 "README.md" "${pkgdir}/usr/share/doc/${pkgname}/README.md"
    
    # Install LICENSE if exists
    if [ -f "LICENSE" ]; then
        install -Dm644 "LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    fi
}

