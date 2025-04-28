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

# ✅ Diccionario de productos y criterios
PRODUCT_CATEGORIES = {
    # Olímpica
    "Arroz 1KG": {
        "url": "https://www.olimpica.com/arroz?page={page}",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Azúcar 1KG": {
        "url": "https://www.olimpica.com/azucar?_q=Azucar&map=ft&page={page}",
        "unidad": r"\b(1[\s]?kg|1[\s]?k|1000[\s]?g|1\.000[\s]?g|1kilo|1 kilo)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Aceite 3L Cocina": {
        "url": "https://www.olimpica.com/aceites?page={page}",
        "unidad": r"\b(3[\s]?(l|lt|litros)|3000[\s]?ml)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Huevos 30": {
        "url": "https://www.olimpica.com/huevos?page={page}",
        "unidad": r"\b(30[\s]?(und|unidades|huevos))\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Leche 1L": {
        "url": "https://www.olimpica.com/leche?page={page}",
        "unidad": r"\b(1[\s]?(l|lt)|1 litro|1000ml)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Pan tajado": {
        "url": "https://www.olimpica.com/panes?page={page}",
        "unidad": r"(tajado|molde|rebanad)",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Papa 1.5KG o 2.5KG": {
        "url": "https://www.olimpica.com/papa?page={page}",
        "unidad": r"\b((1[.,]5[\s]?kg|1500g|1[\s]?1/2[\s]?kg)|(2[.,]5[\s]?kg|2500g|2[\s]?1/2[\s]?kg))\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Fríjol 500G": {
        "url": "https://www.olimpica.com/frijol?page={page}",
        "unidad": r"\b(500[\s]?g|0[.,]?5[\s]?kg|1/2[\s]?kg|½[\s]?kg)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    # Jumbo
    "Arroz 1KG": {
        "url": "https://www.jumbocolombia.com/arroz?_q=Arroz&map=ft",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "div.product-card__name",
            "price": "div.product-card__price"
        }
    },

    "Azúcar 1KG": {
        "url": "https://www.olimpica.com/azucar?_q=Azucar&map=ft&page={page}",
        "unidad": r"\b(1[\s]?kg|1[\s]?k|1000[\s]?g|1\.000[\s]?g|1kilo|1 kilo)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Aceite 3L Cocina": {
        "url": "https://www.olimpica.com/aceites?page={page}",
        "unidad": r"\b(3[\s]?(l|lt|litros)|3000[\s]?ml)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Huevos 30": {
        "url": "https://www.olimpica.com/huevos?page={page}",
        "unidad": r"\b(30[\s]?(und|unidades|huevos))\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Leche 1L": {
        "url": "https://www.olimpica.com/leche?page={page}",
        "unidad": r"\b(1[\s]?(l|lt)|1 litro|1000ml)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Pan tajado": {
        "url": "https://www.olimpica.com/panes?page={page}",
        "unidad": r"(tajado|molde|rebanad)",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Papa 1.5KG o 2.5KG": {
        "url": "https://www.olimpica.com/papa?page={page}",
        "unidad": r"\b((1[.,]5[\s]?kg|1500g|1[\s]?1/2[\s]?kg)|(2[.,]5[\s]?kg|2500g|2[\s]?1/2[\s]?kg))\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    "Fríjol 500G": {
        "url": "https://www.olimpica.com/frijol?page={page}",
        "unidad": r"\b(500[\s]?g|0[.,]?5[\s]?kg|1/2[\s]?kg|½[\s]?kg)\b",
        "selectors": {
            "name": "span.vtex-product-summary-2-x-productBrand",
            "price": "div.olimpica-dinamic-flags-0-x-priceContainer"
        }
    },
    
    # Ara
    "Arroz 1KG Ara": {
        "url": "https://www.ara.com.co/supermercado/arroz?page={page}",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "span.product-name",
            "price": "span.price"
        }
    },
    "Azúcar 1KG Ara": {
        "url": "https://www.ara.com.co/supermercado/azucar?page={page}",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "span.product-name",
            "price": "span.price"
        }
    },
    # Exito
    "Arroz 1KG Exito": {
        "url": "https://www.exito.com/categoria/arroz?page={page}",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "h4.product-title",
            "price": "span.product-price"
        }
    },
    "Azúcar 1KG Exito": {
        "url": "https://www.exito.com/categoria/azucar?page={page}",
        "unidad": r"\b(1[\s]?kg|1000g|1k)\b",
        "selectors": {
            "name": "h4.product-title",
            "price": "span.product-price"
        }
    },
}

PAGES_PER_PRODUCT = 5
SITE_NAME = "Supermercados"
EXCEL_FILE = "canasta_familiar_precios.xlsx"

# 🔍 Scraping general con filtros
def scrape_product_prices(category_url, product_label, unidad_regex, selectors, pages=5):
    """
    Scrapea los precios de productos de diferentes supermercados (Jumbo, Ara, Éxito, Olímpica) 
    basándose en los selectores proporcionados.
    """
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
        # Ajustar el selector de producto dependiendo del supermercado
        if product_label in ["Arroz 1KG Jumbo", "Arroz 1KG Exito"]:  # Ajuste según el sitio
            product_cards = soup.select("div.product-card")  # Para Jumbo y Éxito
        else:
            product_cards = soup.select("article.vtex-product-summary-2-x-element")  # Para Olímpica, Ara

        print(f"   📦 {len(product_cards)} productos encontrados")

        for card in product_cards:
            name_elem = card.select_one(selectors['name'])
            price_container = card.select_one(selectors['price'])

            if not name_elem or not price_container:
                continue

            name = name_elem.get_text(strip=True).lower()
            price_text = "".join(span.get_text(strip=True) for span in price_container.find_all("span"))

            match = re.search(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?", price_text)
            if match:
                price = float(match.group().replace(".", "").replace(",", "."))

                # Detectar unidad (si es necesario)
                unidades_match = re.search(r"x\s?(\d{1,2})", name)
                unidades = int(unidades_match.group(1)) if unidades_match else 1
                precio_unitario = round(price / unidades, 2)

                # Filtrar por unidad y tipo de producto
                if re.search(unidad_regex, name):
                    prices.append(precio_unitario)
                    print(f"   ✅ ACEPTADO '{name}' → total: {price}, unidades: {unidades}, unitario: {precio_unitario}")
                else:
                    print(f"   ❌ DESCARTADO '{name}' (no coincide con unidad esperada)")

    driver.quit()
    return prices

# 📊 Guardar en Excel
columns = ["Date", "Site"] + list(PRODUCT_CATEGORIES.keys())
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=columns)

today = datetime.today().strftime('%Y-%m-%d')
new_row = [today, SITE_NAME]

# Procesar cada producto
for label, info in PRODUCT_CATEGORIES.items():
    url_template = info["url"]
    unidad_regex = info["unidad"]
    selectors = info["selectors"]

    product_prices = scrape_product_prices(url_template, label, unidad_regex, selectors, PAGES_PER_PRODUCT)

    if product_prices:
        avg_price = round(sum(product_prices) / len(product_prices), 2)
        new_row.append(avg_price)
    else:
        new_row.append(None)

# Guardar resultados
df.loc[len(df)] = new_row
df.to_excel(EXCEL_FILE, index=False)

print("\n✅ Todos los precios promedio fueron guardados exitosamente.")
