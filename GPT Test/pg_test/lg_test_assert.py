LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

VALID_USER = "Admin"
VALID_PASS = "admin123"


def acessar_login(page):
    page.goto(LOGIN_URL)
    page.wait_for_selector("input[name='username']")


def preencher_login(page, user, senha):
    page.fill("input[name='username']", user)
    page.fill("input[name='password']", senha)
    page.click("button[type='submit']")


def log_result(ct, status, detalhe=""):
    print(f"[{ct}] - {status} {detalhe}")


def test_ct01_login_valido(page):
    acessar_login(page)
    preencher_login(page, VALID_USER, VALID_PASS)
    page.wait_for_timeout(6000)
    # Verifica se está na dashboard
    assert "/dashboard" in page.url, "Não redirecionou para dashboard"


def test_ct02_senha_invalida(page):
    acessar_login(page)
    preencher_login(page, VALID_USER, "")
    page.wait_for_timeout(6000)
    visible = page.locator("text=Invalid credentials").is_visible()
    assert visible, "Mensagem 'Invalid credentials' não exibida"
    if visible:
        log_result("CT-02", "PASS", "- Mensagem exibida corretamente")
    else:
        log_result("CT-02", "FAIL", "- Mensagem não encontrada")
        page.screenshot(path="ct02_fail.png")


def test_ct03_usuario_invalido(page):
    acessar_login(page)
    preencher_login(page, "ad", VALID_PASS)
    page.wait_for_timeout(6000)
    visible = page.locator("text=Invalid credentials").is_visible()
    assert visible, "Mensagem 'Invalid credentials' não exibida"
    if visible:
        log_result("CT-03", "PASS")
    else:
        log_result("CT-03", "FAIL")
        page.screenshot(path="ct03_fail.png")


def test_ct04_usuario_senha_invalidos(page):
    acessar_login(page)
    preencher_login(page, "fake", "fake123")
    page.wait_for_timeout(6000)
    visible = page.locator("text=Invalid credentials").is_visible()
    assert visible, "Mensagem 'Invalid credentials' não exibida"
    if visible:
        log_result("CT-04", "PASS")
    else:
        log_result("CT-04", "FAIL")
        page.screenshot(path="ct04_fail.png")


def test_ct05_usuario_vazio(page):
    acessar_login(page)
    preencher_login(page, "", VALID_PASS)
    page.wait_for_timeout(6000)
    visible = page.locator("text=Required").is_visible()
    assert visible, "Mensagem 'Required' não exibida"
    if visible:
        log_result("CT-05", "PASS")
    else:
        log_result("CT-05", "FAIL")
        page.screenshot(path="ct05_fail.png")


def test_ct06_senha_vazia(page):
    acessar_login(page)
    preencher_login(page, VALID_USER, "")
    page.wait_for_timeout(6000)
    visible = page.locator("text=Required").is_visible()
    assert visible, "Mensagem 'Required' não exibida"
    if visible:
        log_result("CT-06", "PASS")
    else:
        log_result("CT-06", "FAIL")
        page.screenshot(path="ct06_fail.png")


def test_ct07_campos_vazios(page):
    acessar_login(page)
    preencher_login(page, "", "")
    page.wait_for_timeout(6000)
    count = page.locator("text=Required").count()
    assert count >= 1, "Mensagem 'Required' não exibida para campos vazios"
    if count >= 1:
        log_result("CT-07", "PASS")
    else:
        log_result("CT-07", "FAIL")
        page.screenshot(path="ct07_fail.png")


def test_ct08_case_sensitive(page):
    acessar_login(page)
    preencher_login(page, "admin", "ADMIN123")
    page.wait_for_timeout(6000)
    visible = page.locator("text=Invalid credentials").is_visible()
    assert visible, "Mensagem 'Invalid credentials' não exibida"
    if visible:
        log_result("CT-08", "PASS")
    else:
        log_result("CT-08", "FAIL")
        page.screenshot(path="ct08_fail.png")


def test_ct09_persistencia_sessao(page):
    acessar_login(page)
    preencher_login(page, VALID_USER, VALID_PASS)
    page.wait_for_url("**/dashboard", timeout=10000)
    page.reload()
    assert "/dashboard" in page.url, "Sessão não mantida após reload"
    if "/dashboard" in page.url:
        log_result("CT-09", "PASS", "- Sessão mantida após reload")
    else:
        log_result("CT-09", "FAIL")
        page.screenshot(path="ct09_fail.png")


def test_ct10_logout(page):
    acessar_login(page)
    preencher_login(page, VALID_USER, VALID_PASS)
    page.wait_for_url("**/dashboard", timeout=5000)
    page.click("i.oxd-userdropdown-icon")
    page.click("text=Logout")
    page.wait_for_url("**/login", timeout=5000)
    assert "/login" in page.url, "Logout não redirecionou para login"
    if "/login" in page.url:
        log_result("CT-10", "PASS", "- Logout realizado")
    else:
        log_result("CT-10", "FAIL")
        page.screenshot(path="ct10_fail.png")
