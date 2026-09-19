# Liedjie Herkenner — Opstel-instruksies

## 1. Kry 'n gratis AudD.io sleutel
Gaan na https://audd.io, registreer, kopieer jou API-token.

## 2. Host dit gratis op Render.com
1. Gaan na https://render.com en skep 'n gratis rekening
2. Skep 'n nuwe GitHub repository en laai al hierdie lêers op
   (app.py, requirements.txt, Dockerfile, templates/index.html)
3. In Render: "New +" → "Web Service" → koppel jou GitHub repo
4. Render sal die Dockerfile outomaties oplaai (kies "Docker" as omgewing)
5. Onder "Environment", voeg 'n environment variable by:
   - Key: AUDD_API_KEY
   - Value: (jou AudD sleutel)
6. Klik "Create Web Service" — wag ~5 minute vir die eerste bou

## 3. Gebruik dit op jou foon
Sodra dit klaar gebou is, gee Render jou 'n skakel soos:
https://liedjie-herkenner.onrender.com

Maak dit oop in jou foon se blaaier, voeg dit by jou tuisskerm
("Add to Home Screen") sodat dit soos 'n app lyk, en jy's gereed.

Let wel: Render se gratis vlak "slaap" na 15 min onaktiwiteit — die
eerste versoek na 'n slapie kan 30-60 sekondes vat om wakker te word.
