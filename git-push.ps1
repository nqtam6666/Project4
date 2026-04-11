# =============================================================================
# GIT PUSH SCRIPT - NQT Gym Project
# Tu dong push code len nhanh rieng cua tung thanh vien
# =============================================================================

param(
    [Alias("m")]
    [string]$Message = "",

    [Alias("b")]
    [string]$Branch = "",

    [switch]$Help
)

# Hien thi huong dan
if ($Help) {
    Write-Host @"

=== GIT PUSH SCRIPT ===

Cach dung:
    .\git-push.ps1                              # Push voi message mac dinh
    .\git-push.ps1 -m "Them chuc nang login"    # Push voi message tuy chinh
    .\git-push.ps1 -b "nqt"                     # Chi dinh ten nhanh
    .\git-push.ps1 -m "Fix bug" -b "vtq"        # Ket hop ca hai

Tham so:
    -m, -Message    Noi dung commit message
    -b, -Branch     Ten nhanh (mac dinh: lay tu username hoac hoi)
    -Help           Hien thi huong dan nay

Vi du workflow:
    1. Moi thanh vien push len nhanh rieng: nqt, vtq, pnm...
    2. Chu project review va merge vao main

"@ -ForegroundColor Cyan
    exit 0
}

# -----------------------------------------------------------------------------
# Ham tien ich
# -----------------------------------------------------------------------------

function Write-Step {
    param([string]$Step, [string]$Description)
    Write-Host "[$Step] " -ForegroundColor Yellow -NoNewline
    Write-Host $Description -ForegroundColor White
}

function Write-OK {
    param([string]$Text)
    Write-Host "[OK] " -ForegroundColor Green -NoNewline
    Write-Host $Text -ForegroundColor White
}

function Write-Err {
    param([string]$Text)
    Write-Host "[LOI] " -ForegroundColor Red -NoNewline
    Write-Host $Text -ForegroundColor White
}

# -----------------------------------------------------------------------------
# Kiem tra moi truong
# -----------------------------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       GIT PUSH - NQT Gym Project      " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiem tra co phai git repo khong
if (-not (Test-Path ".git")) {
    Write-Err "Thu muc hien tai khong phai git repository!"
    exit 1
}

# Kiem tra co thay doi gi khong
$nqtStatus = git status --porcelain
if ([string]::IsNullOrWhiteSpace($nqtStatus)) {
    Write-Host "Khong co thay doi nao de commit." -ForegroundColor Yellow

    # Hoi co muon push commit cu khong
    $nqtUnpushed = git log origin/HEAD..HEAD --oneline 2>$null
    if (-not [string]::IsNullOrWhiteSpace($nqtUnpushed)) {
        Write-Host "Co commits chua push:" -ForegroundColor Yellow
        Write-Host $nqtUnpushed -ForegroundColor Gray
        $nqtConfirm = Read-Host "Ban co muon push cac commits nay? (y/n)"
        if ($nqtConfirm -ne "y" -and $nqtConfirm -ne "Y") {
            exit 0
        }
    } else {
        exit 0
    }
}

# -----------------------------------------------------------------------------
# Xac dinh ten nhanh
# -----------------------------------------------------------------------------

if ([string]::IsNullOrWhiteSpace($Branch)) {
    $nqtDefaultBranch = $env:USERNAME.ToLower()

    if ($nqtDefaultBranch.Length -gt 10) {
        $nqtDefaultBranch = $nqtDefaultBranch.Substring(0, 3)
    }

    Write-Host "Ten nhanh mac dinh: " -NoNewline
    Write-Host $nqtDefaultBranch -ForegroundColor Green

    $nqtInputBranch = Read-Host "Nhan Enter de dung hoac nhap ten khac"

    if ([string]::IsNullOrWhiteSpace($nqtInputBranch)) {
        $Branch = $nqtDefaultBranch
    } else {
        $Branch = $nqtInputBranch
    }
}

$Branch = $Branch -replace '[^a-zA-Z0-9_-]', ''

if ([string]::IsNullOrWhiteSpace($Branch)) {
    Write-Err "Ten nhanh khong hop le!"
    exit 1
}

