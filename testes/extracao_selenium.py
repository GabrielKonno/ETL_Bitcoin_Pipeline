import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def obter_preco_bitcoin_infomoney():
    """Utiliza Selenium para capturar o preço do Bitcoin no Infomoney."""

    # Config do Webdriver

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        url = "https://www.infomoney.com.br/cotacoes/cripto/ativo/bitcoin-btc/"
        driver.get(url)

        # Espera alguns segundos para a página carregar completamente
        time.sleep(5)

        # Localiza o elemento que contém o preço do bitcoin
        xpath = '/html/body/div[4]/div/div[1]/div[1]/div/div[3]/div[1]/p'
        elemtno_preco = driver.find_element(By.XPATH, xpath)
        preco_bitcoin = elemtno_preco.text.strip()

        print(f"Preço atual do Bitcoin (InfoMoney): {preco_bitcoin}")

    except Exception as e:
        print(f"Erro ao obter o preço: {e}")
    finally:
        driver.quit()
    
if __name__ == "__main__":
    obter_preco_bitcoin_infomoney()