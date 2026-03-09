---
description: Antigravityのブラウザが起動しない問題の解決方法（Playwright キャッシュクリア）
---

# Antigravity ブラウザ起動問題の解決方法

## 問題
AntigravityでURLを渡してもブラウザが起動しない場合の対処法です。

## 原因
古い破損したPlaywright-goドライバのキャッシュが原因の可能性があります。

## 解決手順

### 1. Playwright キャッシュディレクトリの場所確認

**Mac/Linux:**
```bash
~/Library/Caches/ms-playwright-go
```

**Windows:**
```powershell
$env:LOCALAPPDATA\ms-playwright-go
# 実際のパス例: C:\Users\suzuki.takumi\AppData\Local\ms-playwright-go
```

### 2. キャッシュディレクトリの削除

**Mac/Linux:**
```bash
rm -rf ~/Library/Caches/ms-playwright-go
```

**Windows:**
```powershell
Remove-Item -Path "$env:LOCALAPPDATA\ms-playwright-go" -Recurse -Force
```

### 3. HOME環境変数の設定（Windows）

Windowsの場合、Playwrightの再インストール時に`$HOME`環境変数が必要です：

```powershell
[System.Environment]::SetEnvironmentVariable("HOME", $env:USERPROFILE, "User")
```

または、手動で設定：
1. 「システムのプロパティ」→「環境変数」を開く
2. ユーザー環境変数に `HOME` を追加
3. 値: `C:\Users\suzuki.takumi` （ユーザープロファイルのパス）

### 4. Antigravity の再起動

環境変数の変更を反映させるため、**Antigravityを完全に終了して再起動**してください。

### 5. 動作確認

再起動後、適当なURLでブラウザが正常に開くか確認します。

## 参考情報

この解決方法は、Xで共有されていた以下の情報を参考にしています：
> Antigravityからブラウザが起動しなかったのようやく解決した。
> 古い破損したPlaywright-goドライバのキャッシュが原因だったとClaude Sonnet 4.5 (Thinking) さんが教えてくれた。

---

## 定期的なキャッシュ削除（予防策）

### 手動でキャッシュを削除

いつでも以下のコマンドでキャッシュを削除できます：

```powershell
# // turbo
& "$env:USERPROFILE\Documents\blog_flows\.agent\scripts\clear-playwright-cache.ps1"
```

### タスクスケジューラで定期実行を設定

週1回（毎週月曜日の朝9時）に自動でキャッシュを削除する設定：

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$env:USERPROFILE\Documents\blog_flows\.agent\scripts\clear-playwright-cache.ps1`""
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "Clear-Playwright-Cache" -Action $action -Trigger $trigger -Settings $settings -Description "Antigravity Playwright キャッシュ定期削除"
```

### タスクの確認・削除

```powershell
# タスクの確認
Get-ScheduledTask -TaskName "Clear-Playwright-Cache"

# タスクの削除
Unregister-ScheduledTask -TaskName "Clear-Playwright-Cache" -Confirm:$false
```

---

## 実施日
2026-01-26