Write-OK "Se push len nhanh: $Branch"

# -----------------------------------------------------------------------------
# Xac dinh commit message
# -----------------------------------------------------------------------------

if ([string]::IsNullOrWhiteSpace($Message)) {
    $nqtTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $nqtDefaultMessage = "Update $nqtTimestamp"

    $nqtInputMessage = Read-Host "Nhap commit message (Enter = mac dinh)"

    if ([string]::IsNullOrWhiteSpace($nqtInputMessage)) {
        $Message = $nqtDefaultMessage
    } else {
        $Message = $nqtInputMessage
    }
}

# -----------------------------------------------------------------------------
# Hien thi preview thay doi
# -----------------------------------------------------------------------------

Write-Host ""
Write-Step "1" "Cac file thay doi:"
Write-Host "----------------------------------------" -ForegroundColor Gray

git status --short

Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host ""

Write-Host "Thong tin commit:" -ForegroundColor Yellow
Write-Host "  Nhanh  : $Branch" -ForegroundColor White
Write-Host "  Message: $Message" -ForegroundColor White
Write-Host ""

$nqtConfirm = Read-Host "Xac nhan push? (y/n)"
if ($nqtConfirm -ne "y" -and $nqtConfirm -ne "Y") {
    Write-Host "Da huy." -ForegroundColor Yellow
    exit 0
}

# -----------------------------------------------------------------------------
# Thuc hien git operations
# -----------------------------------------------------------------------------

Write-Host ""

# Buoc 1: Checkout/tao nhanh
Write-Step "2" "Chuyen sang nhanh..."

$nqtCurrentBranch = git branch --show-current

if ($nqtCurrentBranch -ne $Branch) {
    $nqtBranchExists = git branch --list $Branch
    $nqtRemoteBranchExists = git branch -r --list "origin/$Branch"

    if (-not [string]::IsNullOrWhiteSpace($nqtBranchExists)) {
        git checkout $Branch
    } elseif (-not [string]::IsNullOrWhiteSpace($nqtRemoteBranchExists)) {
        git checkout -b $Branch origin/$Branch
    } else {
        git checkout -b $Branch
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Err "Khong the chuyen sang nhanh!"
        exit 1
    }
}

Write-OK "Dang o nhanh: $Branch"

# Buoc 2: Add all changes
Write-Step "3" "Staging tat ca thay doi..."
git add -A

if ($LASTEXITCODE -ne 0) {
    Write-Err "Loi khi staging files!"
    exit 1
}

Write-OK "Da staging tat ca files"

# Buoc 3: Commit
Write-Step "4" "Tao commit..."

$nqtStagedChanges = git diff --cached --name-only
if (-not [string]::IsNullOrWhiteSpace($nqtStagedChanges)) {
    git commit -m "$Message"

    if ($LASTEXITCODE -ne 0) {
        Write-Err "Loi khi commit!"
        exit 1
    }

    Write-OK "Da commit: $Message"
} else {
    Write-Host "Khong co thay doi moi de commit" -ForegroundColor Yellow
}

# Buoc 4: Push
Write-Step "5" "Push len remote..."
git push -u origin $Branch

if ($LASTEXITCODE -ne 0) {
    Write-Err "Loi khi push! Thu pull truoc..."
    git pull origin $Branch --rebase
    git push -u origin $Branch

    if ($LASTEXITCODE -ne 0) {
        Write-Err "Van khong the push. Vui long kiem tra thu cong."
        exit 1
    }
}

Write-OK "Da push thanh cong len origin/$Branch"

# -----------------------------------------------------------------------------
# Hoan thanh
# -----------------------------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "           PUSH THANH CONG!            " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Nhanh: " -NoNewline
Write-Host $Branch -ForegroundColor Cyan
Write-Host ""
Write-Host "Buoc tiep theo:" -ForegroundColor Yellow
Write-Host "  1. Thong bao cho chu project review" -ForegroundColor White
Write-Host "  2. Chu project se merge vao main" -ForegroundColor White
Write-Host ""
