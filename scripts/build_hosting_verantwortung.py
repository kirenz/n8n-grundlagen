import sys
out=sys.argv[1]
W,H=900,500
cols=[("Cloud","n8n betreibt die Technik",["you","n8n","n8n","n8n"],"ab ca. 24 € im Monat","Start in Minuten"),
      ("Managed Hosting","Anbieter betreibt die Technik",["you","prov","prov","prov"],"ab ca. 7 € im Monat","eigene Instanz, keine Server-Pflege"),
      ("Self-Hosted","Ihr Team betreibt alles selbst",["you","you","you","you"],"keine Lizenzkosten","1 bis 3 Std. Pflege im Monat")]
layers=["Workflows und Zugangsdaten","Sicherheit (TLS) und Überwachung","Updates und Backups","Server und Rechenzentrum"]
fill={"you":("#0052ff","#ffffff","Ihr Team"),"n8n":("#e4e4e7","#18181b","n8n"),"prov":("#f4f4f5","#18181b","Anbieter")}
F='font-family="Inter, Helvetica, Arial, sans-serif"'
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
cw,gap,x0,y0,lh=260,30,30,90,62
for ci,(name,sub,who,cost,eff) in enumerate(cols):
    x=x0+ci*(cw+gap)
    s.append(f'<text x="{x+cw/2}" y="40" text-anchor="middle" {F} font-size="22" font-weight="700" fill="#18181b">{name}</text>')
    s.append(f'<text x="{x+cw/2}" y="66" text-anchor="middle" {F} font-size="14" fill="#52525b">{sub}</text>')
    for li,l in enumerate(layers):
        y=y0+li*(lh+6); bg,fg,lab=fill[who[li]]
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{lh}" rx="8" fill="{bg}" stroke="#d4d4d8"/>')
        s.append(f'<text x="{x+14}" y="{y+26}" {F} font-size="14" font-weight="600" fill="{fg}">{l}</text>')
        s.append(f'<text x="{x+14}" y="{y+47}" {F} font-size="13" fill="{fg}" opacity="0.85">{lab}</text>')
    yb=y0+4*(lh+6)+30
    s.append(f'<text x="{x+cw/2}" y="{yb}" text-anchor="middle" {F} font-size="16" font-weight="700" fill="#18181b">{cost}</text>')
    s.append(f'<text x="{x+cw/2}" y="{yb+24}" text-anchor="middle" {F} font-size="14" fill="#52525b">{eff}</text>')
# legend
ly=H-28; lx=30
for key in ("you","n8n","prov"):
    bg,fg,lab=fill[key]
    s.append(f'<rect x="{lx}" y="{ly-14}" width="18" height="18" rx="4" fill="{bg}" stroke="#d4d4d8"/>')
    s.append(f'<text x="{lx+26}" y="{ly}" {F} font-size="14" fill="#18181b">{lab}</text>'); lx+=150
s.append(f'<text x="{W-30}" y="{ly}" text-anchor="end" {F} font-size="13" fill="#52525b">Preise: Größenordnung, Tarife ändern sich</text>')
s.append('</svg>'); open(out,'w').write('\n'.join(s))
