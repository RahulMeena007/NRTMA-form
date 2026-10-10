with open("apply.html", "r", encoding="utf-8") as f:
    html = f.read()

ids = ["btnOption1", "choice-section", "form-section", "onlineBackBtn", "onlineBackBtnBottom", "submitBtn", "successPopup", "closePopupBtn"]
for i in ids:
    if f'id="{i}"' in html or f"id='{i}'" in html:
        print(f"Found {i}")
    else:
        print(f"MISSING {i}")
