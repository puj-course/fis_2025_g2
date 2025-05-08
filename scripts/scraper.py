from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os
import time

PAGES_PER_PRODUCT = 5
EXCEL_FILE = "canasta_familiar_precios.xlsx"

SUPERMARKET_CATEGORIES = {
    "Olimpica": {
        "selectors": {
            "card": "article.vtex-product-summary-2-x-element",
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        },
        "products": {
            "Arroz 1KG": {
                "url": "https://www.olimpica.com/arroz?page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?kg|1000[\s]?g(r)?(s)?|1[\s]?k(ilo)?)\b"
            },
            "Azúcar 1KG": {
                "url": "https://www.olimpica.com/azucar?_q=Azucar&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?kg|1[\s]?k|1000[\s]?g(r)?(s)?|1\.000[\s]?g|1[\s]?kilo)\b"
            },
            "Aceite 3L Cocina": {
                "url": "https://www.olimpica.com/aceites?page={page}",
                "unidad": r"\b(x\s*)?(3[\s]?(l|lt|litros)|3000[\s]?ml|3\.0[\s]?l)\b"
            },
            "Huevos 30": {
                "url": "https://www.olimpica.com/huevos?page={page}",
                "unidad": r"\b(x\s*)?30[\s]?(unds|unidades|huevos|und)\b"
            },
            "Leche 1L": {
                "url": "https://www.olimpica.com/leche?page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?(l|lt)|1[\s]?litro|1000[\s]?ml)\b"
            },
            "Pan tajado": {
                "url": "https://www.olimpica.com/panes?page={page}",
                "unidad": r"\b(tajado|molde|rebanad)\b"
            },
            "Papa 1.5KG o 2.5KG": {
                "url": "https://www.olimpica.com/papa?page={page}",
                "unidad": r"\b(x\s*)?((1[.,]5[\s]?kg|1500[\s]?g(r)?(s)?|1[\s]?1/2[\s]?kg)|(2[.,]5[\s]?kg|2500[\s]?g(r)?(s)?|2[\s]?1/2[\s]?kg))\b"
            },
            "Fríjol 500G": {
                "url": "https://www.olimpica.com/frijol?page={page}",
                "unidad": r"\b(x\s*)?(500[\s]?g(r)?(s)?|0[.,]?5[\s]?kg|1/2[\s]?kg|½[\s]?kg)\b"
            }
        }
    },
    "Jumbo": {
        "selectors": {
            "card": "article.vtex-product-summary-2-x-element",
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.tiendasjumboqaio-jumbo-minicart-2-x-price"
        },
        "products": {
            "Arroz 1KG": {
                "url": "https://www.jumbocolombia.com/arroz?_q=arroz&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?kg|1000[\s]?g(r)?(s)?|1[\s]?k(ilo)?)\b"
            },
            "Azúcar 1KG": {
                "url": "https://www.jumbocolombia.com/azucar?_q=azucar&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?kg|1[\s]?k|1000[\s]?g(r)?(s)?|1\.000[\s]?g|1[\s]?kilo)\b"
            },
            "Aceite 3L Cocina": {
                "url": "https://www.jumbocolombia.com/aceite?_q=aceite&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(3[\s]?(l|lt|litros)|3000[\s]?ml|3\.0[\s]?l)\b"
            },
            "Huevos 30": {
                "url": "https://www.jumbocolombia.com/huevos?_q=huevos&map=ft&page={page}",
                "unidad": r"\b(x\s*)?30[\s]?(und|unidades|huevos|unds)\b"
            },
            "Leche 1L": {
                "url": "https://www.jumbocolombia.com/leche?_q=leche&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(1[\s]?(l|lt)|1[\s]?litro|1000[\s]?ml)\b"
            },
            "Pan tajado": {
                "url": "https://www.jumbocolombia.com/pan?_q=pan&map=ft&page={page}",
                "unidad": r"\b(tajado|molde|rebanad)\b"
            },
            "Papa 1.5KG o 2.5KG": {
                "url": "https://www.jumbocolombia.com/papa?_q=papa&map=ft&page={page}",
                "unidad": r"\b(x\s*)?((1[.,]5[\s]?kg|1500[\s]?g(r)?(s)?|1[\s]?1/2[\s]?kg)|(2[.,]5[\s]?kg|2500[\s]?g(r)?(s)?|2[\s]?1/2[\s]?kg))\b"
            },
            "Fríjol 500G": {
                "url": "https://www.jumbocolombia.com/frijol?_q=frijol&map=ft&page={page}",
                "unidad": r"\b(x\s*)?(500[\s]?g(r)?(s)?|0[.,]?5[\s]?kg|1/2[\s]?kg|½[\s]?kg)\b"
            }
        }
    }, 
    "Exito": {
        "selectors": {
            "card": "article[class^='productCard_productCard']",
            "name": "h3.styles_name__qQJiK",
            "price": "p.ProductPrice_container__price__XmMWA"
        },
        "products": {
            "Arroz 1KG": {
                "url": "https://www.exito.com/s?q=Arroz&sort=score_desc&page=0{page}",
                "unidad": r"\b(x\s*)?(1000\s+g(r)?(s)?|1\s*k(ilo)?|1\s*kg)\b"
            },
            "Azúcar 1KG": {
                "url": "https://www.exito.com/s?q=Azucar&sort=score_desc&page=0{page}",
                "unidad":  r"\b(x\s*)?(1000\s+g(r)?(s)?|1\s*k(ilo)?|1\s*kg|1\s*k)\b"
            },
            "Aceite 3L Cocina": {
                "url": "https://www.exito.com/s?q=Aceite&sort=score_desc&page=0{page}",
                "unidad":  r"\b(x\s*)?(3\s*l(itros)?|3\s*lt|3000\s+ml|3[.,]0\s*l)\b"
            },
            "Huevos 30": {
                "url": "https://www.exito.com/s?q=Huevos&sort=score_desc&page=0{page}",
                "unidad":  r"\b(x\s*)?30\s+(und|unidades|huevos|unds)\b"
            },
            "Leche 1L": {
                "url": "https://www.exito.com/s?q=Leche&sort=score_desc&page=0{page}",
                "unidad": r"\b(x\s*)?(1\s*l|1\s*lt|1\s*litro|1000\s+ml)\b"
            },
            "Pan tajado": {
                "url": "https://www.exito.com/s?q=Pan&sort=score_desc&page=0{page}",
                "unidad":  r"\b(tajado|molde|rebanad)\b"
            },
            "Papa 1.5KG o 2.5KG": {
                "url": "https://www.exito.com/s?q=Papa&sort=score_desc&page=0{page}",
                "unidad": r"\b(x\s*)?((1[.,]?5\s*kg|1500\s+g(r)?(s)?|1\s+1/2\s*kg)|(2[.,]?5\s*kg|2500\s+g(r)?(s)?|2\s+1/2\s*kg))\b"
            },
            "Fríjol 500G": {
                "url": "https://www.exito.com/s?q=Frijol&sort=score_desc&page=0{page}",
                "unidad": r"\b(x\s*)?(500\s+g(r)?(s)?|0[.,]?\s*5\s*kg|1/2\s*kg|½\s*kg)\b"
            }
        }
    }
}



