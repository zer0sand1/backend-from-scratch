from router import Router


def dummy_handler(request):
    return "dummy_response"


def another_handler(request):
    return "another_response"


def test_add_and_match_route():
    router = Router()
    router.add("GET", "/", dummy_handler)

    result = router.match("GET", "/")

    assert result is dummy_handler


def test_match_returns_none_for_unknown_route():
    router = Router()

    result = router.match("GET", "/")

    assert result is None


def test_match_returns_none_for_method_mismatch():
    router = Router()
    router.add("GET", "/", dummy_handler)

    result = router.match("POST", "/")

    assert result is None


def test_match_case_insensitive_method():
    router = Router()
    router.add("GET", "/", dummy_handler)

    assert router.match("get", "/") is dummy_handler
    assert router.match("GET", "/") is dummy_handler
    assert router.match("Get", "/") is dummy_handler


def test_add_overwrites_existing_route():
    router = Router()
    router.add("GET", "/", dummy_handler)
    router.add("GET", "/", another_handler)

    result = router.match("GET", "/")

    assert result is another_handler


def test_multiple_routes():
    router = Router()
    router.add("GET", "/", dummy_handler)
    router.add("POST", "/data", another_handler)
    router.add("GET", "/about", dummy_handler)

    assert router.match("GET", "/") is dummy_handler
    assert router.match("POST", "/data") is another_handler
    assert router.match("GET", "/about") is dummy_handler


def test_match_path_is_case_sensitive():
    router = Router()
    router.add("GET", "/about", dummy_handler)

    result = router.match("GET", "/About")

    assert result is None