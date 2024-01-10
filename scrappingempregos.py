"""
Imagine que foi contrato e precisa obter informações de um site, e então você é solicitado para fazer o scraping do site empregos.com, extrair as  informações relevantes das postagens de emprego e as armazenar.
Tarefa:
1- Seu script deve ser capaz de visitar o site empregos.com e navegar pelas páginas de postagens de emprego.
2- Seu script deve extrair informações relevantes de cada postagem de emprego. As informações a serem extraídas incluem, mas não se limitam a, o título do emprego, a descrição do emprego, a localização do emprego e o nome da empresa.
3- Após extrair as informações, seu script deve armazená-las de maneira temporário ou então em um banco de dados
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrappingDoSiteEmpregos(search_query='scrappythonsiteempregos'):
    site = 'https://www.empregos.com.br/'

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('window-size=1920,1080')
    navegador = webdriver.Chrome(options=options)

    try:
        navegador.get(site)

        time.sleep(5)

        encontrarInputPrimeiraPagina = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[name="ctl00$ContentBody$ucSuggestCargo$txtCargo"]'))
        )

        encontrarInputPrimeiraPagina.send_keys(search_query)

        encontrarBotaoDeBuscarVagas = WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_ContentBody_lnkBuscar'))
        )
        encontrarBotaoDeBuscarVagas.click()

        with open('vagas-do-site-empregos-com-br.txt', 'w', encoding='utf-8') as file:
            file.write('')

        while True:
            WebDriverWait(navegador, 20).until(
                EC.presence_of_element_located((By.ID, 'ctl00_ContentBody_divPaiMioloBusca')))

            time.sleep(5)

            vagas = navegador.find_elements(By.XPATH,
                                            '//li[contains(@class, "item  ") or contains(@class, "item  vaga-patrocinada")]')

            with open('vagas-do-site-empregos-com-br.txt', 'a', encoding='utf-8') as file:
                for vaga in vagas:
                    # Coletando titulo das vagas
                    try:
                        buscaTituloDasVagas = vaga.find_element(By.XPATH, './/h2/a')
                        tituloDasVagas = buscaTituloDasVagas.text.strip() if buscaTituloDasVagas.text else 'Título não encontrado'
                    except:
                        tituloDasVagas = 'Título não encontrado'
                    # coletando nome das empresas
                    try:
                        buscaNomeDasEmpresas = vaga.find_element(By.XPATH, './/span[@class="nome-empresa"]/a')
                        nomeEmpresas = buscaNomeDasEmpresas.text.strip() if buscaNomeDasEmpresas.text else 'Empresa confidencial'
                    except:
                        nomeEmpresas = 'Empresa confidencial'
                    # Coletando descrição das vagas
                    try:
                        buscaDescricaoVagas = vaga.find_element(By.XPATH, './/p[@class="resumo-vaga"]')
                        descricaoVagas = buscaDescricaoVagas.text.strip() if buscaDescricaoVagas.text else 'Descrição não disponível'
                    except:
                        descricaoVagas = 'Descrição não disponível'
                    # Coletando salario
                    buscaSalarioDasVagas = vaga.find_elements(By.XPATH, './/div[contains(@class, "salario-de-ate")]')
                    salarioVagas = buscaSalarioDasVagas[
                        0].text.strip() if buscaSalarioDasVagas else 'Salário a combinar'

                    file.write(
                        f'Título: {tituloDasVagas}\nEmpresa: {nomeEmpresas}\nDescrição: {descricaoVagas}\nSalário: {salarioVagas}\n\n')

            try:
                botaoDePopupEmail = WebDriverWait(navegador, 3).until(
                    EC.element_to_be_clickable((By.ID, 'ctl00_ContentBody_aFecharModalLead'))
                )
                botaoDePopupEmail.click()
            except:
                pass
            try:
                botaoDeProximaPagina = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.ID, 'ctl00_ContentBody_lkbPaginacaoTopProximo'))
                )
                botaoDeProximaPagina.click()
                WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.ID, 'ctl00_ContentBody_divPaiMioloBusca')))
                time.sleep(3)
            except:
                break

    finally:
        navegador.quit()


if __name__ == '__main__':
    # CASO QUEIRA BUSCAR OUTRAS VAGAS COLOQUE O NOME NO PARAMETRO ABAIXO:
    scrappingDoSiteEmpregos(search_query='Desenvolvedor PHP')
