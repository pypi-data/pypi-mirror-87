![](https://github.com/navikt/dataverk-vault/workflows/Unittests/badge.svg)
![](https://github.com/navikt/dataverk-vault/workflows/Release/badge.svg)
![](https://badge.fury.io/py/dataverk-vault.svg)

# Dataverk vault

Bibliotek med api mot vault for secrets handling og database credential generering for dataverk

### Installasjon

#### Master branch versjon
```
git clone https://github.com/navikt/dataverk-vault.git
cd dataverk-vault
pip install .
```

#### Siste release
```
pip install dataverk-vault
```

## Environment variabler
Følgende miljøvariabler må være satt der biblioteket brukes:
- APPLICATION_NAME: Applikasjonsnavn i vault
- K8S_SERVICEACCOUNT_PATH: Serviceaccount sti i containermiljø
- VKS_VAULT_ADDR: Vault adresse
- VKS_AUTH_PATH: Autentisering URI
- VKS_KV_PATH: Secrets URI

## Eksempler på bruk
````python
from dataverk_vault import api as vault_api

# Hent hemmeligheter
secrets = vault_api.read_secrets()

# Hent hemmeligheter og sett de som miljøvariabler
vault_api.set_secrets_as_envs()

# Hent nytt brukernavn/passord for postgres databaser
new_creds = vault_api.get_database_creds("postgresql/<sone>/creds/<db>-<role>")
````

## For NAV-ansatte
Interne henvendelser kan sendes via Slack i kanalen #dataverk