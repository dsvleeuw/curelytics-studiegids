<#
  Lavish -> Claude loop voor de CureLytics-studiegids.

  1. Bouwt de fiches (python _generator/build.py)
  2. Opent de studiegids in Lavish Editor (http://127.0.0.1:4387/...)
  3. Wacht op feedback uit de browser (lavish-axi poll)
  4. Stuurt elke feedback door naar Claude Code (claude -p), die de bron aanpast en opnieuw bouwt
  5. Toont Claude's samenvatting in Lavish en wacht op de volgende feedback

  Stoppen: klik in Lavish op "End session" / "Send & End", of druk Ctrl+C.
#>
param(
    [string]$Bestand = "curelytics-gids.html"
)

# Continue: npx/claude schrijven waarschuwingen naar stderr; onder "Stop" zou Windows PowerShell daarop afbreken.
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8
$utf8 = New-Object System.Text.UTF8Encoding($false)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$logDir = Join-Path $root "_tools\log"
New-Item -ItemType Directory -Force $logDir | Out-Null
$replyFile = Join-Path $logDir "laatste-antwoord.md"

function Stap($tekst) { Write-Host ""; Write-Host "==> $tekst" -ForegroundColor Cyan }

foreach ($cmd in "python", "npx", "claude") {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "'$cmd' is niet gevonden. Installeer het eerst." -ForegroundColor Red
        exit 1
    }
}

Stap "Fiches bouwen"
python _generator/build.py
if ($LASTEXITCODE -ne 0) { Write-Host "Build mislukt." -ForegroundColor Red; exit 1 }

Stap "Studiegids openen in Lavish (http://127.0.0.1:4387)"
$open = (npx -y lavish-axi $Bestand 2>&1 | Out-String)
if ($open -match "did not reopen it") {
    # De sessie was eerder vanuit de browser beëindigd; jij start dit script bewust, dus heropenen.
    $open = (npx -y lavish-axi $Bestand --reopen 2>&1 | Out-String)
}
Write-Host $open
if ($open -match 'url:\s*"([^"]+)"') { Write-Host "Lavish draait op $($Matches[1])" -ForegroundColor Green }

$prompt = @'
Je krijgt hieronder feedback uit Lavish Editor op de CureLytics-studiegids (curelytics-gids.html).
Werk volgens CLAUDE.md in deze map. Belangrijk:
- Elk <article> heeft een id (bv. bi-004) en een attribuut data-bron dat zegt welk bestand en welke index
  de bron is (bv. "_generator/content_bi.py · FICHES[3]"). Uitbreidingen (visuals, praktijk, begrippen, code,
  tabel, valkuilen, quiz) staan in het bijbehorende _extra.py-bestand onder dezelfde index in EXTRA.
- Opmaak/UI zit in _generator/ui.css, _generator/ui.js, _generator/build.py en _generator/diagrams.py.
- Bewerk NOOIT de gegenereerde HTML direct. Pas de bron aan en draai daarna: python _generator/build.py
- Bijgevoegde screenshots (paden in de feedback) mag je openen om te zien wat bedoeld wordt.
- Is iets onduidelijk, doe dan de meest redelijke interpretatie en noem dat in je samenvatting.
Eindig met een korte samenvatting in het Nederlands (max 6 bullets) van wat je hebt aangepast.
Die samenvatting wordt in Lavish aan de gebruiker getoond.

=== FEEDBACK UIT LAVISH ===
'@

$allowed = "Read,Edit,Write,Glob,Grep,Bash(python _generator/build.py),Bash(python _generator/build.py:*),PowerShell(python _generator/build.py)"
$ronde = 0
$heeftAntwoord = $false

while ($true) {
    $ronde++
    Stap "Wachten op feedback uit Lavish (ronde $ronde) - typ/annoteer in de browser en klik 'Send to Agent'"
    if ($heeftAntwoord) {
        $poll = (npx -y lavish-axi poll $Bestand --takeover --owner "claude-loop" --agent-reply-file $replyFile 2>&1 | Out-String)
    } else {
        $poll = (npx -y lavish-axi poll $Bestand --takeover --owner "claude-loop" 2>&1 | Out-String)
    }
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    [IO.File]::WriteAllText((Join-Path $logDir "feedback-$stamp.txt"), $poll, $utf8)

    $isFeedback = $poll -match 'status:\s*"?feedback'
    $isEnded = ($poll -match 'status:\s*"?ended') -or ($poll -match 'session_ended:\s*true')
    $isDisconnected = $poll -match 'status:\s*"?browser_disconnected'

    if ($isDisconnected) {
        Write-Host "Het Lavish-venster is gesloten of verbroken. Draai het script opnieuw om verder te gaan." -ForegroundColor Yellow
        break
    }
    if (-not $isFeedback) {
        if ($isEnded) { Write-Host "Sessie beëindigd in Lavish. Tot de volgende keer!" -ForegroundColor Green; break }
        Write-Host "Onverwachte uitvoer van lavish-axi (zie _tools\log\feedback-$stamp.txt). Opnieuw wachten..." -ForegroundColor Yellow
        Write-Host $poll
        Start-Sleep -Seconds 2
        continue
    }

    Stap "Feedback doorsturen naar Claude"
    $antwoord = ($prompt + "`n" + $poll) | claude -p --permission-mode acceptEdits --allowedTools $allowed 2>&1 | Out-String
    if ([string]::IsNullOrWhiteSpace($antwoord)) { $antwoord = "Claude gaf geen antwoord terug - kijk in het terminalvenster." }
    [IO.File]::WriteAllText($replyFile, $antwoord.Trim(), $utf8)
    [IO.File]::WriteAllText((Join-Path $logDir "antwoord-$stamp.md"), $antwoord, $utf8)
    Write-Host $antwoord
    $heeftAntwoord = $true

    if ($isEnded) {
        # Laatste batch van "Send & End": antwoord nog tonen, dan stoppen.
        npx -y lavish-axi reply $Bestand --agent-reply-file $replyFile 2>&1 | Out-Null
        Write-Host "Laatste feedback verwerkt; sessie was beëindigd. Klaar." -ForegroundColor Green
        break
    }
}
