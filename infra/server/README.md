# n8n Self-Host Stack — Setup-Anleitung

Produktiver n8n-Stack auf Hetzner CX33 mit Postgres, Caddy als Reverse Proxy und Auto-TLS.

## Voraussetzungen

- Hetzner CX33 läuft (Ubuntu 24.04 LTS empfohlen)
- DNS: A-Record `n8n.kirenz.de → 49.12.14.207` ist gesetzt und propagiert (`dig +short n8n.kirenz.de` zeigt die IP)
- SSH-Key-Auth zum Server steht (`ssh hetzner` läuft passwortfrei)
- Lokal `git`, optional `rsync`

## Setup in 8 Schritten

### 1. Server vorbereiten (einmalig)

```bash
ssh hetzner

# System aktuell halten
apt update && apt upgrade -y

# Docker installieren (Engine + Compose-Plugin)
curl -fsSL https://get.docker.com | sh

# Firewall: nur 22, 80, 443 zulassen
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Stack-Verzeichnis anlegen
mkdir -p /opt/n8n
exit
```

### 2. Templates auf den Server kopieren

```bash
# Vom lokalen Mac aus, im n8n-ai-agents-Repo
cd /Users/jankirenz/code/kurse/n8n-ai-agents
rsync -avz infra/server/ hetzner:/opt/n8n/
```

### 3. .env auf dem Server anlegen

```bash
ssh hetzner
cd /opt/n8n
cp .env.example .env

# Encryption Key generieren — diesen Wert NIE wieder ändern
echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env.tmp

# Postgres-Passwörter generieren
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '/+=' | head -c 32)" >> .env.tmp
echo "POSTGRES_NON_ROOT_PASSWORD=$(openssl rand -base64 32 | tr -d '/+=' | head -c 32)" >> .env.tmp

# Werte aus .env.tmp manuell in .env übernehmen, Platzhalter ersetzen
nano .env
rm .env.tmp
```

**Wichtig:** Den Inhalt von `.env` auch lokal in 1Password / Bitwarden hinterlegen. Wenn der Server stirbt und du den Encryption-Key verlierst, sind alle gespeicherten Credentials in n8n unwiederbringlich verloren.

### 4. Init-Skript ausführbar machen

```bash
chmod +x /opt/n8n/init-postgres.sh
chmod +x /opt/n8n/backup.sh
```

### 5. Stack starten

```bash
cd /opt/n8n
docker compose up -d

# Warten bis n8n hochgefahren ist (~30 Sekunden)
docker compose logs -f n8n
# Strg+C wenn 'Editor is now accessible via:' erscheint
```

### 6. Erstmaliger UI-Zugriff

`https://n8n.kirenz.de` im Browser öffnen. Beim ersten Aufruf richtet n8n den Owner-Account ein:

- E-Mail
- Vor- und Nachname
- Starkes Passwort (Bitwarden / 1Password)

Dieser Account ist dein Admin-Login für die UI.

### 7. Backups aktivieren

```bash
ssh hetzner

# SSH-Key auf der Storage Box hinterlegen, falls noch nicht
ssh-keygen -t ed25519 -f ~/.ssh/storagebox -N ""
# Den public key per Hetzner-Console / Storage-Box-Web-UI auf der Box hinzufügen

# SSH-Config-Eintrag für die Box
cat >> ~/.ssh/config <<'EOF'
Host storagebox
  HostName u580735.your-storagebox.de
  User u580735
  Port 23
  IdentityFile ~/.ssh/storagebox
EOF

# Cron-Job einrichten
crontab -e
# Zeile hinzufügen:
# 0 3 * * * /opt/n8n/backup.sh >> /var/log/n8n-backup.log 2>&1

# Erstes Backup manuell testen
/opt/n8n/backup.sh
```

### 8. SSH-Härtung (nach erfolgreichem Setup)

```bash
ssh hetzner

# Passwort-Login deaktivieren
sed -i 's/#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh

# root-Passwort rotieren (sicherheitshalber, auch wenn Login deaktiviert)
passwd
# Starkes Passwort vergeben — nur als Fallback für Hetzner-Console
```

## Update-Routine (monatlich)

```bash
ssh hetzner
cd /opt/n8n

# Aktuelle Versionen ziehen
docker compose pull

# Neu starten mit neuen Images
docker compose up -d

# Logs prüfen
docker compose logs --tail 50 n8n
```

## Workflow-Migration vom lokalen Container

Sobald n8n auf dem Server läuft, alle 5 Modul-Workflows aus dem lokalen Container per Skript migrieren:

```bash
cd /Users/jankirenz/code/kurse/n8n-ai-agents
infra/server/migrate-workflows.sh
```

Das Skript liest die JSON-Dateien aus `workflows/` und legt sie per n8n-API auf dem Server an. Voraussetzung: API-Key vom Server-n8n.

## Troubleshooting

**Caddy bekommt kein TLS-Zertifikat:**
- `dig +short n8n.kirenz.de` muss `49.12.14.207` zurückgeben — wenn nicht, DNS abwarten
- Port 80 muss von außen erreichbar sein (Hetzner Cloud Firewall + UFW)
- `docker compose logs caddy` zeigt ACME-Fehler

**n8n-UI zeigt nur weiße Seite:**
- `WEBHOOK_URL` und `N8N_HOST` müssen auf `n8n.kirenz.de` stehen
- `N8N_PROTOCOL=https` und `N8N_PROXY_HOPS=1` (Caddy davor)

**Workflows aktivieren sich nicht:**
- IMAP/SMTP-Credentials prüfen
- `docker compose logs n8n` zeigt Fehler-Stack

## Sicherheits-Hinweise

- `.env` enthält Klartext-Passwörter — `chmod 600 .env` und niemals committed
- `N8N_ENCRYPTION_KEY` extern sichern (1Password)
- Nur 22/80/443 öffentlich, alle anderen Ports zu
- n8n-User-Management aktiv, jeder User mit eigenem Login
- Backup-Restore quartalsweise testen (sonst weiß man nicht, ob's geht)
