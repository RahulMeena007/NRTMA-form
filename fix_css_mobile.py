footer_mobile = """
@media (max-width: 768px) {
  .footer-main {
      grid-template-columns: 1fr;
      padding: 40px 20px 20px;
  }
}
"""
with open("apply.css", "a", encoding="utf-8") as f:
    f.write(footer_mobile)
