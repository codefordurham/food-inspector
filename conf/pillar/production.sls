#!yaml|gpg

environment: production

# FIXME: Change to match production domain name
domain: eatsmart.rochapps.com

# FIXME: Update to the correct project repo
repo:
  url: git@github.com:codefordurham/Durham-Restaurants.git
  branch: project_template_upgrade

requirements_file: requirements/production.txt

# Additional public environment variables to set for the project
env:
  FOO: BAR

# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
# http_auth:
#   username: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----

# Private environment variables.
# Must be GPG encrypted.
secrets:
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAxy5mLEdeO4ZAQf/R7YIwh81EiOmyxPtsjw3Z3mQn/SdYYWUu0dnkgZrgXLN
    Qe7UVEgUoEJjFiQsnxHxG6ld9wB7ek/gZQ8VqEG5LGwbyVk++EQUQM8vZbzJ9Q78
    czF+VyJZrPBgdu2tKkyBHlSesiE+umlTp379muKH8+pyo4yVVQR6OlatRTaO6DWn
    zctKZVMeV/2OX5wBuBz9l27U4uzBOAkVHQl7L4aG1Kpae2Lg8XqnRnN4DBLW5IPy
    wQbqxufLU7vNi+t3fo10qR7ZjWAlfdBujKxPhKH1uP55YOx7Y/SILR/dp+HVYaO5
    bo3m+Zvn7Ci98NbnPiugjDvZfsIu1qKZumtM3aK/LNJ7AZb0BwBRq4Cz7eoCpvUS
    PeTGa/0oyIwUkGd2OajnFGlHsm1jhpRZgtfaqzJysC5AH5sOQo8iYebGoV1Df6vt
    BfGRO45UMyD2z726v0M2OoS+qseGwVtbry9D+Lcu/MMXTEeSggVygpX8LWX2gOGY
    B5p38MGkZc0yaVjv
    =lsD1
    -----END PGP MESSAGE-----

  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAxy5mLEdeO4ZAQgAp+Z+YcP4Khk9XzuUq66BLP2KeVfDLiuGD0d5jH1x/ap2
    rSNj9bQTXKkFF31AOK96pUTBi6gtHPA/gHzn9MImkXlXBKSodb14iHav1+05trme
    VXODP/1IqlG10q35Jh5B8IZJVG0UulqPOIVUhYcsChOnSQck7cK3k0IliEiB6Fwj
    EUISRHZ+dEquOhmqCcrU50XUlz6gpli+hAeCnYqcJv7HsTvGpQTXA7cVvLOzhokB
    KtyhSB+v/AtmBTuwdX9N9l5kMp0d7ppFvILeBtxg51Bll0N3WLkIarTO1fv1v3Pg
    6IalpsE/c0BPsTHtgHWTKUWbbV5DQGAU3V00WGFeyNJOAQA54IUyqfq+r8B7bIsU
    FKuxD4yrOyHISXOrKeBLT3opEg9ElsfnEr9FNtXAFnfMieIeBXQZjlGAad2mlzOl
    tRRQ1OcGgguGm7KME6IM
    =0l/b
    -----END PGP MESSAGE-----

  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAxy5mLEdeO4ZAQf+NHAS7mRETVfIA8lvg611HYw2jwkBs2AXphOxs5x76Xyk
    g+WtBY0IPVkyUIDH4Jmnw8x9ZO7KDksNaDHYKGX4maRwp7k57ekAl8D44I5x379p
    aT8Yeq6zUAQBAH4LRBUScB4CDeffFne6p61S0cMyxexIDJsDL1RraKG8OG3CkM3K
    cwxZIlxW+xwl/ISHQzBTa1qanQ1jUDXdRXi42lZXpcRucKB0nRlkATaiTNnfWmgC
    bUbwp+r48ao1bkftfuIR1ears11cIZ+prXeGReCfQX8GvGPd3SpVO9ZWU6pcyLWW
    mXycRe6K74Xb8a4xpgvRgze6ldRSKYbKJazlS2bQRNJOAXjitxvCddkpszQCEhf3
    pE3gUugqAvLQqwO+3BN/mo05dp3/IS/OyL7TqbRGUOgP6AHuwj2Hvc53HAc6wQrQ
    K8FRUmQZM3jJfLsbb3m+
    =u+ox
    -----END PGP MESSAGE-----


# Private deploy key. Must be GPG encrypted.
github_deploy_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =Qw/+
  -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
# {% if 'balancer' in grains['roles'] %}
# ssl_key: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----
#
# ssl_cert: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----
# {% endif %}
