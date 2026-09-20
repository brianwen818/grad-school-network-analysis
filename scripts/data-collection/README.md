# 師資資料蒐集

本目錄提供 14 個系所的師資蒐集器。中文與英文官網會分開蒐集，再以站內識別碼、email、個人頁網址及姓名依序配對。

## 安裝

```powershell
python -m pip install -r scripts/data-collection/requirements.txt
python -m pip install -r scripts/data-collection/requirements-browser.txt
python -m playwright install chromium
```

第二、三行只在需要瀏覽器備援時執行。`ntu-ds` 與 `nthu-cs` 會優先使用頁面公開引用的同源 API／模組端點；端點失效時才改用 Chromium，清大資工另有系所正式 PDF 備援。

## 執行

```powershell
python scripts/data-collection/collect.py --school all
python scripts/data-collection/collect.py --school ntu-fin
python scripts/data-collection/collect.py --school ntu-ds --headed
```

`--school ntu-comm-engin-ds` 會自動映射到 `ntu-comm-engin-ds-network`，資料與分析都只寫入後者，避免產生重複目錄。

預設會更新 `data/data-collection/<school>`，並產生 `analysis/data-collection/<school>` 與跨校摘要。來源工作表位於 `data/data-collection/prof_info_page_links.xlsx`。使用 `--skip-analysis` 可略過分析輸出；`--dry-run` 只檢查設定與連結表，不連線也不寫檔。

網站 TLS 憑證若在受控網路環境中無法驗證，可暫時加入 `--insecure`；一般執行不建議使用。

## 測試

```powershell
python -m unittest discover -s scripts/data-collection/tests -v
```

設定 `FACULTY_LIVE_TESTS=1` 後會額外執行官網 smoke test。
