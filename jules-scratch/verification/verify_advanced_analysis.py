import re
from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:5173/")

    # Fill out the form
    page.get_by_label("คุณดูซีรีส์วาย (BL) หรือ Yuri (GL) บ่อยแค่ไหน?").select_option("4")
    page.get_by_label("คุณติดตามอินฟลูเอนเซอร์ LGBTQ+ หรือไม่?").select_option("4")
    page.get_by_label("ครอบครัวมีทัศนคติต่อ LGBTQ+ อย่างไร?").select_option("4")
    page.get_by_label("เพื่อนสนิทของคุณมีคนที่เป็น LGBTQ+ หรือไม่?").select_option("4")
    page.get_by_label("สถานศึกษา/ที่ทำงานของคุณสนับสนุน LGBTQ+ หรือไม่?").select_option("2")

    # Submit for initial analysis
    page.get_by_role("button", name="✨ คำนวณผลลัพธ์").click()

    # Wait for the first result card to appear
    expect(page.get_by_text("ผลการวิเคราะห์")).to_be_visible()

    # Click the advanced analysis button
    page.get_by_role("button", name="🔬 เรียกใช้การวิเคราะห์ขั้นสูง").click()

    # In the dialog, choose AI insights
    with page.expect_response("**/api/v2/analysis") as response_info:
        page.get_by_role("button", name="🤖 Get AI Insights").click()

    # Wait for the advanced results to appear
    expect(page.get_by_text("🔬 Two-Way ANOVA Analysis")).to_be_visible()

    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)