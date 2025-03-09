# Modules
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
# Packages
from bs4 import BeautifulSoup
# Own
from terminal import cprint_success, cprint_failure, cprint_warning, cprint_info
from classes import Response


# URL_BASE_BBC = "https://www.bbccom/mundo"
URL_BASE_BBC = "https://www.bbc.com/mundo"


async def fetch(session: aiohttp.ClientSession, url: str, retries: int = 3, timeout: int = 5) -> Response | None:
    """
    Get HTML body of an URL.

    Args:
        session (aiohttp.ClientSession): aiohttp session responsible for performing multiple asynchronous requests.
        url (str): URL to fetch.
        retries (int, optional): Number of retries to get the URL (default: 3).
        timeout (int, optional): Maximum waiting time for a response (default: 5).

    Returns:
        Response | None: Instance of Response if successful, otherwise None.
    """
    for i in range(retries):
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    cprint_success(
                        f"{fetch.__name__} | {url} | Attempt: {i+1} | Response status: {response.status}.")
                    return Response(response.headers, await response.text())
                elif response.status in {301, 302}:
                    cprint_warning(
                        f"{url} | Attempt: {i+1} | Redirected ({response.status}).")
                else:
                    cprint_warning(
                        f"{url} | Attempt: {i+1} | HTTP {response.status} received.")

        except aiohttp.ClientConnectionError:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Connection error.")
        except aiohttp.ClientResponseError as e:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Response error: {e.status} {e.message}")
        except aiohttp.ClientPayloadError:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Payload error.")
        except asyncio.TimeoutError:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Timeout error.")
        except UnicodeDecodeError:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Encoding error while decoding response.")
        except Exception as e:
            cprint_failure(
                f"{fetch.__name__} | {url} | Attempt: {i+1} | Unexpected error: {e}")

    cprint_failure(
        f"{fetch.__name__} | {url} | could not be resolved after {retries} attempts")
    return None


def extract_urls(html: str, url_base: str) -> set:
    '''
    Extract all URLs from the given HTML code that are within the specified base URL.

    Args:
    - html (str): The HTML code to extract links from.
    - url_base (str): The base URL to filter links by. Only links from the same domain and 
                      starting with this URL base will be extracted.

    Returns:
    - set: A set of URLs that were extracted and match the base URL criteria.
    '''
    try:
        urls = set()
        soup = BeautifulSoup(html, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            url = urljoin(url_base, a_tag["href"])
            if urlparse(url_base).netloc == urlparse(url).netloc and url.startswith(url_base):
                # cprint_warning(url)
                urls.add(url)
    except Exception as e:
        cprint_failure(f"{extract_urls.__name__} | Unexpected error: {e}")
        return set()
    else:
        return urls


async def wrapper(url_seed, url_base):
    try:
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url_seed)
            if response:
                # cprint_info(response.get_html())
                extract_urls(response.get_html(), url_base)
                # Guardar los links en un json
                # Controlar que no existan ya
                # Hacer que el proceso sea lo más paralelizable y eficiente posible
    except Exception as e:
        cprint_failure(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(wrapper(URL_BASE_BBC, URL_BASE_BBC))
