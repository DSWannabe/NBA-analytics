import asyncio
from playwright.async_api import async_playwright
import pycountry as pc


# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto(
#             "https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season=1999-00"
#         )
#         # Wait for the dropdowns to be available
#         await page.wait_for_selector("select.DropDown_select__4pIg9")

#         # Find all dropdowns with the class DropDown_select__4pIg9
#         dropdowns = await page.query_selector_all("select.DropDown_select__4pIg9")

#         # Iterate through the dropdowns to find the one with the -1 option
#         for dropdown in dropdowns:
#             options = await dropdown.query_selector_all("option")
#             for option in options:
#                 if await option.get_attribute("value") == "-1":
#                     await dropdown.select_option(value="-1")
#                     break

#         # Debugging: Check the selected value
#         selected_value = None
#         for dropdown in dropdowns:
#             if await dropdown.evaluate("el => el.value") == "-1":
#                 selected_value = await dropdown.evaluate("el => el.value")
#                 break
#         print(f"Selected value: {selected_value}")

#         await browser.close()

# asyncio.run(main())

a = "1924 R3 Pick 25"
year_draft, round, lll, pick = a.replace(',', '').split()
print(year_draft, round[1:], pick)