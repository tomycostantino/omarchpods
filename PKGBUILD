pkgname=omarchpods
pkgver=0.0.1
pkgrel=1
pkgdesc="Headphones manager for Omarchy"
arch=('x86_64')
url="https://github.com/tomycostantino/omarchpods"
depends=('bluez' 'python')
makedepends=('cmake' 'gcc' 'git')
backup=('etc/omarchpods/omarchpods.conf')
source=()
sha256sums=()

build() {
    cd "${srcdir}/.."
 

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


    install -Dm755 "build/MagicPodsCore" "${pkgdir}/usr/bin/omarchpods"

    install -dm755 "${pkgdir}/opt/omarchpods"


    install -dm755 "${pkgdir}/opt/omarchpods/ui"
    cp -r ui/* "${pkgdir}/opt/omarchpods/ui/"

    install -Dm644 "omarchpods.service" "${pkgdir}/usr/lib/systemd/user/omarchpods.service"

    cat > "${pkgdir}/usr/bin/omarchy-launch-omarchpods" << 'EOF'
#!/bin/bash
xdg-terminal-exec --app-id=com.omarchy.Omarchy --title=Omarchpods python /opt/omarchpods/ui/main.py
EOF
    chmod +x "${pkgdir}/usr/bin/omarchy-launch-omarchpods"

    if [ -f "LICENSE" ]; then
        install -Dm644 "LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    fi
}