def scrape_product_prices(category_url, product_label, unidad_regex, pages, selectors):
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=options
    )

    prices = []

    for page in range(1, pages + 1):
        url = category_url.format(page=page)
        print(f"\n🔎 Buscando '{product_label}' en: {url}")
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_cards = soup.select(selectors["card"])
        print(f"   📦 {len(product_cards)} productos encontrados")

        for card in product_cards:
            name_elem = card.select_one(selectors["name"])
            price_elem = card.select_one(selectors["price"])

            if not name_elem or not price_elem:
                continue

            name = name_elem.get_text(strip=True).lower()
            price_text = price_elem.get_text(strip=True).replace("\xa0", " ")

            match = re.search(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?", price_text)
            if match:
                price = float(match.group().replace(".", "").replace(",", "."))

                unidades_match = re.search(r"x\s?(\d{1,2})", name)
                unidades = int(unidades_match.group(1)) if unidades_match else 1
                precio_unitario = round(price / unidades, 2)

                if "aceite" in product_label.lower():
                    if re.search(unidad_regex, name) and re.search(r"(aceite).*(soya|vegetal|mezcla|girasol|canola|cocina)", name):
                        prices.append(precio_unitario)
                        print(f"   ✅ ACEPTADO '{name}' → total: {price}, unidades: {unidades}, unitario: {precio_unitario}")
                    else:
                        print(f"   ❌ DESCARTADO '{name}' (no cumple unidad y/o tipo)")
                elif "leche" in product_label.lower():
                    if re.search(unidad_regex, name):
                        prices.append(precio_unitario)
                        print(f"   ✅ ACEPTADO '{name}' → total: {price}, unidades: {unidades}, unitario: {precio_unitario}")
                    else:
                        print(f"   ❌ DESCARTADO '{name}' (no coincide con unidad esperada)")
                else:
                    if re.search(unidad_regex, name):
                        prices.append(price)
                        print(f"   ✅ ACEPTADO '{name}' → {price}")
                    else:
                        print(f"   ❌ DESCARTADO '{name}' (no coincide con unidad esperada)")
            else:
                print(f"   ⚠️ Precio no encontrado en '{name}'")

    driver.quit()
    return prices


columns = ["Date", "Site"] + list(next(iter(SUPERMARKET_CATEGORIES.values()))["products"].keys())
df = pd.read_excel(EXCEL_FILE) if os.path.exists(EXCEL_FILE) else pd.DataFrame(columns=columns)
today = datetime.today().strftime('%Y-%m-%d')

for supermarket, data in SUPERMARKET_CATEGORIES.items():
    new_row = [today, supermarket]
    for product_label, product_info in data["products"].items():
        url = product_info["url"]
        unidad = product_info["unidad"]
        selectors = data["selectors"]

        prices = scrape_product_prices(url, product_label, unidad, PAGES_PER_PRODUCT, selectors,)
        avg_price = round(sum(prices) / len(prices), 2) if prices else None
        new_row.append(avg_price)

    df.loc[len(df)] = new_row
    df.to_excel(EXCEL_FILE, index=False)

print("\\n✅ Precios actualizados correctamente.")