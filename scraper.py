import asyncio
import aiohttp

from terminal import cprint_success, cprint_failure, cprint_warning, cprint_info


# URL_BASE = "https://www.bbc.com/mundo"
URL_BASE = "https://www.bbc.es"


class Response():
    '''
    HTML response container.

    Attributes:
    - headers (str): HTML headers response.
    - html (str): HTML code response.
    '''

    def __init__(self, headers: str, html: str) -> None:
        '''
        Response initializer.

        Args:
        - headers (str): HTML headers response.
        - html (str): HTML code response.
        '''
        self.__headers = headers
        self.__html = html

    def get_headers(self):
        '''
        Gets headers attribute.
        '''
        return self.__headers

    def get_html(self):
        '''
        Gets html attribute.
        '''
        return self.__html


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
                        f"{url} | Attempt: {i+1} | Response status: {response.status}.")
                    return Response(response.headers, await response.text())
                elif response.status in {301, 302}:
                    cprint_warning(
                        f"{url} | Attempt: {i+1} | Redirected ({response.status}).")
                else:
                    cprint_warning(
                        f"{url} | Attempt: {i+1} | HTTP {response.status} received.")

        except aiohttp.ClientConnectionError:
            cprint_failure(f"{url} | Attempt: {i+1} | Connection error.")
        except aiohttp.ClientResponseError as e:
            cprint_failure(
                f"{url} | Attempt: {i+1} | Response error: {e.status} {e.message}")
        except aiohttp.ClientPayloadError:
            cprint_failure(f"{url} | Attempt: {i+1} | Payload error.")
        except asyncio.TimeoutError:
            cprint_failure(f"{url} | Attempt: {i+1} | Timeout error.")
        except UnicodeDecodeError:
            cprint_failure(
                f"{url} | Attempt: {i+1} | Encoding error while decoding response.")
        except Exception as e:
            cprint_failure(f"{url} | Attempt: {i+1} | Unexpected error: {e}")

    cprint_failure(f"{url} | could not be resolved after {retries} attempts")
    return None


async def wrapper(url_base):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url_base)
        if response:
            cprint_info(response.get_html())


if __name__ == "__main__":
    asyncio.run(wrapper(URL_BASE))
